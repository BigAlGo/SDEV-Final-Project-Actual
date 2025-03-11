import keyboard

class SpotifyInteractor():
    def __init__(self):
        self.makeHotKey()
        self.songNumber = 0
  
    def removeHotkeys(self):
        '''Removes any hotkeys'''
        keyboard.remove_all_hotkeys()

    def hotKeyPressed(self):
        print("Hot key Pressed")

    def makeHotKey(self):
        '''Recreates the hotkey based on the config file'''
        settingsFile = open("Config\\settings", "r")
        fileLines = settingsFile.readlines()
        settingsFile.close()


        if (fileLines[1].find("/,") != -1):
            #Finds the hotkeys
            hotkey1 = fileLines[1][0 : fileLines[1].find("/,")]
            hotkey2 = fileLines[1][fileLines[1].find("/,") + 2 :-1]
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
    

