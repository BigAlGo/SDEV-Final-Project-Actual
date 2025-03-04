import tkinter as tk
from tkinter import *

#creating settings window
def createSettingsWindow():
    global settingsWindow
    settingsWindow = tk.Toplevel()
    settingsWindow.title("Settings")
    
    #calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    #creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 1280/2))
    oHeight = str(int(height - 700/2 - 65))

    settingsWindow.geometry("1280x700+" + oWidth + "+" + oHeight)

    settingsCanvas = Canvas(settingsWindow, width = 1280, height = 700)
    settingsCanvas.pack(fill = "both", expand = True)

    global settingImage
    settingImage = PhotoImage(file = "SettingsBG.gif")

    settingsCanvas.create_image(0, 0, image = settingImage, anchor = "nw")

    settingsCanvas.create_text(640, 200, text = "Volume", font = ("Lucida Sans", 30), fill = "#132a4f")

    volumeScale = Scale(settingsWindow, from_ = 0, to_ = 100, orient=tk.HORIZONTAL, resolution = 1)
    confirmButton = Button(settingsWindow, text = "Save", command = closeSettingsWindow)

    volumeScaleWindow   = settingsCanvas.create_window(640, 300, window = volumeScale)
    confirmButtonWindow = settingsCanvas.create_window(640, 600, window = confirmButton)

def closeSettingsWindow():
    settingsWindow.destroy()

def main():
    global mainWindow
    mainWindow = tk.Tk()

    #calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    #creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 640/2))
    oHeight = str(int(height - 360/2 - 30))

    mainWindow.title("Main Screen")
    mainWindow.geometry("640x360" + "+" + oWidth + "+" + oHeight)

    mainImage = PhotoImage(file = "ValorantMainBG.gif")

    mainCanvas = Canvas(mainWindow, width = 640, height = 360)
    mainCanvas.pack(fill = "both", expand = True)

    mainCanvas.create_image(0, 0, image = mainImage, anchor = "nw")

    settingsButton = Button(mainWindow, text = "Open Settings", command = createSettingsWindow)

    settingsButtonWindow = mainCanvas.create_window(320, 180, window = settingsButton)

    mainWindow.mainloop()

main()
