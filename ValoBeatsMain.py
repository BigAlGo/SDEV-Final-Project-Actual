import tkinter as tk
from tkinter import *
import SpotifyInteractor as SI


def createSettingsWindow():
    '''Creates the settings window'''
    #creates settings window
    global settingsWindow
    settingsWindow = tk.Toplevel()
    settingsWindow.title("Settings")
    
    #calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    #creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 1280/2))
    oHeight = str(int(height - 700/2 - 65))

    #creates size of screen
    settingsWindow.geometry("1280x700+" + oWidth + "+" + oHeight)

    #creates a canvas for the photo and text to be put on
    settingsCanvas = Canvas(settingsWindow, width = 1280, height = 700)
    settingsCanvas.pack(fill = "both", expand = True)

    #gets photo for settings
    global settingImage
    settingImage = PhotoImage(file = "SettingsBG.gif")

    #adds the image to the canvas
    settingsCanvas.create_image(0, 0, image = settingImage, anchor = "nw")

    #adds text to the window
    settingsCanvas.create_text(640, 200, text = "Volume", font = ("Lucida Sans", 30), fill = "#132a4f")

    #creates a scale and a button to put on the canvas
    volumeScale = Scale(settingsWindow, from_ = 0, to_ = 100, orient=tk.HORIZONTAL, resolution = 1)
    confirmButton = Button(settingsWindow, text = "Save", command = closeSettingsWindow)

    #adds the scale and button to the canvas
    volumeScaleWindow   = settingsCanvas.create_window(640, 300, window = volumeScale)
    confirmButtonWindow = settingsCanvas.create_window(640, 600, window = confirmButton)

def closeSettingsWindow():
    '''Closes the settings window'''
    settingsWindow.destroy()

def main():
    #creates a spotify interactor
    global spotifyInter
    spotifyInter = SI.SpotifyInteractor()
    #creates main window
    global mainWindow
    mainWindow = tk.Tk()

    #calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    #creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 640/2))
    oHeight = str(int(height - 360/2 - 30))

    #creates screen and size
    mainWindow.title("Main Screen")
    mainWindow.geometry("640x360" + "+" + oWidth + "+" + oHeight)

    #gets photo for main
    mainImage = PhotoImage(file = "ValorantMainBG.gif")

    #creates a canvas for the photo and text to be put on
    mainCanvas = Canvas(mainWindow, width = 640, height = 360)
    mainCanvas.pack(fill = "both", expand = True)

    #adds the image to the canvas
    mainCanvas.create_image(0, 0, image = mainImage, anchor = "nw")

    #creates a button
    settingsButton = Button(mainWindow, text = "Open Settings", command = createSettingsWindow)

    #adds the button to the canvas
    settingsButtonWindow = mainCanvas.create_window(320, 180, window = settingsButton)

    spotifyInter.createHotKey()
    mainWindow.mainloop()



if __name__ == "__main__":
    main()
