from breezypythongui import EasyFrame
from tkinter import PhotoImage
from tkinter import Tk

class MainWindow(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title = "Valo Beats")

        self.setSize(426,118)
        
        imagePath = PhotoImage(file = "C:\\Users\\brownall1\Desktop\\SDEV Final Project\\ValorantBG.gif")

        bgImage = self.addCanvas(self,canvas = imagePath)
        self.TK
        bgImage.place()

        self.addButton("Text 1", 0, 0, command = lambda : showWindow2(self))
        self.scale = self.addScale(row = 1, column = 0, from_ = 0, to = 100, resolution = 1)
        self.scale.set(50)
        
class SecondWindow(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title = "Valo Beats 2 electrik bogalooooo")

        self.addLabel("hello world 2 electrik bogalooooo", 0, 0)
    
def showWindow2(self):
    print(self.scale.get())
    quit(self)
    SecondWindow.mainloop()

def main():
    MainWindow().mainloop()

if __name__ == "__main__":
    main()