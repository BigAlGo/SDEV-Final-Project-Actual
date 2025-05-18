import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import SpotifyInteractor as SI

import keyboard
import threading
import time
import os

# remake all songs in a playlist
# remake all master songs
# add a loading bar to downloading songs

# pause doeent work
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
    settingsWindow.iconbitmap("Images\\ValoBeatsLogo.ico")
    
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

    # Colors
    darkRed =  "#5c1314"
    lightRed = "#831f1f"
    onColor = "#f52740"
    offColor = "#000000"
    
    # Adds text to the window
    settingsCanvas.create_text(640, 300, text = "Volume", font = ("Lucida Sans", 30), fill = offColor)
    settingsCanvas.create_text(640, 200, text = "PlayList URL", font = ("Lucida Sans", 30), fill = offColor)

    # Opens the settings file
    settingsFile = open("Config\\settings", "r")
    fileLines = settingsFile.readlines()

    # Creating the Radio Buttons
    normalRadio = tk.Radiobutton(settingsCanvas, text = "Unrated/Competitive", variable = radioGameType, value = "Normal", selectcolor = lightRed, fg = offColor,  bg = lightRed, activebackground = "#000000", activeforeground = lightRed)
    swiftRadio  = tk.Radiobutton(settingsCanvas, text = "Swift Play", variable = radioGameType, value = "Swift", selectcolor = lightRed, fg = offColor, bg = lightRed, activebackground = "#000000", activeforeground = lightRed)
    spikeRadio  = tk.Radiobutton(settingsCanvas, text = "Spike Rush", variable = radioGameType, value = "Spike", selectcolor = lightRed, fg = offColor, bg = lightRed, activebackground = "#000000", activeforeground = lightRed)

    radioGameType.set(fileLines[1][:-1])

    # Creates a scale, a button, and text entry to put on the canvas
    global loudVolumeScale
    global quietVolumeScale
    loudVolumeScale  = Scale(settingsWindow, from_ = 0, to_ = 100, orient = tk.HORIZONTAL, resolution = 1, fg = offColor, bg = lightRed, troughcolor = darkRed, activebackground = lightRed, highlightbackground = lightRed, highlightcolor = offColor)
    quietVolumeScale = Scale(settingsWindow, from_ = 0, to_ = 100, orient = tk.HORIZONTAL, resolution = 1, fg = offColor, bg = lightRed, troughcolor = darkRed, activebackground = lightRed, highlightbackground = lightRed, highlightcolor = offColor)

    # Sets the orginal volume to be the last volume
    loudVolumeScale.set(int(fileLines[0][0:3]))
    quietVolumeScale.set(int(fileLines[0][3:6]))

    # Creates the entry fields for the playlist
    global playListLinkText
    playListLinkText = Entry(settingsWindow, width = 90, justify = "center", bg = lightRed, fg = offColor)
    
    # Adds previous playlist to the field
    playListLinkText.insert(0, fileLines[2][:-1])

    settingsFile.close()

    confirmButton    = Button(settingsWindow, text = "Save", command = saveSettings, fg = offColor, bg = lightRed, activebackground = "#000000", activeforeground = lightRed)
    openRemakeWindow = Button(settingsWindow, text = "Open Remake Window", command = createRemakeWindow, fg = offColor, bg = lightRed, activebackground = "#000000", activeforeground = lightRed)
    openHotkeyWindow = Button(settingsWindow, text = "Open Hotkey Window", command = createHotKeyWindow, fg = offColor, bg = lightRed, activebackground = "#000000", activeforeground = lightRed)

    # Adds everything to the canvas
    settingsCanvas.create_window(640, 250, window = playListLinkText)

    settingsCanvas.create_window(580, 350, window = loudVolumeScale)
    settingsCanvas.create_window(700, 350, window = quietVolumeScale)

    settingsCanvas.create_window(640, 400, window = normalRadio)
    settingsCanvas.create_window(600, 430, window = swiftRadio)
    settingsCanvas.create_window(680, 430, window = spikeRadio)

    settingsCanvas.create_window(572, 500, window = openRemakeWindow)
    settingsCanvas.create_window(708, 500, window = openHotkeyWindow)

    settingsCanvas.create_window(640, 600, window = confirmButton)

    settingsWindow.bind("<Destroy>", settingsDestroyed) 

def createHotKeyWindow():
    '''Creates the hotkey window'''
    global hotkeyWindow
    hotkeyWindow = tk.Toplevel()
    hotkeyWindow.title("Hot Keys")
    hotkeyWindow.iconbitmap("Images\\ValoBeatsLogo.ico")

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
    hotkeyImage = PhotoImage(file = "Images\\HotkeyWindowBG.gif")

    # Adds the image to the canvas
    hotkeyCanvas.create_image(0, 0, image = hotkeyImage, anchor = "nw")

    global playKeyText
    global endKeyText
    global pauseKeyText
    global lowKeyText
    global highKeyText

    # Creates the entry fields for the hotkeys    
    playKeyText =  Entry(hotkeyWindow, justify = "center", width = 10, bg = "#000000", fg = "#f57e3a")
    endKeyText =   Entry(hotkeyWindow, justify = "center", width = 10, bg = "#000000", fg = "#f57e3a")
    pauseKeyText = Entry(hotkeyWindow, justify = "center", width = 10, bg = "#000000", fg = "#f57e3a")
    lowKeyText =   Entry(hotkeyWindow, justify = "center", width = 10, bg = "#000000", fg = "#f57e3a")
    highKeyText =  Entry(hotkeyWindow, justify = "center", width = 10, bg = "#000000", fg = "#f57e3a")

    playKeyText .bind("<Button-1>", spotifyIntern.hotKeyEntryClicked)
    endKeyText  .bind("<Button-1>", spotifyIntern.hotKeyEntryClicked)
    pauseKeyText.bind("<Button-1>", spotifyIntern.hotKeyEntryClicked)
    lowKeyText  .bind("<Button-1>", spotifyIntern.hotKeyEntryClicked)
    highKeyText .bind("<Button-1>", spotifyIntern.hotKeyEntryClicked)

    # Opens the settings file
    settingsFile = open("Config\\hotkeys", "r")
    fileLines = settingsFile.readlines()
    settingsFile.close()

    playKey  = fileLines[0][:-1]
    endKey   = fileLines[1][:-1]
    pauseKey = fileLines[4][:-1]
    lowKey   = fileLines[2][:-1]
    highKey  = fileLines[3][:-1]

    # Adding the hotkeys to the entry
    playKeyText .insert(0, playKey)
    endKeyText  .insert(0, endKey)
    pauseKeyText.insert(0, pauseKey)
    lowKeyText  .insert(0, lowKey)
    highKeyText .insert(0, highKey)

    saveButton = Button(hotkeyWindow, text = "Save", command = saveHotKeys, bg = "#f57e3a", fg = "#000000", activebackground = "#000000", activeforeground = "#f57e3a")
    # recordButton = Button(hotkeyWindow, text = "Record Hotkey", command = spotifyIntern.hotKeyRecord, bg = "#f57e3a", fg = "#000000", activebackground = "#000000", activeforeground = "#f57e3a")
    
    # Adding the elements
    hotkeyCanvas.create_text(50, 50, justify = "center", text = "Play Hotkey")
    hotkeyCanvas.create_text(170, 50, justify = "center", text = "End Game Hotkey")
    hotkeyCanvas.create_text(290, 50, justify = "center", text = "Pause Hotkey")
    hotkeyCanvas.create_text(105, 150, justify = "center", text = "Volume Down Hotkey")
    hotkeyCanvas.create_text(235, 150, justify = "center", text = "Volume Up Hotkey")

    hotkeyCanvas.create_window(50, 70, window = playKeyText)
    hotkeyCanvas.create_window(170, 70, window = endKeyText)
    hotkeyCanvas.create_window(290, 70, window = pauseKeyText)
    hotkeyCanvas.create_window(105, 170, window = lowKeyText)
    hotkeyCanvas.create_window(235, 170, window = highKeyText)

    hotkeyCanvas.create_window(270, 250, window = saveButton)
    # hotkeyCanvas.create_window(170, 120, window = recordButton) doesnt work, probebly remove


def createRemakeWindow():
    '''Creates the hotkey window'''
    global remakeWindow
    remakeWindow = tk.Toplevel()
    remakeWindow.title("Remake")
    remakeWindow.iconbitmap("Images\\ValoBeatsLogo.ico")

    # Calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    # Creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 540/2))
    oHeight = str(int(height - 360/2 - 65))

    # Creates size of screen
    remakeWindow.geometry("540x360+" + oWidth + "+" + oHeight)

    remakeCanvas = Canvas(remakeWindow, width = 540, height = 360)
    remakeCanvas.pack(fill = "both", expand = True)

    # Gets photo from settings
    global hotkeyImage
    hotkeyImage = PhotoImage(file = "Images\\RemakeWindowBG.gif")

    # Adds the image to the canvas
    remakeCanvas.create_image(0, 0, image = hotkeyImage, anchor = "nw")

    global remakeOneButton
    global remakeAllButton
    global remakePlaylistButton

    # Creates the buttons for remaking    
    remakeOneButton =      Button(remakeWindow, text = "Remake One", command = spotifyIntern.remakeOneSong, bg = "#f57e3a", fg = "#000000", activebackground = "#000000", activeforeground = "#f57e3a")
    remakeAllButton =      Button(remakeWindow, text = "Remake All", command = remakeSongFile, bg = "#f57e3a", fg = "#000000", activebackground = "#000000", activeforeground = "#f57e3a")
    remakePlaylistButton = Button(remakeWindow, text = "Remake Playlist", bg = "#f57e3a", fg = "#000000", activebackground = "#000000", activeforeground = "#f57e3a")

    closeButton = Button(remakeWindow, text = "Close", command = remakeWindow.destroy, bg = "#f57e3a", fg = "#000000", activebackground = "#000000", activeforeground = "#f57e3a")
    
    # Adding the elements
    remakeCanvas.create_window(50, 70, window = remakeOneButton)
    remakeCanvas.create_window(170, 70, window = remakeAllButton)
    remakeCanvas.create_window(290, 70, window = remakePlaylistButton)

    remakeCanvas.create_window(270, 250, window = closeButton)

def settingsDestroyed(e = None):
    '''When the settings window is manually closed and they didn't click save, 
    reopen the main window and remake the hotkeys'''
    mainWindow.deiconify()
    spotifyIntern.makeHotKeys()

def saveSettings():
    '''Saves the settings to the file'''
    # Gets the previous file name incase we can't connect to internet
    settingsFile = open("Config\\settings", "r")
    ogFileName = settingsFile.readlines()[3]
    settingsFile.close()

    settingsFile = open("Config\\settings", "w")

    # Writing volume in correct format
    if (loudVolumeScale.get() < 10):
        settingsFile.write("00" + str(loudVolumeScale.get()))
    elif (loudVolumeScale.get() < 100):
        settingsFile.write("0" + str(loudVolumeScale.get()))
    else:
        settingsFile.write(str(loudVolumeScale.get()))

    if (quietVolumeScale.get() < 10):
        settingsFile.write("00" + str(quietVolumeScale.get()) + "\n")
    elif (quietVolumeScale.get() < 100):
        settingsFile.write("0" + str(quietVolumeScale.get()) + "\n")
    else:
        settingsFile.write(str(quietVolumeScale.get()) + "\n")

    # Write the game type
    settingsFile.write(radioGameType.get() + "\n")

    # Write the playlist link
    settingsFile.write(playListLinkText.get() + "\n")
    
    # Write the playlist name only if it is valid else write previous file name
    tempFileName = spotifyIntern.playlistURLToFileName(playListLinkText.get())
    if tempFileName:
        settingsFile.write(tempFileName)
    else:
        settingsFile.write(ogFileName)

    # End writing the settings
    settingsFile.close()

    if not spotifyIntern.isValidPlaylist():
        messagebox.showerror("Invalid Input", playListLinkText.get() + " is not a valid public playList link, please try again")
        return

    # Checking if a device is open
    devices = spotifyIntern.getDevices()
    if devices == False:
        messagebox.showwarning("Connection Failed", "Unable to connect to the Spotify servers, skipping downloading and checking of songs")
    elif devices['devices'] == None:
        messagebox.showerror("No Devices", "No active devices found. Open Spotify on a device signed into your account and try again.")
        return
    else:
        # Createing new playlist Song File or adding to previous
        fileName = spotifyIntern.playlistURLToFileName(playListLinkText.get())
        playlistSongFile = open("Songs\\" + fileName, "a")

        uniqueSongs = spotifyIntern.updatePlaylistFile(fileName)
        failedSongs = spotifyIntern.downloadNewSongs(uniqueSongs)
        if failedSongs:
            for song in failedSongs:
                uniqueSongs.remove(song)
        '''PART 2 Add new information to mastersongfile from user'''
        
        # Asks how you want to input the songs
        if len(uniqueSongs) != 0:
            realAnswer = messagebox.askyesnocancel("Song Timing", "Would you like to use local playing to set the timing for all the songs? (Most accurate)")
            if not realAnswer:
                spotAnswer = messagebox.askyesnocancel("Song Timing", "Would you like to use your spotify in your browser set the timing for all the songs?")

        masterSongFile = open("Songs\\masterSongFile", "a")

        # Asks What time you want each new song to start at
        for song in uniqueSongs:
            # Using pygame to find the song time
            if realAnswer:
                correct = False
                while True:
                    # Loops until we get correct input
                    messagebox.showinfo("Song Timing", "After pressing OK, wait until the time you want the song to play and then click any button")
                    try:
                        # only add it if the song is works when playing it
                        spotifyIntern.playSong(song)
                    except:
                        break
                    # Waits for any key press
                    keyboard.read_key()
                    
                    time = spotifyIntern.getLocalPlayTime()
                    spotifyIntern.pausePlay()
                    
                    correct = messagebox.askyesnocancel("Song Timing", "The time you entered is " + str(time) + ". Is this correct?")
                    
                    if (correct == None or correct == True):
                        break
                if correct:
                    # Only add the song if they didn't press cancel
                    masterSongFile.write(song + " " + str(time) + "\n")
                    playlistSongFile.write(song + " " + str(time) + "\n")
            # Using Spotify in browser
            elif spotAnswer:
                correct = False
                while True:
                    # Loops until we get correct input
                    messagebox.showinfo("Song Timing", "Please go to the time at which you want the song " + spotifyIntern.getNameOfSong(song) + " to start on a device and then click OK")
                    time = spotifyIntern.getSongTime()
                    if (time != -1):
                        correct = messagebox.askyesnocancel("Song Timing", "The time you entered is " + str(time) + ". Is this correct?")
                        if (correct == None or correct == True):
                            break
                if correct:
                    # Only add the song if they didn't press cancel
                    masterSongFile.write(song + " " + str(time) + "\n")
                    playlistSongFile.write(song + " " + str(time) + "\n")
            # Using manual input
            else:
                while True:
                    timeAnswer = simpledialog.askfloat("Song Timing", "What time would you like the song " + spotifyIntern.getNameOfSong(song) + " to start at?")
                    if timeAnswer == None:
                        break
                    if timeAnswer >= 0:
                        break
                    else:
                        messagebox.showerror("Song Timing", str(timeAnswer) + " is not a valid time")
                if timeAnswer != None:
                    masterSongFile.write(song + " " + str(timeAnswer) + "\n")
                    playlistSongFile.write(song + " " + str(time) + "\n")

        masterSongFile.close()

    # Show main window
    mainWindow.deiconify()

    settingsWindow.destroy()

def saveHotKeys():
    '''Saves the hotkeys to the file'''
    settingsFile = open("Config\\hotkeys", "w")

    # Writing the hotkeys to the file
    settingsFile.write(playKeyText.get()  + "\n")
    settingsFile.write(endKeyText.get()   + "\n")
    settingsFile.write(lowKeyText.get()   + "\n")
    settingsFile.write(highKeyText.get()  + "\n")
    settingsFile.write(pauseKeyText.get() + "\n")

    settingsFile.close()

    spotifyIntern.makeHotKeys()

    hotkeyWindow.destroy()

def addSongNext():
    '''Uses Spotify's search to look through the main file for the song requested, then adds that song to play next'''
    songsFile = open("Songs\\masterSongFile", "r")
    masterLines = songsFile.readlines()

    masterSongs = []
    for line in masterLines:
        masterSongs.append(line[:line.find(" ")])
    found = False
    # Searching for the song
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
        message = "Song found and added to que. Current que is: "

        for song in spotifyIntern.getNextSongs():
            message += spotifyIntern.getNameOfSong(song[:song.index(" ")]) + ", "
        message = message[:-2]

        messagebox.showinfo("Search", message)
    else:
        messagebox.showinfo("Search", "No saved song was found using the query: \"" + nextSongText.get() + "\". try narrowing it down by searching with the author as well.")

def remakeSongFile():
    '''Double checks that you want to delete the '''
    answer = messagebox.askquestion("Confirmation", "Are you sure you want to DELETE ALL saved songs and redo the Song Timing for ALL saved songs?")
    if (answer == "yes"):
        spotifyIntern.deleteSongFile()

def endProgram():
    '''Closes and ends the program'''
    mainWindow.quit()
    mainWindow.destroy()

def main():
    '''Main Function creates the main window'''

    # Creates main window
    global mainWindow
    mainWindow = tk.Tk()
    # mainWindow.overrideredirect(1) # If I dont want a window boarder, but it also doent make a moveable window 
    
    # Changing the Icon
    mainWindow.iconbitmap("Images\\ValoBeatsLogo.ico")

    # Creates a spotify intern
    global spotifyIntern
    spotifyIntern = SI.SpotifyInteractor(mainWindow.winfo_screenwidth(), mainWindow.winfo_screenheight())

    # For later
    global radioGameType
    radioGameType = tk.StringVar()

    # Calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    # Creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 640/2))
    oHeight = str(int(height - 427/2 - 30))

    # Creates screen and size
    mainWindow.title("Main Screen")
    mainWindow.geometry("640x427" + "+" + oWidth + "+" + oHeight)

    # Gets photo for main
    mainImage = PhotoImage(file = "Images\\ValoBeatsMainBG.gif")

    # Creates a canvas for the photo and text to be put on
    mainCanvas = Canvas(mainWindow, width = 640, height = 427)
    mainCanvas.pack(fill = "both", expand = True)

    # Adds the image to the canvas
    mainCanvas.create_image(0, 0, image = mainImage, anchor = "nw")

    # Stores the next song
    global nextSongText

    # Creates buttons
    backGround = "#04121e"
    foreGround = "#f52740"

    activebackground = "#f52740"
    activeforeground = "#04121e"
    boarderWidth = 0,

    shuffleButton   = Button(mainWindow, text = "Shuffle songs", width = 12, bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = spotifyIntern.shuffleSongs)
    resetRoundsButton = Button(mainWindow, text = "Finish Game", width = 12, bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = spotifyIntern.resetRounds)

    searchButton = Button(mainWindow, text = "Add Next Song To Play", width = 18, bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = addSongNext)
    nextSongText = Entry(mainWindow, justify = "center", width = 22, bg = foreGround, fg = backGround)

    settingsButton = Button(mainWindow, text = "Open Settings", bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = createSettingsWindow)

    closeButton = Button(mainWindow, text = "Close", bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = endProgram)
    
    # Adds each element to the canvas
    mainCanvas.create_window(80, 80, window = shuffleButton)
    mainCanvas.create_window(80, 105, window = resetRoundsButton)

    mainCanvas.create_window(500, 125, window = searchButton)
    mainCanvas.create_window(500, 146, window = nextSongText)

    mainCanvas.create_window(485, 320, window = settingsButton)

    mainCanvas.create_window(310, 300, window = closeButton)

    # Wait for input
    mainWindow.mainloop()

if __name__ == "__main__":
    main()
