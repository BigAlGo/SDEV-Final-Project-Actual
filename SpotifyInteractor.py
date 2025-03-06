import keyboard

class SpotifyInteractor():
    def __init__(self):
        '''does nothing'''

    def createHotKey(self):
        keyboard.add_hotkey("p", self.hotKeyPressed)
        
    def hotKeyPressed(self):
        print("hello world")
