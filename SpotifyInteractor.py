from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from tkinter import messagebox
import time
import random
import keyboard
import spotipy
import re

class SpotifyInteractor():
    def __init__(self):
        self.makeHotKey()
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
        self.nextSong = None

    def hotKeyPressed(self):
        '''Plays a song after a specified time'''
        roundStartTime = time.time()
        print("song #" + str(self.songNumber))
        print("round #"+ str(self.roundNumber))

        #Gets the current device
        deviceId = self.devices['devices'][0]['id']

        songNameFile = open("Config\\songNames", "r")
        if (self.nextSong == None):
            songLine = songNameFile.readlines()[self.songNumber]
        else:
            songLine = self.nextSong
            self.nextSong = None

        # Gets the string from after the space to before the \n
        if (songLine.find("\n") != -1):
            songTime = float(songLine[songLine.find(" ") + 1 :])
        else:
            songTime = float(songLine[songLine.find(" ") + 1 : -1])

        songNameFile.close()

        # Opening the settings file to get the type of game
        settingsFile = open("Config\\settings", "r")
        gameType = settingsFile.readlines()[2][:-1]
        settingsFile.close()

        # Offset for calling from wifi
        wifiOffset = 0.45
        if gameType == "Normal":
            overTimeRound = 25
            firstRoundTime = 30
            halfTimeRound = 13
            halfTimeTime = 45
            normalRoundTime = 30
        elif gameType == "Swift":
            overTimeRound = 9
            firstRoundTime = 30
            halfTimeRound = 5
            halfTimeTime = 45
            normalRoundTime = 30
        elif gameType == "Spike":
            # todo fix these numbers
            overTimeRound = 7
            firstRoundTime = 11
            halfTimeRound = 4
            halfTimeTime = 20
            normalRoundTime = 20
        
        song_uri = self.convertUrlToUri(songLine[:songLine.find(" ")])

        # After what time to play the song
        playAfterTime = 0
        # At what time to start the song
        playIntoTime = 0
        if self.roundNumber == 1:
            # First round
            if songTime > firstRoundTime:
                playIntoTime = songTime - firstRoundTime
            else:
                playAfterTime = time.time() + firstRoundTime - songTime - wifiOffset
            print("firs " + str(firstRoundTime + (time.time() - playAfterTime)))
        elif self.roundNumber == halfTimeRound or self.roundNumber >= overTimeRound:
            # Half time or over time
            if songTime > halfTimeTime:
                playIntoTime = songTime - halfTimeTime
            else:
                playAfterTime = time.time() + halfTimeTime - songTime - wifiOffset
            print("half " + str(halfTimeTime + (time.time() - playAfterTime)))
        else:
            # Normal rounds
            if songTime > normalRoundTime:
                playIntoTime = songTime - normalRoundTime
            else:
                playAfterTime = time.time() + normalRoundTime - songTime - wifiOffset
            print("norm " + str(normalRoundTime + (time.time() - playAfterTime)))


        if (playIntoTime == 0):
            # Wait for play after time
            while time.time() < playAfterTime:
                if self.roundNumber == 1:
                    # First round
                    print("firs round " + str(firstRoundTime - (time.time() - roundStartTime)))
                elif self.roundNumber == halfTimeRound or self.roundNumber >= overTimeRound:
                    # Half time
                    print("half round " + str(halfTimeRound - (time.time() - roundStartTime)))
                else:
                    # Normal rounds
                    print("norm round " + str(normalRoundTime - (time.time() - roundStartTime)))

                time.sleep(0.05)
            # Play a song
            startTime = time.time()
            self.spotifyClient.start_playback(device_id = deviceId, uris = [song_uri])
        else:
            # Play a song at an offset
            startTime = time.time()
            self.spotifyClient.start_playback(device_id = deviceId, uris = [song_uri], position_ms = (playIntoTime - 0.67) * 1000)

        # Repeats the current track
        self.spotifyClient.repeat("track", device_id=deviceId)

        print("played")

        # Wait for playback to start
        while True:
            playback = self.spotifyClient.current_playback()
            if playback and playback["is_playing"]:
                break
            time.sleep(0.05)  # Check every 50ms

        # Stop timing
        endTime = time.time()
        delay = endTime - startTime
        print(delay)
        printTime = time.time() + songTime

        while time.time() < printTime:
            if self.roundNumber == 1:
                # First round
                print("firs round " + str(firstRoundTime - (time.time() - roundStartTime)))
            elif self.roundNumber == halfTimeRound or self.roundNumber >= overTimeRound:
                # Half time
                print("half round " + str(halfTimeRound - (time.time() - roundStartTime)))
            else:
                # Normal rounds
                print("norm round " + str(normalRoundTime - (time.time() - roundStartTime)))
            
            time.sleep(0.1)
        print("Time for beat drop, RIGHT?")
        print(normalRoundTime - (time.time() - roundStartTime))

        self.songNumber = self.songNumber + 1
        self.roundNumber = self.roundNumber + 1

    def makeHotKey(self):
        '''Creates the hotkey based on the config file'''
        settingsFile = open("Config\\settings", "r")
        fileLines = settingsFile.readlines()
        settingsFile.close()


        if fileLines[1].find("/,") != -1:
            # Finds the hotkeys
            hotkey1 = fileLines[1][0 : fileLines[1].find("/,")]
            hotkey2 = fileLines[1][fileLines[1].find("/,") + 2 :-1]
            # If add hotkey fails, return false
            try:
                keyboard.add_hotkey(hotkey1 + "+" + hotkey2, callback = self.hotKeyPressed)
                return True
            except (ValueError):
                return False
        else:
            try:
                keyboard.add_hotkey(fileLines[1][:-1], callback = self.hotKeyPressed)
                return True
            except ValueError:
                return False

    def isValidPlaylist(self):
        '''Returns if the URL on line 3 of the settings file is valid'''
        settingsFile = open("Config\\settings", "r")
        playlistURL = settingsFile.readlines()[3]
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

        songsFile = open("Config\\" + playlistFileName, "r")
        oldLines = songsFile.readlines()
        songsFile.close()

        oldSongs = []
        for line in oldLines:
            oldSongs.append(line[:line.find(" ")])
        
        # Creates a list of all the songs in the playlist
        
        # Reads the url from settings
        settingsFile = open("Config\\settings", "r")
        playlistURL = settingsFile.readlines()[3]
        settingsFile.close()

        # Creates a list of new songs
        tracks = self.spotifyClient.playlist_tracks(playlistURL)['items']

        # Extract track URLs
        newSongs = []
        for track in tracks:
            if track["track"]:
                newSongs.append(track["track"]["external_urls"]["spotify"])
    
        playlistFile = open("Config\\" + playlistFileName, "a")
        masterFile = open("Config\\masterSongFile", "r")

        uniqueSongs = []
        for newSong in newSongs:
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
        songNames = open("Config\\songNames", "r")
        songs = songNames.readlines()
        songNames.close()
        
        random.shuffle(songs)

        songNames = open("Config\\songNames", "w")
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
        '''Uses spotify's search to look for the 5 best songs'''
        return self.spotifyClient.search(q = name, type = "track", limit = 5)

    def deleteSongFile(self):
        '''Deleats the SongNames File'''
        #Deletes the current songNames file
        open('Config\\songNames', 'w').close()
    
    def removeHotkeys(self):
        '''Removes any hotkeys'''
        keyboard.remove_all_hotkeys()

    def resetRounds(self):
        '''Resets the rounds'''
        self.roundNumber = 1
    
    def setNextSong(self, set):
        '''Sets the next song'''
        self.nextSong = set