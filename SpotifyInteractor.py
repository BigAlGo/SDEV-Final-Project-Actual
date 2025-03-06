import keyboard

class SpotifyInteractor():
    def __init__(self):
        '''Config file is formatted so that the 
        First line is the volume
        Second line is the hotkey
        Third line is the playlist url
        Then every line after that is all of the spotify songs that have been saved
        in the format: First word of the line is the url of a song
        and second word is the the offset timer'''
        self.settingsFile = open("Config", "r")
        keyboard.add_hotkey("p", self.hotKeyPressed)
        keyboard.remove_all_hotkeys()
  
    
    def hotKeyPressed(self):
        '''Do the things with spotipy'''
        print("hello world")

    def redoHotKey(self):
        '''Recreates the hotkey based on the config file'''
        settingsFile = open("Config", "r")
        keys = settingsFile.readline(2)
        if "/," in keys:
            print("yes")
        else:
            print("no")
        settingsFile.close()

    

