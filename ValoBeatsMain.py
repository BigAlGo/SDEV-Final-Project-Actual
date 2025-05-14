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

    radioGameType.set(fileLines[1][:-1])

    # Creates a scale, a button, and text entry to put on the canvas
    global loudVolumeScale
    global quietVolumeScale
    loudVolumeScale = Scale(settingsWindow, from_ = 0, to_ = 100, orient = tk.HORIZONTAL, resolution = 1, bg = "#d85965", troughcolor = "#4f374d", activebackground = "#d85965", highlightbackground = "#d1656c", highlightcolor= "#000000")
    quietVolumeScale = Scale(settingsWindow, from_ = 0, to_ = 100, orient = tk.HORIZONTAL, resolution = 1, bg = "#d85965", troughcolor = "#4f374d", activebackground = "#d85965", highlightbackground = "#d1656c", highlightcolor= "#000000")


    # Sets the orginal volume to be the last volume
    loudVolumeScale.set(int(fileLines[0][0:3]))
    quietVolumeScale.set(int(fileLines[0][3:6]))

    # Creates the entry fields for the playlist
    global playListLinkText
    playListLinkText = Entry(settingsWindow, width = 30, justify = "center", bg = "#eb4454", fg = "#e8fbfb")
    
    # Adds previous playlist to the field
    playListLinkText.insert(0, fileLines[2])

    settingsFile.close()

    confirmButton = Button(settingsWindow, text = "Save", command = saveSettings, bg = "#4c9ba4", activebackground = "#000000", activeforeground = "#4c9ba4")
    openRemakeWindow = Button(settingsWindow, text = "Open Remake Window", command = createRemakeWindow, bg = "#4c9ba4", activebackground = "#000000", activeforeground = "#4c9ba4")
    openHotkeyWindow = Button(settingsWindow, text = "Open Hotkey Window", command = createHotKeyWindow, bg = "#72d8cc", activebackground = "#000000", activeforeground = "#4c9ba4")

    # Adds everything to the canvas
    settingsCanvas.create_window(320, 300, window = loudVolumeScale)
    settingsCanvas.create_window(320, 350, window = quietVolumeScale)

    settingsCanvas.create_window(1120, 470, window = normalRadio)
    settingsCanvas.create_window(1120, 500, window = swiftRadio)
    settingsCanvas.create_window(1120, 530, window = spikeRadio)

    settingsCanvas.create_window(640, 600, window = confirmButton)
    settingsCanvas.create_window(160, 500, window = openRemakeWindow)

    settingsCanvas.create_window(640, 335, window = playListLinkText)
    settingsCanvas.create_window(960, 285, window = openHotkeyWindow)

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
    hotkeyImage = PhotoImage(file = "Images\\HotKeysImage.gif")

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
    oHeight = str(int(height - 303/2 - 65))

    # Creates size of screen
    remakeWindow.geometry("540x303+" + oWidth + "+" + oHeight)

    remakeCanvas = Canvas(remakeWindow, width = 540, height = 303)
    remakeCanvas.pack(fill = "both", expand = True)

    # Gets photo from settings
    global hotkeyImage
    hotkeyImage = PhotoImage(file = "Images\\HotKeysImage.gif")

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

# Loading Bar window
def createLoadingBarWindow():
    '''Creates the loading bar window'''
    global loadingBarWindow
    loadingBarWindow = tk.Toplevel()
    loadingBarWindow.title("Loading Bar")
    loadingBarWindow.iconbitmap("Images\\ValoBeatsLogo.ico")

    # Calculates the middle of the screen
    width = mainWindow.winfo_screenwidth() / 2
    height = mainWindow.winfo_screenheight() / 2

    # Creates a string of the offset needed to get to the center of the screen
    oWidth = str(int(width - 540/2))
    oHeight = str(int(height - 303/2 - 65))

    # Creates size of screen
    loadingBarWindow.geometry("540x303+" + oWidth + "+" + oHeight)

    # Creates a canvas
    global loadingBarCanvas
    loadingBarCanvas = Canvas(loadingBarWindow, width = 540, height = 303)
    loadingBarCanvas.pack(fill = "both", expand = True)

    loadingBarCanvas.create_rectangle(90, 90, 460, 210, outline = "black", fill = "white", tag = "outline")
    loadingBarCanvas.create_rectangle(100, 100, 450, 200, outline = "red", fill = "red", tag="box")
    loadingBarCanvas.create_text(270, 150, text = "Song Download Progress", font = ("Lucida Sans", 30), fill = "#000000", tag = "text")

    threading.Thread(target = loadingThread, daemon=True).start()

def loadingThread():
    '''Updates the loading bar'''
    startTime = time.time()
    while True:
        songsToDownload = getSongsToDownload(startTime)
        # if len(songsToDownload) == 0:
            # break
        print(songsToDownload)

        # Updates the loading bar based on the number of songs to download vs original number of songs
        loadingBarCanvas.coords("box", 100, 100, 450 - (len(songsToDownload) * 35), 200)
        loadingBarCanvas.update()
        time.sleep(0.1)

    loadingBarWindow.destroy()

def getSongsToDownload(startTime):
    '''Gets the songs to download from the online playlist vs local'''
    settingsFile = open("Config\\settings", "r")
    playlistURL = settingsFile.readlines()[2]
    settingsFile.close()
    
    # Gets the songs in the playlist
    try:
        tracks = spotifyIntern.spotifyClient.playlist_tracks(playlistURL)['items']

        # Extract track URLs
        spotifySongs = []
        for track in tracks:
            if track["track"]:
                spotifySongs.append(track["track"]["external_urls"]["spotify"])

        # Gets the folder of the songs
        cwd = os.getcwd()
        outputPath = cwd + "\\Songs\\LocalSongsOGG"

        # Makes a list of the songs in the local folder
        localSongs = []
        for file in os.listdir(outputPath):
            if file.endswith(".ogg"):
                localSongs.append(file[:-4])

        # Checks if the songs in spotifySongs are in localSongs
        # If they are not, add them to the list of songs to download
        songsToDownload = []
        for song in spotifySongs:
            songFileName = spotifyIntern.sanitizeFilename(song) + ".ogg"
            if song not in localSongs:
                songsToDownload.append(song)
    except:
        songsToDownload = [1] * int(10 - (time.time() - startTime))

    return songsToDownload
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
    settingsFile.write(playListLinkText.get())
    
    # Write the playlist name only if it is valid else write previous file name
    tempFileName = spotifyIntern.playlistURLToFileName(playListLinkText.get())
    if tempFileName:
        print(tempFileName)
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
        masterSongFile = open("Songs\\masterSongFile", "a")

        # Createing new playlist Song File or adding to previous
        fileName = spotifyIntern.playlistURLToFileName(playListLinkText.get())
        playlistSongFile = open("Songs\\" + fileName, "a")
        
        # Asks how you want to input the songs
        uniqueSongs = spotifyIntern.updatePlaylistFile(fileName)
        spotifyIntern.downloadNewSongs(uniqueSongs)

        if len(uniqueSongs) != 0:
            realAnswer = messagebox.askyesnocancel("Song Timing", "Would you like to use local playing to set the timing for all the songs? (Most accurate)")
            if not realAnswer:
                spotAnswer = messagebox.askyesnocancel("Song Timing", "Would you like to use your spotify in your browser set the timing for all the songs?")

        # Asks What time you want each new song to start at
        for song in uniqueSongs:
            # Using pygame to find the song time
            if realAnswer:
                correct = False
                while True:
                    # Loops until we get correct input
                    messagebox.showinfo("Song Timing", "After pressing OK, wait until the time you want the song to play and then click any button")
                    spotifyIntern.playSong(song)
                    # Waits for any key press
                    keyboard.read_key()
                    
                    time = spotifyIntern.getLocalPlayTime()
                    spotifyIntern.pauseToggle()
                    
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
    settingsFile.write(playKeyText.get() + "\n")
    settingsFile.write(endKeyText.get() + "\n")
    settingsFile.write(lowKeyText.get() + "\n")
    settingsFile.write(highKeyText.get() + "\n")
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
    answer = messagebox.askquestion("Confirmation", "Are you sure you want to DELETE ALL saved songs and redo the Song Timing for all the songs in the current playlist?")
    if (answer == "yes"):
        spotifyIntern.deleteSongFile()

def endProgram():
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

    closeButton = Button(mainWindow, text = "Close", bg = backGround, fg = foreGround, activebackground = activebackground, activeforeground = activeforeground, bd = boarderWidth, command = endProgram)
    # Adds each element to the canvas
    mainCanvas.create_window(80, 50, window = shuffleButton)
    mainCanvas.create_window(80, 75, window = resetRoundsButton)

    mainCanvas.create_window(500, 105, window = searchButton)
    mainCanvas.create_window(500, 126, window = nextSongText)

    mainCanvas.create_window(450, 300, window = settingsButton)

    mainCanvas.create_window(320, 270, window = closeButton)

    # Wait for input
    createLoadingBarWindow()
    mainWindow.mainloop()

if __name__ == "__main__":
    main()
