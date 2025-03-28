import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import SpotifyInteractor as SI

#todo add a hotkey for turning the music down 
#todo when redoing song times, allow them to choose a certain song to remove

#todo add a separate window for hotkeys and add more hotkeys
def createSettingsWindow():
    '''Creates the settings window'''
    # Hides main window
    mainWindow.withdraw()

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
    settingsCanvas.create_text(960, 225, text = "HotKeys", font = ("Lucida Sans", 30), fill = "#72d8cc")
    settingsCanvas.create_text(640, 270, text = "PlayList URL", font = ("Lucida Sans", 30), fill = "#c73d4c")

    # Opens the settings file
    settingsFile = open("Config\\settings", "r")
    fileLines = settingsFile.readlines()

    # Creating the Radio Buttons
    normalRadio = tk.Radiobutton(settingsCanvas, text = "Unrated/Competitive", variable = radioGameType, value = "Normal", bg = "#4c9ba4", activebackground = "#000000", activeforeground = "#4c9ba4")
    swiftRadio = tk.Radiobutton(settingsCanvas, text = "Swift Play", variable = radioGameType, value = "Swift", bg = "#4c9ba4", activebackground = "#000000", activeforeground = "#4c9ba4")
    spikeRadio = tk.Radiobutton(settingsCanvas, text = "Spike Rush", variable = radioGameType, value = "Spike", bg = "#4c9ba4", activebackground = "#000000", activeforeground = "#4c9ba4")

    radioGameType.set(fileLines[2][:-1])

    # Creates a scale, a button, and text entry to put on the canvas
    global volumeScale
    volumeScale = Scale(settingsWindow, from_ = 0, to_ = 100, orient = tk.HORIZONTAL, resolution = 1, bg = "#d85965", troughcolor = "#4f374d", activebackground = "#d85965", highlightbackground = "#d1656c", highlightcolor= "#000000")
    

    # Sets the orginal volume to be the last volume
    volumeScale.set(int(fileLines[0][0:3]))

    # Creates the entry fields for the playlist
    global playListLinkText
    playListLinkText = Entry(settingsWindow, width = 30, justify = "center", bg = "#eb4454", fg = "#e8fbfb")
    
    # Adds previous playlist to the field
    playListLinkText.insert(0, fileLines[3])

    settingsFile.close()

    confirmButton = Button(settingsWindow, text = "Save", command = saveSettings, bg = "#4c9ba4", activebackground = "#000000", activeforeground = "#4c9ba4")
    reCreateButton = Button(settingsWindow, text = "Delete All Songs", command = remakeSongFile, bg = "#4c9ba4", activebackground = "#000000", activeforeground = "#4c9ba4")
    openHotkeyWindow = Button(settingsWindow, text = "Open Hotkey Window", command = createHotKeyWindow, bg = "#72d8cc", activebackground = "#000000", activeforeground = "#4c9ba4")

    # Adds everything to the canvas
    settingsCanvas.create_window(320, 300, window = volumeScale)

    settingsCanvas.create_window(1120, 470, window = normalRadio)
    settingsCanvas.create_window(1120, 500, window = swiftRadio)
    settingsCanvas.create_window(1120, 530, window = spikeRadio)

    settingsCanvas.create_window(640, 600, window = confirmButton)
    settingsCanvas.create_window(160, 500, window = reCreateButton)

    settingsCanvas.create_window(640, 335, window = playListLinkText)
    settingsCanvas.create_window(960, 285, window = openHotkeyWindow)

    settingsWindow.bind("<Destroy>", settingsDestroyed) 

def createHotKeyWindow():
    '''Creates the hotkey window'''
    global hotkeyWindow
    hotkeyWindow = tk.Toplevel()
    hotkeyWindow.title("Hot Keys")

    # Calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    # Creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 540/2))
    oHeight = str(int(height - 303/2 - 65))

    # Creates size of screen
    hotkeyWindow.geometry("540x303+" + oWidth + "+" + oHeight)

    hotkeyCanvas = Canvas(hotkeyWindow, width = 540, height = 303)
    hotkeyCanvas.pack(fill = "both", expand = True)

    # Gets photo from settings
    global hotkeyImage
    hotkeyImage = PhotoImage(file = "Images\\HotKeysImage.gif")

    # Adds the image to the canvas
    hotkeyCanvas.create_image(0, 0, image = hotkeyImage, anchor = "nw")
    hotkeyCanvas.create_text(255, 225, text = "TEST?", font = ("Lucida Sans", 30), fill = "#d85965")

    # Creates the entry fields for the hotkeys
    global hotKeyText1
    global hotKeyText2
    hotKeyText1 = Entry(settingsWindow, justify = "center", bg = "#4f374d", fg = "#d1656c")
    hotKeyText2 = Entry(settingsWindow, justify = "center", bg = "#4f374d", fg = "#d1656c")

    # Opens the settings file
    settingsFile = open("Config\\settings", "r")
    fileLines = settingsFile.readlines()
    settingsFile.close()

    # Adds the preveious hotkeys to the entry fields
    if fileLines[1].find("/,") != -1:
        #inserts from 0 to /,
        hotKeyText1.insert(0, fileLines[1][0 : fileLines[1].find("/,")])
        #inserts from /, to end
        hotKeyText2.insert(0, fileLines[1][fileLines[1].find("/,") + 2 : -1])
    else:
        hotKeyText1.insert(0, fileLines[1][:-1])

    
    # Adding the elements
    hotkeyCanvas.create_window(250, 250, window = hotKeyText1)
    hotkeyCanvas.create_window(250, 300, window = hotKeyText2)


def settingsDestroyed(event):
    '''When the settings window is manually closed and they didnt click save, 
    reopen the main window and remake the hotkeys'''
    mainWindow.deiconify()
    spotifyIntern.makeHotKey()


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
    
    # End writing the settings
    settingsFile.close()

    if not spotifyIntern.makeHotKey():
        if len(hotKeyText2.get()) == 0:
            messagebox.showwarning("WARNING", hotKeyText1.get() + " is not a valid hotkey, please try again")
        else:
            messagebox.showwarning("WARNING", hotKeyText1.get() + " or " + hotKeyText2.get() + " is not a valid hotkey, please try again")
        return
    

    if not spotifyIntern.isValidPlaylist():
        messagebox.showwarning("WARNING", playListLinkText.get() + " is not a valid public playList link, please try again")
        return

    # Checking if a device is open
    devices = spotifyIntern.getDevices()
    if not devices['devices']:
        messagebox.showwarning("No Devices", "No active devices found. Open Spotify on a device signed into your account and try again.")
        return

    masterSongFile = open("Songs\\masterSongFile", "a")

    # Createing new playlist Song File
    fileName = spotifyIntern.playlistURLToFileName(playListLinkText.get())
    playlistSongFile = open("Songs\\" + fileName, "a")
    
    # Asks how you want to input the songs
    uniqueSongs = spotifyIntern.getPlaylistLinks(fileName)
    if len(uniqueSongs) != 0:
        howAnswer = messagebox.askyesnocancel("Song Timing", "Would you like to use your spotify in your browser set the timing for all the songs?")

    # Asks What time you want each new song to start at
    for song in uniqueSongs:
        if howAnswer == True:
            # Using browser data
            correct = False
            while True:
                # Loops until we get correct input
                messagebox.showinfo("Song Timing", "Please go to the time at which you want the song " + spotifyIntern.getNameOfSong(song) + " to start on a device and then click OK")
                time = spotifyIntern.getSongTime()
                if (time != -1):
                    correct = messagebox.askyesnocancel("Song Timeing", "The time you entered is " + str(time) + ". Is this correct?")
                    if (correct == None or correct == True):
                        break
            if correct != None:
                # Only add the song if they didn't press cancel
                masterSongFile.write(song + " " + str(time) + "\n")
                playlistSongFile.write(song + " " + str(time) + "\n")

        elif howAnswer ==  False:
            # Using manual input
            timeAnswer = simpledialog.askfloat("Song Timing", "What time would you like the song " + spotifyIntern.getNameOfSong(song) + " to start at?")
            if timeAnswer != None:
                masterSongFile.write(song + " " + str(timeAnswer) + "\n")
                playlistSongFile.write(song + " " + str(time) + "\n")

    masterSongFile.close()

    mainWindow.deiconify()

    settingsWindow.destroy()

def addSongNext():
    '''Uses Spotify's search to look through the main file for the song requested, then adds that song to play next'''
    songsFile = open("Songs\\masterSongFile", "r")
    masterLines = songsFile.readlines()

    masterSongs = []
    for line in masterLines:
        masterSongs.append(line[:line.find(" ")])
    found = False
    # Searching for the 
    for track in spotifyIntern.searchForBestSong(nextSongText.get())["tracks"]["items"]:
        for masterSong in masterSongs:
            if track["external_urls"]["spotify"] == masterSong:
                # Found in master songs, refind the whole line, then add to playlist file
                for masterLine in masterLines:
                    if masterLine.find(track["external_urls"]["spotify"]) != -1:
                        newLine = masterLine
                        found = True
                        break
                if found:
                    break
        if found:
            break
    if found:
        spotifyIntern.setNextSong(newLine)
        nextSongText.delete(0, "end")
    else:
        messagebox.showinfo("Search", "No saved song was found using the query: \"" + nextSongText.get() + "\". try narrowing it down by searching with the author as well")

def remakeSongFile():
    answer = messagebox.askquestion("Confirmation", "Are you sure you want to DELETE ALL saved songs and redo the Song Timing for all the songs in the current playlist?")
    if (answer == "yes"):
        spotifyIntern.deleteSongFile()


def main():
    '''Main Function creates the main window'''
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
    # mainWindow.overrideredirect(1) # If I dont want a window boarder, but it also doent make a moveable window 

    # For later
    global radioGameType
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

    # Stores the next song
    global nextSongText

    # Creates buttons

    backGround = "#0f1922"
    foreGround = "#fe4357"

    activebackground = "#fe4357"
    activeforeground = "#0f1922"
    boarderWidth = 0,

    shuffleButton   = Button(mainWindow, text = "Shuffle songs", width = 12, bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = spotifyIntern.shuffleSongs)
    resetRoundsButton = Button(mainWindow, text = "Finish Game", width = 12, bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = spotifyIntern.resetRounds)

    searchButton = Button(mainWindow, text = "Add Next Song To Play", width = 18, bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = addSongNext)
    nextSongText = Entry(mainWindow, justify = "center", width = 22, bg = foreGround, fg = backGround)

    settingsButton = Button(mainWindow, text = "Open Settings", bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = createSettingsWindow)

    # Adds each element to the canvas

    mainCanvas.create_window(80, 50, window = shuffleButton)
    mainCanvas.create_window(80, 75, window = resetRoundsButton)

    mainCanvas.create_window(500, 105, window = searchButton)
    mainCanvas.create_window(500, 126, window = nextSongText)

    mainCanvas.create_window(450, 300, window = settingsButton)

    # Wait for input
    mainWindow.mainloop()

if __name__ == "__main__":
    main()
