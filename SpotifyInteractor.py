import keyboard
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import time
import random
from tkinter import messagebox



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
        # self.devices = self.spotifyClient.devices()
        # while not self.devices['devices']:
            # messagebox.showwarning("No Devices", "No active devices found. Open Spotify on a device signed into your account and try again.")

    def hotKeyPressed(self):
        '''Plays a song after a specified time'''
        print("hot key pressed")
        #Gets the current device
        active_device_id = self.devices['devices'][0]['id']

        songNameFile = open("Config\\songNames", "r")
        songLine = songNameFile.readlines()[self.songNumber]

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
        wifiOffset = 0.5
        if gameType == "Normal":
            firstRoundTime = 31
            halfTimeRound = 13
            halfTimeTime = 45
            normalRoundTime = 30
        elif gameType == "Swift":
            firstRoundTime = 31
            halfTimeRound = 5
            halfTimeTime = 45
            normalRoundTime = 30
        elif gameType == "Spike":
            # todo fix these numbers
            firstRoundTime = 19.5
            halfTimeRound = 4
            halfTimeTime = 19.7
            normalRoundTime = 19.5
        
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
        elif self.roundNumber == halfTimeRound:
            # Half time
            if songTime > halfTimeTime:
                playIntoTime = songTime - halfTimeTime
            else:
                playAfterTime = time.time() + halfTimeTime - songTime - wifiOffset
        else:
            # Normal rounds
            if songTime > normalRoundTime:
                playIntoTime = songTime - normalRoundTime
            else:
                playAfterTime = time.time() + normalRoundTime - songTime - wifiOffset


        if (playIntoTime == 0):
            # Wait for play after time

            while time.time() < playAfterTime:
                time.sleep(0.02)
            # Play a song
            self.spotifyClient.start_playback(device_id = active_device_id, uris = [song_uri])
        else:
            # Play a song at an offset
            self.spotifyClient.start_playback(device_id = active_device_id, uris = [song_uri], position_ms = (playIntoTime - 0.67) * 1000 )

        self.songNumber = self.songNumber + 1
        self.roundNumber = self.roundNumber + 1
        print("played")

        

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

    def getPlaylistLinks(self):
        '''Returns a list of lings to songs that have not been saved but are in the playlist'''        
        
        # Creates a list of all the saved songs 
        songsFile = open("Config\\songNames", "r")
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
    
        
        uniqueSongs = []
        # Looks through all the new songs and see if it already exists in the old songs
        for newSong in newSongs:
            found = False
            for oldSong in oldSongs:
                if newSong == oldSong:
                    found = True
                    break
            # If new song is not found in old songs, add it to uniqueSongs
            if not found:
                uniqueSongs.append(newSong)

        return uniqueSongs

    def shuffleSongs(self):
        '''TODO? make this shuffle the songs in songNames'''
        songNames = open("Config\\songNames", "r")
        songs = songNames.readlines()
        songNames.close()
        
        random.shuffle(songs)

        songNames = open("Config\\songNames", "w")
        songNames.writelines(songs)
        songNames.close()

    def convertUrlToUri(self, spotify_url):
        """Extracts track ID from a Spotify URL and converts it into a Spotify URI."""
        if "track/" in spotify_url:
            track_id = spotify_url.split("track/")[1].split("?")[0]
            return "spotify:track:" + track_id
        return None


    def getDevices(self):
        '''Gets the divices signed into the account'''
        self.devices = self.spotifyClient.devices()
        return self.devices
    
    def getNameOfSong(self, url):
        '''Returns the name of a song given the url'''
        return self.spotifyClient.track(url)['name']

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
