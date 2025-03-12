import keyboard
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyInteractor():
    def __init__(self):
        self.makeHotKey()
        self.songNumber = 0

        #Initing spotify
        auth_manager = SpotifyClientCredentials(client_id = "35661866380c4cdcb93e51cc756ee958",
                                        client_secret = "7b316369507444e59e11722d4e49d1c8")
        self.spotify = spotipy.Spotify(auth_manager = auth_manager)

  
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
            #Finds the hotkeys
            hotkey1 = fileLines[1][0 : fileLines[1].find("/,")]
            hotkey2 = fileLines[1][fileLines[1].find("/,") + 2 :-1]
            #If add hotkey fails, return false
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
        # Todo: make this work
        # return self.spotify.track(url).__str__()
        return url


    def isValidPlaylist(self):
        '''Returns if the URL on line 3 of the settings file is valid'''
        settingsFile = open("Config\\settings", "r")
        playlistURL = settingsFile.readlines()[2]
        #todo check if this is a valid playlist using 
        # try:
            # self.spotify.playlist(playlistURL)
            # return True
        # except ?:
            # return False
        settingsFile.close()
        print(playlistURL)
        return True

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
        
        # Todo use spotify instesd of reading the values from the file
        # newLines = self.spotify.playlist_items()
        songsFile = open("Config\\SongsInPlayListTemp", "r")
        newLines = songsFile.readlines()
        songsFile.close()

        newSongs = []
        for line in newLines:
            if line.find("\n") != -1:
                newSongs.append(line[:-1])
            else:
                newSongs.append(line)
        
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

