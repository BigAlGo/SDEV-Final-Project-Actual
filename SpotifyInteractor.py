from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from tkinter import messagebox
import time
import random
import keyboard
import spotipy
import re
import threading

import OpenCVVision as OpenCv

class SpotifyInteractor():
    def __init__(self, screenWidth, screenHeight):
        self.vision = OpenCv.OpenCVVision(screenWidth, screenHeight, self.roundStart)

        self.makeHotKeys()
        self.songNumber = 0
        self.roundNumber = 1

        #Initing spotify
        # able to get and modify the playback state and able to read public playlists 
        SCOPE = "user-modify-playback-state user-read-playback-state"

        authManagerClient = SpotifyOAuth(
            client_id="35661866380c4cdcb93e51cc756ee958",
            client_secret="fd334360adb04a7980412c946f1e00af",
            redirect_uri="http://localhost:5000/callback",
            scope=SCOPE,
            show_dialog=True
        )
        self.spotifyClient = spotipy.Spotify(auth_manager = authManagerClient)
        self.devices = self.spotifyClient.devices()
        while not self.devices['devices']:
            messagebox.showwarning("No Devices", "No active devices found. Open Spotify on a device signed into your account and try again.")
            self.devices = self.spotifyClient.devices()
        self.nextSong = None
        self.roundLoop = False

    def roundStartHotKeyPressed(self):
        print("Button pressed")
        self.startRoundLoop()

    def startRoundLoop(self):
        if not self.roundLoop:
            self.roundLoop = True
            self.vision.startLoop()
            threading.Thread(target=self.roundStart, daemon=True).start()
            print("thread start")


    def stopRoundLoop(self):
        self.roundLoop = False
        self.vision.stopLoop()

    def roundStart(self):
        """Plays a song after a specified time"""
        print("roundStart")
        # I am in a thread so while loops don't affect the over all program

        round_start_time = time.monotonic()
        print("song #" + str(self.songNumber))
        print("round #" + str(self.roundNumber))

        # Get the current device
        device_id = self.devices['devices'][0]['id']

        # Get the playlist file
        file_name = self.getPlaylistFileFromSettings()
        with open("Songs\\" + file_name, "r") as song_file:
            if self.nextSong is None:
                song_line = song_file.readlines()[self.songNumber]
            else:
                song_line = self.nextSong

        # Extract song time from the song line
        song_time = float(song_line.split(" ")[-1].strip())

        # Determine game type
        file = open("Config\\settings", "r")
        game_type = file.readlines()[1].strip()
        file.close()

        # Adjust round timing based on game type
        wifi_offset = 0.5
        round_times = {
            "Normal": (30, 13, 45, 30, 25),
            "Swift": (30, 5, 45, 30, 9),
            "Spike": (11, 4, 20, 20, 7)
        }
        first_round_time, half_time_round, half_time_time, normal_round_time, over_time_round = round_times.get(game_type, (30, 13, 45, 30, 25))

        song_uri = self.convertUrlToUri(song_line.split(" ")[0])

        # Determine when to play the song
        play_after_time = round_start_time
        play_into_time = 0

        if self.roundNumber == 1:
            if song_time > first_round_time:
                play_into_time = song_time - first_round_time
            else:
                play_after_time += first_round_time - song_time - wifi_offset
            print("First round, song starts in:", first_round_time - (time.monotonic() - round_start_time))
        elif self.roundNumber == half_time_round or self.roundNumber >= over_time_round:
            if song_time > half_time_time:
                play_into_time = song_time - half_time_time
            else:
                play_after_time += half_time_time - song_time - wifi_offset
            print("Half-time round, song starts in:", half_time_time - (time.monotonic() - round_start_time))
        else:
            if song_time > normal_round_time:
                play_into_time = song_time - normal_round_time
            else:
                play_after_time += normal_round_time - song_time - wifi_offset
            print("Normal round, song starts in:", normal_round_time - (time.monotonic() - round_start_time))

        # Ensure play_after_time is in the future
        if time.monotonic() > play_after_time:
            print("Warning: play_after_time has already passed!")
            play_after_time = time.monotonic() + 0.1  # Small delay to avoid immediate playback

        if play_into_time == 0:
            # Wait for play_after_time
            while time.monotonic() < play_after_time and self.roundLoop:
                print(f"Waiting... {play_after_time - time.monotonic():.2f} seconds left")
                time.sleep(0.05)

            # Start playback
            start_time = time.monotonic()
            self.spotifyClient.start_playback(device_id = device_id, uris = [song_uri])
        else:
            # Start playback with offset
            start_time = time.monotonic()
            self.spotifyClient.start_playback(device_id = device_id, uris = [song_uri], position_ms = int((play_into_time - 0.67) * 1000))

        # Repeat track
        self.spotifyClient.repeat("track", device_id = device_id)

        print("Playback started, waiting for confirmation...")

        # Wait for playback confirmation
        while self.roundLoop:
            playback = self.spotifyClient.current_playback()
            if playback and playback["is_playing"]:
                actual_start_time = time.monotonic()
                break
            time.sleep(0.05)

        if not self.roundLoop:
            actual_start_time = time.monotonic()
        # Calculate actual delay
        delay = actual_start_time - start_time
        print(f"Actual playback delay: {delay:.3f} seconds")

        # Wait until beat drop
        print_time = time.monotonic() + song_time
        while time.monotonic() < print_time and self.roundLoop:
            remaining_time = print_time - time.monotonic()
            print(f"Time until beat drop: {remaining_time:.2f} seconds")
            time.sleep(0.1)

        print("Time for beat drop!")
        # Making sure the text is off screen before running vision
        time.sleep(0.5)

        # Update song number
        if self.nextSong is None:
            self.songNumber += 1
        else:
            self.nextSong = None

        self.roundNumber += 1
        
        if self.roundLoop:
            # I am still in a thread so while loops don't affect the over all program
            self.vision.mainLoop()
        else:
            self.resetRounds()

    def makeHotKeys(self):
        '''Creates the hotkeys based on the hotKeys file'''
        settingsFile = open("Config\\hotKeys", "r")
        fileLines = settingsFile.readlines()
        settingsFile.close()

        playKey = fileLines[0][:-1]
        endKey = fileLines[1][:-1]
        lowKey = fileLines[2][:-1]
        highKey = fileLines[3][:-1]
        pauseKey = fileLines[4][:-1]

        try:
            keyboard.add_hotkey(playKey, callback = self.roundStartHotKeyPressed)
            keyboard.add_hotkey(endKey, callback = self.stopRoundLoop)
            keyboard.add_hotkey(lowKey, callback = lambda: print("lowKey"))
            keyboard.add_hotkey(highKey, callback = lambda: print("highKey"))
            keyboard.add_hotkey(pauseKey, callback = lambda: print("pauseKey"))

            return True
        except (ValueError):
            return False

    def isValidPlaylist(self):
        '''Returns if the URL on line 3 of the settings file is valid'''
        settingsFile = open("Config\\settings", "r")
        playlistURL = settingsFile.readlines()[2]
        settingsFile.close()

        # Tries to fetch the playlist
        try:
            self.spotifyClient.playlist(playlistURL)
            return True
        except spotipy.exceptions.SpotifyException:
            return False

    def getPlaylistLinks(self, playlistFileName):
        '''Returns a list of lings to songs that have not been saved but are in the spotify playlist
        and writes songs from the master file that are not in the playlist file, to the playlist file'''        
        
        # Creates a list of all the saved songs 
        songsFile = open("Songs\\masterSongFile", "r")
        masterLines = songsFile.readlines()
        songsFile.close()

        masterSongs = []
        for line in masterLines:
            masterSongs.append(line[:line.find(" ")])

        songsFile = open("Songs\\" + playlistFileName, "r")
        oldLines = songsFile.readlines()
        songsFile.close()

        oldSongs = []
        for line in oldLines:
            oldSongs.append(line[:line.find(" ")])
        
        # Creates a list of all the songs in the playlist
        # Reads the url from settings
        settingsFile = open("Config\\settings", "r")
        playlistURL = settingsFile.readlines()[2]
        settingsFile.close()

        # Creates a list of new songs
        tracks = self.spotifyClient.playlist_tracks(playlistURL)['items']

        # Extract track URLs
        newSongs = []
        for track in tracks:
            if track["track"]:
                newSongs.append(track["track"]["external_urls"]["spotify"])
        
    
        playlistFile = open("Songs\\" + playlistFileName, "a")
        masterFile = open("Songs\\masterSongFile", "r")

        uniqueSongs = []
        found = False
        for newSong in newSongs:
            found = False
            for oldSong in oldSongs:
                if newSong == oldSong:
                    # Already in the playlist file, do nothing
                    found = True
                    break

            if not found:
                # Not in playlist file
                for masterSong in masterSongs:
                    if newSong == masterSong:
                        # Found in master songs, refind the whole line, then add to playlist file
                        masterFile.seek(0)
                        for masterLine in masterFile.readlines():
                            if masterLine.find(newSong) != -1:
                                newLine = masterLine
                                break
                        playlistFile.write(newLine)
                        found = True
                        break
                
                if not found:
                    # Not in master or playlist file, ask what time
                    uniqueSongs.append(newSong)
        
        playlistFile.close()
        masterFile.close()
        return uniqueSongs

    def shuffleSongs(self):
        '''This shuffles the songs in songNames'''
        fileName = self.getPlaylistFileFromSettings()
        songNames = open("Songs\\" + fileName, "r")

        songs = songNames.readlines()
        songNames.close()
        
        random.shuffle(songs)

        fileName = self.getPlaylistFileFromSettings()

        songNames = open("Songs\\" + fileName, "r")
        songNames.writelines(songs)
        songNames.close()

    def convertUrlToUri(self, spotifyUrl):
        """Converts from a Spotify URL to a Spotify URI"""
        if "track/" in spotifyUrl:
            # For Tracks
            trackId = spotifyUrl.split("track/")[1].split("?")[0]
            return "spotify:track:" + trackId
        elif "playlist/" in spotifyUrl:
            # For playlists
            playlistId = spotifyUrl.split("playlist/")[1].split("?")[0]
            return "spotify:playlist:" + playlistId
        return None

    def getDevices(self):
        '''Gets the divices signed into the account'''
        self.devices = self.spotifyClient.devices()
        return self.devices
    
    def getNameOfSong(self, url):
        '''Returns the name of a song given the url'''
        return self.spotifyClient.track(url)['name']
    
    def getNameofPlaylist(self, uri):
        '''Returns the name of a song given the uri'''
        id = uri.split("spotify:playlist:")[1]
        return self.spotifyClient.playlist(id)['name']
    
    def getPlaylistFileFromSettings(self):
        settingsFile = open("Config\\settings", "r")
        fileName = self.playlistURLToFileName(settingsFile.readlines()[2])
        settingsFile.close()
        return fileName
    
    def getSongTime(self):
        ''' Gets the time of the current song playing'''
        playback = self.spotifyClient.current_playback()

        # If somthing is playing
        if playback:
            songTime = playback["progress_ms"] / 1000 
            return songTime
        else:
            messagebox.showwarning("Song timing", "No song is currently playing.")
            return -1
    
    def sanitizeFilename(self, name):
        ''' Replaces invalid filename characters'''
        name = name.strip().replace(" ", "_")
        return re.sub(r'[<>:"/\\|?*]', "_", name)
    
    def playlistURLToFileName(self, url):
        '''Converts from url to uri to name to sanitized filename '''
        return self.sanitizeFilename(self.getNameofPlaylist(self.convertUrlToUri(url)))

    def searchForBestSong(self, name):
        '''Uses spotify's search to look for the 20 best songs'''
        return self.spotifyClient.search(q = name, type = "track", limit = 20)

    def deleteSongFile(self):
        '''Deleats the SongNames File'''
        #Deletes the current songNames file
        fileName = self.getPlaylistFileFromSettings()

        open("Songs\\" + fileName, "r").close()
    
    def removeHotkeys(self):
        '''Removes any hotkeys'''
        keyboard.remove_all_hotkeys()

    def resetRounds(self):
        '''Resets the rounds and pauses playback'''
        self.spotifyClient.pause_playback()
        self.roundNumber = 1
    
    def setNextSong(self, set):
        '''Sets the next song'''
        self.nextSong = set