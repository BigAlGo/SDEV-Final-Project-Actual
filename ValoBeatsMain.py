import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import SpotifyInteractor as SI


def createSettingsWindow():
    '''Creates the settings window'''
    #cancel the hotkey
    spotifyIntern.removeHotkeys()

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
    settingImage = PhotoImage(file = "Images\\SettingsBG.gif")

    #adds the image to the canvas
    settingsCanvas.create_image(0, 0, image = settingImage, anchor = "nw")

    #adds text to the window
    settingsCanvas.create_text(320, 225, text = "Volume", font = ("Lucida Sans", 30), fill = "#d85965")
    settingsCanvas.create_text(960, 225, text = "HotKeys", font = ("Lucida Sans", 30), fill = "#2b4055")
    settingsCanvas.create_text(640, 270, text = "PlayList URL", font = ("Lucida Sans", 30), fill = "#c73d4c")

    #creates a scale, a button, and text entry to put on the canvas
    global volumeScale
    volumeScale = Scale(settingsWindow, from_ = 0, to_ = 100, orient = tk.HORIZONTAL, resolution = 1, bg = "#d85965", fg = "#2a3b52", highlightbackground = "#d1656c")
    
    settingsFile = open("Config\\settings", "r")
    fileLines = settingsFile.readlines()

    #sets the orginal volume to be the last volume
    volumeScale.set(int(fileLines[0][0:3]))

    #creates the entry fields for the hotkeys and playlist
    global hotKeyText1
    global hotKeyText2
    global playListLinkText
    hotKeyText1 = Entry(settingsWindow, bg = "#4f374d", fg = "#d1656c", highlightbackground = "#4f374d")
    hotKeyText2 = Entry(settingsWindow, bg = "#4f374d", fg = "#d1656c", highlightbackground = "#4f374d")
    playListLinkText = Entry(settingsWindow, bg = "#eb4454", fg = "#e8fbfb", highlightbackground = "#4f374d")
    
    #adds the preveious hotkeys to the entry fields
    if (fileLines[1].find("/,") != -1):
        #inserts from 0 to /,
        hotKeyText1.insert(0, fileLines[1][0 : fileLines[1].find("/,")])
        #inserts from /, to end
        hotKeyText2.insert(0, fileLines[1][fileLines[1].find("/,") + 2 : -1])
    else:
        hotKeyText1.insert(0, fileLines[1][:-1])

    playListLinkText.insert(0, fileLines[2])

    settingsFile.close()

    confirmButton = Button(settingsWindow, text = "Save", command = saveSettings, bg = "#4c9ba4")

    #adds the scale and button to the canvas
    volumeScaleWindow   = settingsCanvas.create_window(320, 300, window = volumeScale)

    confirmButtonWindow = settingsCanvas.create_window(640, 600, window = confirmButton)

    hotKeyText1Window = settingsCanvas.create_window(960, 285, window = hotKeyText1)
    hotKeyText2Window = settingsCanvas.create_window(960, 305, window = hotKeyText2)
    playListLinkWindow = settingsCanvas.create_window(640, 335, window = playListLinkText)

def saveSettings():
    '''opens the settings window to write to'''

    settingsFile = open("Config\\settings", "w")

    #writing volume in correct format
    if (volumeScale.get() < 10):
        settingsFile.write("00" + str(volumeScale.get()) + "\n")
    elif (volumeScale.get() < 100):
        settingsFile.write("0" + str(volumeScale.get()) + "\n")
    else:
        settingsFile.write(str(volumeScale.get()) + "\n")

    #If nothing entered
    if len(hotKeyText1.get()) == 0:
        messagebox.showwarning("WARNING", "Please enter a valid key into the first box")
        settingsFile.close()
        return

    #if nothing entered in 2nd box
    if len(hotKeyText2.get()) == 0:
        settingsFile.write(hotKeyText1.get() + "\n")
    else:
        settingsFile.write(hotKeyText1.get() + "/," + hotKeyText2.get() + "\n")

    settingsFile.write(playListLinkText.get())
    
    settingsFile.close()
    if (not spotifyIntern.makeHotKey()):
        if len(hotKeyText2.get()) == 0:
            messagebox.showwarning("WARNING", hotKeyText1.get() + " is not a valid hotkey, please try again")
        else:
            messagebox.showwarning("WARNING", hotKeyText1.get() + " or " + hotKeyText2.get() + " is not a valid hotkey, please try again")
        return
    

    #todo:
    if not spotifyIntern.isValidPlaylist():
        messagebox.showwarning("WARNING", playListLinkText.get() + " is not a valid playList name, please try again")
        return

    # Asks What time you want each new song to start at
    songFile = open("Config\\songNames", "a")
    for song in spotifyIntern.getPlaylistLinks():
        answer = simpledialog.askfloat("Song Timing", "What Time would you like the song " + spotifyIntern.getNameOfSong(song) + " to start at?")
        songFile.write("\n" + song + " " + str(answer))
    songFile.close

    #write first 3 lines
    #open song names in "a" mode
    #search through all links for the new link
    #if not found
    #   ask user for time
    #write to list
    #close
    settingsFile.close()


    settingsWindow.destroy()


def main():
    '''Main Function creates the main window'''

    '''Config file is formatted so that the 
    First line is the volume
    Second line is the hotkey
    Third line is the playlist url
    Then every line after that is all of the spotify songs that have been saved
    in the format: First word of the line is the url of a song
    and second word is the the offset timer'''
    global settingsFile

    #creates a spotify interactor
    global spotifyIntern
    spotifyIntern = SI.SpotifyInteractor()
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
    mainImage = PhotoImage(file = "Images\\ValorantMainBG.gif")

    #creates a canvas for the photo and text to be put on
    mainCanvas = Canvas(mainWindow, width = 640, height = 360)
    mainCanvas.pack(fill = "both", expand = True)

    #adds the image to the canvas
    mainCanvas.create_image(0, 0, image = mainImage, anchor = "nw")

    #creates a button
    settingsButton = Button(mainWindow, text = "Open Settings", command = createSettingsWindow)

    #adds the button to the canvas
    settingsButtonWindow = mainCanvas.create_window(320, 180, window = settingsButton)


    mainWindow.mainloop()



if __name__ == "__main__":
    main()
