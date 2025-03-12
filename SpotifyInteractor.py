import keyboard
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth



class SpotifyInteractor():
    def __init__(self):
        self.makeHotKey()
        self.songNumber = 0

        #Initing spotify
        authManagerGeneral = SpotifyClientCredentials(client_id = "35661866380c4cdcb93e51cc756ee958",
                                        client_secret = "7b316369507444e59e11722d4e49d1c8",)
        self.spotifyGeneral = spotipy.Spotify(auth_manager = authManagerGeneral)


        authManagerClient = SpotifyOAuth(
            client_id="35661866380c4cdcb93e51cc756ee958",
            client_secret="7b316369507444e59e11722d4e49d1c8",
            redirect_uri="http://localhost:1234",
            scope="user-read-playback-state"
        )
        self.spotifyClient = spotipy.Spotify(auth_manager = authManagerClient)

  
    def removeHotkeys(self):
        '''Removes any hotkeys'''
        keyboard.remove_all_hotkeys()

    def hotKeyPressed(self):
        print("Hot key Pressed")

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
            
    def getNameOfSong(self, url):
        '''Returns the name of a song given the url'''
        devices = self.spotifyClient.devices()

        if devices["devices"]:
            for device in devices["devices"]:
                print(f"Device Name: {device['name']}, Type: {device['type']}, ID: {device['id']}")
        else:
            print("No active devices found. Open Spotify and start playing something!")

        
        return self.spotifyGeneral.track(url)['name']

    def isValidPlaylist(self):
        '''Returns if the URL on line 3 of the settings file is valid'''
        settingsFile = open("Config\\settings", "r")
        playlistURL = settingsFile.readlines()[2]
        settingsFile.close()

        # Tries to fetch the playlist
        try:
            self.spotifyGeneral.playlist(playlistURL)
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
        playlistURL = settingsFile.readlines()[2]
        settingsFile.close()

        # Creates a list of new songs
        tracks = self.spotifyGeneral.playlist_tracks(playlistURL)['items']

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

