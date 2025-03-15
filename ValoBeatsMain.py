import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import SpotifyInteractor as SI

#todo fix the bug of a single line being created at the start of the song names file after clicking clear songs
#todo add a song name input to be able to switch between songs 
#todo change the while loop to be an offset in the playback function
#todo add the ability to save different songNames files
#todo add overtime support
def createSettingsWindow():
    '''Creates the settings window'''
    # Cancel the hotkey
    spotifyIntern.removeHotkeys()

    # Creates settings window
    global settingsWindow
    settingsWindow = tk.Toplevel()
    settingsWindow.title("Settings")
    
    # Calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    # Creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 1280/2))
    oHeight = str(int(height - 700/2 - 65))

    # Creates size of screen
    settingsWindow.geometry("1280x700+" + oWidth + "+" + oHeight)

    # Creates a canvas for the photo and text to be put on
    settingsCanvas = Canvas(settingsWindow, width = 1280, height = 700)
    settingsCanvas.pack(fill = "both", expand = True)

    # Gets photo for settings
    global settingImage
    settingImage = PhotoImage(file = "Images\\SettingsBG.gif")

    # Adds the image to the canvas
    settingsCanvas.create_image(0, 0, image = settingImage, anchor = "nw")

    # Adds text to the window
    settingsCanvas.create_text(320, 225, text = "Volume", font = ("Lucida Sans", 30), fill = "#d85965")
    settingsCanvas.create_text(960, 225, text = "HotKeys", font = ("Lucida Sans", 30), fill = "#2b4055")
    settingsCanvas.create_text(640, 270, text = "PlayList URL", font = ("Lucida Sans", 30), fill = "#c73d4c")

    # Opens the settings file
    settingsFile = open("Config\\settings", "r")
    fileLines = settingsFile.readlines()

    # Creating the Radio Buttons
    normalRadio = tk.Radiobutton(settingsCanvas, text = "Unrated/Competitive", variable = radioGameType, value = "Normal", bg = "#4c9ba4")
    swiftRadio = tk.Radiobutton(settingsCanvas, text = "Swift Play", variable = radioGameType, value = "Swift", bg = "#4c9ba4")
    spikeRadio = tk.Radiobutton(settingsCanvas, text = "Spike Rush", variable = radioGameType, value = "Spike", bg = "#4c9ba4")

    radioGameType.set(fileLines[2][:-1])

    # Creates a scale, a button, and text entry to put on the canvas
    global volumeScale
    volumeScale = Scale(settingsWindow, from_ = 0, to_ = 100, orient = tk.HORIZONTAL, resolution = 1, bg = "#d85965", fg = "#2a3b52", highlightbackground = "#d1656c")
    

    # Sets the orginal volume to be the last volume
    volumeScale.set(int(fileLines[0][0:3]))

    # Creates the entry fields for the hotkeys and playlist
    global hotKeyText1
    global hotKeyText2
    global playListLinkText
    hotKeyText1 = Entry(settingsWindow, bg = "#4f374d", fg = "#d1656c", highlightbackground = "#4f374d")
    hotKeyText2 = Entry(settingsWindow, bg = "#4f374d", fg = "#d1656c", highlightbackground = "#4f374d")
    playListLinkText = Entry(settingsWindow, bg = "#eb4454", fg = "#e8fbfb", highlightbackground = "#4f374d")
    
    # Adds the preveious hotkeys to the entry fields
    if (fileLines[1].find("/,") != -1):
        #inserts from 0 to /,
        hotKeyText1.insert(0, fileLines[1][0 : fileLines[1].find("/,")])
        #inserts from /, to end
        hotKeyText2.insert(0, fileLines[1][fileLines[1].find("/,") + 2 : -1])
    else:
        hotKeyText1.insert(0, fileLines[1][:-1])

    playListLinkText.insert(0, fileLines[3])

    settingsFile.close()

    confirmButton = Button(settingsWindow, text = "Save", command = saveSettings, bg = "#4c9ba4")
    reCreateButton = Button(settingsWindow, text = "Delete All Songs", command = remakeSongFile, bg = "#4c9ba4")

    # Adds everything to the canvas
    settingsCanvas.create_window(320, 300, window = volumeScale)

    settingsCanvas.create_window(1120, 470, window = normalRadio)
    settingsCanvas.create_window(1120, 500, window = swiftRadio)
    settingsCanvas.create_window(1120, 530, window = spikeRadio)

    settingsCanvas.create_window(640, 600, window = confirmButton)
    settingsCanvas.create_window(160, 500, window = reCreateButton)

    settingsCanvas.create_window(960, 285, window = hotKeyText1)
    settingsCanvas.create_window(960, 305, window = hotKeyText2)
    settingsCanvas.create_window(640, 335, window = playListLinkText)

def saveSettings():
    '''opens the settings window to write to'''

    settingsFile = open("Config\\settings", "w")

    # Writing volume in correct format
    if (volumeScale.get() < 10):
        settingsFile.write("00" + str(volumeScale.get()) + "\n")
    elif (volumeScale.get() < 100):
        settingsFile.write("0" + str(volumeScale.get()) + "\n")
    else:
        settingsFile.write(str(volumeScale.get()) + "\n")

    # If nothing entered
    if len(hotKeyText1.get()) == 0:
        messagebox.showwarning("WARNING", "Please enter a valid key into the first box")
        settingsFile.close()
        return

    # If nothing entered in 2nd box
    if len(hotKeyText2.get()) == 0:
        settingsFile.write(hotKeyText1.get() + "\n")
    else:
        settingsFile.write(hotKeyText1.get() + "/," + hotKeyText2.get() + "\n")

    # Write the game type
    settingsFile.write(radioGameType.get() + "\n")

    # Write the playlist link
    settingsFile.write(playListLinkText.get())
    
    settingsFile.close()
    if (not spotifyIntern.makeHotKey()):
        if len(hotKeyText2.get()) == 0:
            messagebox.showwarning("WARNING", hotKeyText1.get() + " is not a valid hotkey, please try again")
        else:
            messagebox.showwarning("WARNING", hotKeyText1.get() + " or " + hotKeyText2.get() + " is not a valid hotkey, please try again")
        return
    

    if not spotifyIntern.isValidPlaylist():
        messagebox.showwarning("WARNING", playListLinkText.get() + " is not a valid playList name, please try again")
        return

    # Asks What time you want each new song to start at
    songFile = open("Config\\songNames", "a")
    for song in spotifyIntern.getPlaylistLinks():
        answer = simpledialog.askfloat("Song Timing", "What time would you like the song " + spotifyIntern.getNameOfSong(song) + " to start at?")
        if answer != None:
            songFile.write("\n" + song + " " + str(answer))
    
    songFile.close()


    # Checking if a device is open
    devices = spotifyIntern.getDevices()
    if not devices['devices']:
        messagebox.showwarning("No Devices", "No active devices found. Open Spotify on a device signed into your account and try again.")
        return

    settingsWindow.destroy()

def remakeSongFile():
    answer = messagebox.askquestion("Confirmation", "Are you sure you want to DELETE ALL saved songs and redo the Song Timing for all the songs in the current playlist?")
    if (answer == "yes"):
        spotifyIntern.deleteSongFile()


def main():
    '''Main Function creates the main window'''
    # For later
    global radioGameType
    '''Config file is formatted so that the 
    First line is the volume
    Second line is the hotkey
    Third line is the type of game 
    Forth line is the playlist url
    '''

    # Creates a spotify intern
    global spotifyIntern
    spotifyIntern = SI.SpotifyInteractor()
    # Creates main window
    global mainWindow
    mainWindow = tk.Tk()
    # For later
    radioGameType = tk.StringVar()


    # Calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    # Creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 640/2))
    oHeight = str(int(height - 360/2 - 30))

    # Creates screen and size
    mainWindow.title("Main Screen")
    mainWindow.geometry("640x360" + "+" + oWidth + "+" + oHeight)

    # Gets photo for main
    mainImage = PhotoImage(file = "Images\\ValorantMainBG.gif")

    # Creates a canvas for the photo and text to be put on
    mainCanvas = Canvas(mainWindow, width = 640, height = 360)
    mainCanvas.pack(fill = "both", expand = True)

    # Adds the image to the canvas
    mainCanvas.create_image(0, 0, image = mainImage, anchor = "nw")

    # Creates a button
    settingsButton = Button(mainWindow, text = "Open Settings", command = createSettingsWindow)
    shuffleButton = Button(mainWindow, text = "Shuffle songs", command = spotifyIntern.shuffleSongs)

    # Adds the button to the canvas
    settingsButtonWindow = mainCanvas.create_window(320, 200, window = settingsButton)
    shuffleButtonWindow = mainCanvas.create_window(220, 180, window = shuffleButton)

    # Wait for input
    mainWindow.mainloop()



if __name__ == "__main__":
    main()
