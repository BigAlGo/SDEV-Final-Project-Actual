import spotdl.download
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from tkinter import messagebox
from tkinter import simpledialog
from pygame import mixer
import OpenCVVision as OpenCv
import tkinter as tk
import os
import subprocess
import time
import random
import keyboard
import spotipy
import re
import threading
import sys
from spotdl import Spotdl
from spotdl.types.options import DownloaderOptions

class SpotifyInteractor():
    '''This class contains methods to interact with spotify and writing to the local file system'''
    def __init__(self, screenWidth, screenHeight):
        '''Creates a SpotifyInteractor object by creating a spotdl object and a spotpy object'''
        self.vision = OpenCv.OpenCVVision(screenWidth, screenHeight, self.roundStart)

        mixer.init()

        self.makeHotKeys()
        self.songNumber = 0
        self.roundNumber = 1

        # Initing spotipy
        clientId = "35661866380c4cdcb93e51cc756ee958"
        clientSecret = "fd334360adb04a7980412c946f1e00af"
        # Able to get and modify the playback state and able to read public playlists 
        SCOPE = "user-modify-playback-state user-read-playback-state"
        authManagerClient = SpotifyOAuth(
            client_id = clientId,
            client_secret = clientSecret,
            redirect_uri="http://localhost:5000/callback",
            scope=SCOPE,
            show_dialog=True
        )
        self.spotifyClient = spotipy.Spotify(auth_manager = authManagerClient)
        
        # SpotDL options
        outputDir = "Songs\\LocalSongsOGG"
        downloader_settings = {
            "output_format": "ogg",
            "output": outputDir,
            "threads": 1
        }
        # Initialize SpotDL instance
        self.spotdl = Spotdl(
            client_id = clientId,
            client_secret = clientSecret,
            downloader_settings = downloader_settings
        )
        # Checking of you are able to connect to spotify's servers
        devices = self.getDevices()
        if devices == False:
            messagebox.showwarning("Connection Failed", "Unable to connect to the Spotify servers, It is blocked by a firewall or something")
 
        self.nextSongs = []
        self.roundLoop = False
        self.savedKey = None
        self.hotKeyRecord = None
        self.paused = False
        self.lastPauseTime = time.time()

    def roundStartHotKeyPressed(self):
        '''Pass through function'''
        self.setVolumeHigh()
        self.startRoundLoop()

    def startRoundLoop(self):
        '''Starts the thread if it is not already open'''
        if not self.roundLoop:
            self.roundLoop = True
            self.vision.startLoop()
            threading.Thread(target=self.roundStart, daemon=True).start()
            print("thread start")


    def stopRoundLoop(self):
        '''Stops the thread'''
        self.roundLoop = False
        self.vision.stopLoop()
        self.resetRounds()

    def roundStart(self):
        '''Plays a song after a specified time'''
        # I am in a thread so while loops don't affect the over all program
        startTime = time.time()

        # Get the playlist file
        file_name = self.getPlaylistFileFromSettings()
        if not file_name:
            settingsFile = open("Config\\settings", "r")
            file_name = settingsFile.readlines()[3]
            settingsFile.close()
        
        # Get the song info
        songFile = open("Songs\\" + file_name, "r")
        if len(self.nextSongs) == 0:
            songLines = songFile.readlines()
            songLine = songLines[self.songNumber]
        else:
            songLine = self.nextSongs[0]

        # Extract song info from the song line
        songTime = float(songLine.split(" ")[-1].strip())
        songUrl = songLine.split(" ")[0]

        # Update song number
        if len(self.nextSongs) == 0:
            # Loops through the song file
            if self.songNumber > len(songLines) - 2:
                self.songNumber = 1
            else:
                self.songNumber += 1
        else:
            self.nextSongs.pop(0)

        # Determine game type
        file = open("Config\\settings", "r")
        gameType = file.readlines()[1].strip()
        file.close()

        # Adjust round timing based on game type format is:
        # firstTime, halfRound, halfTime, normalTime, overRound
        roundTimes = {
            "Normal": (31, 13, 45, 30, 25),
            "Swift" : (31, 5, 45, 30, 9),
            "Spike" : (11, 4, 20, 20, 7)
        }
        firstRoundTime, halfTimeRound, halfTimeTime, normalRoundTime, overTimeRound = roundTimes.get(gameType, (30, 13, 45, 30, 25))

        # Determine when to play the song
        if self.roundNumber == 1:
            thisRoundTime = firstRoundTime
        elif self.roundNumber == halfTimeRound or self.roundNumber >= overTimeRound:
            thisRoundTime = halfTimeTime
        else:
            thisRoundTime = normalRoundTime
        
        roundStartTime = startTime + thisRoundTime

        # Figure out if we need to wait or play now
        if thisRoundTime - songTime - 3 >= 0:
            # Calculating when we need to do things
            playAfterTime = roundStartTime - songTime
            fadeOutStartTime = playAfterTime - 3
            loadMusicTime = playAfterTime - songTime - 0.5

            while time.time() < fadeOutStartTime:
                time.sleep(0.05)
            
            mixer.music.fadeout(2500)

            while time.time() < loadMusicTime:
                time.sleep(0.05)

            # Load song
            songPath = "Songs\\LocalSongsOGG\\" + self.sanitizeFilename(songUrl) + ".ogg"
            mixer.music.load(songPath)

            while time.time() < playAfterTime:
                time.sleep(0.05)

            # Play song
            mixer.music.play(loops = -1, fade_ms = 0)

            while time.time() < roundStartTime:
                time.sleep(0.05)

            # Wait for the barrier drop
        else:
            # Calculating when we need to do things
            mixer.music.fadeout(2500)
            calcsTime = time.time()
            playIntoTime = -(startTime + thisRoundTime - calcsTime - 3 - songTime)
            loadMusicTime = calcsTime + 2.5
            playTime = calcsTime + 3
            
            while time.time() < loadMusicTime:
                time.sleep(0.05)

            # Load song
            songPath = "Songs\\LocalSongsOGG\\" + self.sanitizeFilename(songUrl) + ".ogg"
            mixer.music.load(songPath)

            while time.time() < playTime:
                time.sleep(0.05)

            # Play song
            mixer.music.play(loops = -1, fade_ms = 500)
            mixer.music.set_pos(playIntoTime)

            while time.time() < roundStartTime:
                time.sleep(0.05)
            
            # Wait for the barrier drop
        self.setVolumeHigh()

        # Making sure the text is off screen before running vision
        time.sleep(1)

        # Update round number
        self.roundNumber += 1
        
        if self.roundLoop:
            # I am still in a thread so while loops don't affect the overall program
            self.vision.mainLoop()
        else:
            self.resetRounds()

    def makeHotKeys(self):
        '''Creates the hotkeys based on the hotKeys file'''
        settingsFile = open("Config\\hotKeys", "r")
        fileLines = settingsFile.readlines()
        settingsFile.close()

        playKey = fileLines[0][:-1]
        endKey = fileLines[1][:-1]
        lowKey = fileLines[2][:-1]
        highKey = fileLines[3][:-1]
        pauseKey = fileLines[4][:-1]

        try:
            keyboard.add_hotkey(playKey, callback = self.roundStartHotKeyPressed)
            keyboard.add_hotkey(endKey, callback = self.stopRoundLoop)
            keyboard.add_hotkey(lowKey, callback = self.setVolumeLow)
            keyboard.add_hotkey(highKey, callback = self.setVolumeHigh)
            keyboard.add_hotkey(pauseKey, callback = self.pausePlay)

            return True
        except ValueError:
            return False

    def hotKeyEntryClicked(self, event):
        '''Replaces the entry with the hotkey'''
        if self.hotKeyRecord:
            # if not None 
            event.widget.delete(0, tk.END)
            event.widget.insert(0, self.hotKeyRecord)
            self.hotKeyRecord = None

    def isValidPlaylist(self):
        '''Returns if the URL on line 3 of the settings file is valid'''
        settingsFile = open("Config\\settings", "r")
        playlistURL = settingsFile.readlines()[2]
        settingsFile.close()

        # Tries to fetch the playlist
        try:
            self.spotifyClient.playlist(playlistURL)
            return True
        except spotipy.exceptions.SpotifyException:
            return False
        except:
            messagebox.showwarning("Connection failed", "Unable to check if the playlist is valid because we are unable to connect to the Spotify servers, we will assume that the link is correct")
            return True

    def updatePlaylistFile(self, playlistFileName):
        '''Returns a list of lings to songs that have not been saved but are in the spotify playlist
        and writes all songs that are in the online playlist from the master file, to the playlist file'''        
        
        # Creates a list of all the saved songs 
        songsFile = open("Songs\\masterSongFile", "r")
        masterLines = songsFile.readlines()
        songsFile.close()

        masterSongs = []
        for line in masterLines:
            masterSongs.append(line[:line.find(" ")])

        songsFile = open("Songs\\" + playlistFileName, "r")
        oldLines = songsFile.readlines()
        songsFile.close()

        oldSongs = []
        for line in oldLines:
            oldSongs.append(line[:line.find(" ")])
        
        # Creates a list of all the songs in the playlist
        # Reads the url from settings
        settingsFile = open("Config\\settings", "r")
        playlistURL = settingsFile.readlines()[2]
        settingsFile.close()

        # Creates a list of new songs
        tracks = self.spotifyClient.playlist_tracks(playlistURL)['items']

        # Extract track URLs
        newSongs = []
        for track in tracks:
            if track["track"]:
                newSongs.append(track["track"]["external_urls"]["spotify"])
        
    
        playlistFile = open("Songs\\" + playlistFileName, "w")
        masterFile = open("Songs\\masterSongFile", "r")

        uniqueSongs = []
        for newSong in newSongs:
            found = False
            for masterSong in masterSongs:
                if newSong == masterSong:
                    # Found in master songs, refind the whole line, then add to playlist file
                    masterFile.seek(0)
                    for masterLine in masterFile.readlines():
                        if masterLine.find(newSong) != -1:
                            newLine = masterLine
                            break
                    playlistFile.write(newLine)
                    found = True
                    break
            
            if not found:
                # Not in master or playlist file, ask what time
                uniqueSongs.append(newSong)
        
        playlistFile.close()
        masterFile.close()
        return uniqueSongs
    
    def getPlaylistLinks(self, playlistFileName):
        '''Returns a list of lings to songs that have not been saved but are in the spotify playlist
        and writes songs from the master file that are not in the playlist file, to the playlist file'''        
        
        # Creates a list of all the saved songs 
        songsFile = open("Songs\\masterSongFile", "r")
        masterLines = songsFile.readlines()
        songsFile.close()

        masterSongs = []
        for line in masterLines:
            masterSongs.append(line[:line.find(" ")])

        songsFile = open("Songs\\" + playlistFileName, "r")
        oldLines = songsFile.readlines()
        songsFile.close()

        oldSongs = []
        for line in oldLines:
            oldSongs.append(line[:line.find(" ")])
        
        # Creates a list of all the songs in the playlist
        # Reads the url from settings
        settingsFile = open("Config\\settings", "r")
        playlistURL = settingsFile.readlines()[2]
        settingsFile.close()

        # Creates a list of new songs
        tracks = self.spotifyClient.playlist_tracks(playlistURL)['items']

        # Extract track URLs
        newSongs = []
        for track in tracks:
            if track["track"]:
                newSongs.append(track["track"]["external_urls"]["spotify"])
        
    
        playlistFile = open("Songs\\" + playlistFileName, "a")
        masterFile = open("Songs\\masterSongFile", "r")

        uniqueSongs = []
        found = False
        for newSong in newSongs:
            found = False
            for oldSong in oldSongs:
                if newSong == oldSong:
                    # Already in the playlist file, do nothing
                    found = True
                    break

            if not found:
                # Not in playlist file
                for masterSong in masterSongs:
                    if newSong == masterSong:
                        # Found in master songs, refind the whole line, then add to playlist file
                        masterFile.seek(0)
                        for masterLine in masterFile.readlines():
                            if masterLine.find(newSong) != -1:
                                newLine = masterLine
                                break
                        playlistFile.write(newLine)
                        found = True
                        break
                
                if not found:
                    # Not in master or playlist file, ask what time
                    uniqueSongs.append(newSong)
        
        playlistFile.close()
        masterFile.close()
        return uniqueSongs
    
    def downloadNewSongs(self, songUrls):
        '''Takes in a list of songUrls and downloads them'''

        if len(songUrls) == 0:
            return
        
        # Getting the number of songs
        numberOfSongs = len(songUrls)

        # Assumes 15 sec per song to download
        timeSec = 15 * numberOfSongs
        
        timeMinute = int(timeSec / 60.0)
        timeSec = timeSec % 60

        if (numberOfSongs >= 1):
            messagebox.showinfo("Downloading Songs", "The program will download " + str(numberOfSongs) + " songs from spotify, estimated time: " + str(timeMinute) + " minute(s) and " + str(timeSec) + " seconds. It may be longer depending on your internet.\nIf the program says it is not responding during this time, it is still downloading.\nDO NOT CLOSE THE PROGRAM DURING THIS TIME!")
        failedURLs = []
        for url in songUrls:
            try:
                if not self.downloadSong(url):
                    failedURLs.append(url)
            except:
                messagebox.showerror("Error Downloading", "Error Downloading " + url + ", song might have got deleted off of spotify")
                failedURLs.append(url)
        return failedURLs

    def downloadSavedSongs(self):
        '''Downloades the songs saved in masterSongFile'''
        songsFile = open("Songs\\masterSongFile", "r")
        songLines = songsFile.readlines()
        songsFile.close()

        songUrls = []

        for line in songLines:
            songUrls.append(line.split(" ")[0])

        cwd = os.getcwd()
        localSongs = cwd + "\\Songs\\LocalSongsOGG"

        # Getting the number of songs in master vs in local
        fileSongs = len(os.listdir(localSongs))
        nameSongs = len(songUrls)
        numberOfSongs = nameSongs - fileSongs

        # Assumes 30 sec per song to download
        timeSec = 30 * numberOfSongs
        
        timeMinute = int(timeSec / 60.0)
        timeSec = timeSec % 60

        if (numberOfSongs >= 1):
            messagebox.showinfo("Downloading Songs", f"The program will download {numberOfSongs} songs from spotify, estimated time: {timeMinute} minute(s) and {timeSec} seconds. It may be longer depending on your internet. If the program says it is not responding during this time, it is probebly still downloading")

        for url in songUrls:
            self.downloadSong(url)
        

    def shuffleSongs(self):
        '''This shuffles the songs in songNames'''
        fileName = self.getPlaylistFileFromSettings()
        songNames = open("Songs\\" + fileName, "r")

        songs = songNames.readlines()
        songNames.close()
        
        random.shuffle(songs)

        fileName = self.getPlaylistFileFromSettings()

        songNames = open("Songs\\" + fileName, "w")
        songNames.writelines(songs)
        songNames.close()

    def convertUrlToUri(self, spotifyUrl):
        '''Converts from a Spotify URL to a Spotify URI'''
        if "track/" in spotifyUrl:
            # For Tracks
            trackId = spotifyUrl.split("track/")[1].split("?")[0]
            return "spotify:track:" + trackId
        elif "playlist/" in spotifyUrl:
            # For playlists
            playlistId = spotifyUrl.split("playlist/")[1].split("?")[0]
            return "spotify:playlist:" + playlistId
        return None

    def getDevices(self):
        '''Gets the devices signed into the account'''
        try:
            self.devices = self.spotifyClient.devices()
            return self.devices
        except:
            # Unable to connect to Spotify
            return False
    
    def getNameOfSong(self, url):
        '''Returns the name of a song given the url'''
        return self.spotifyClient.track(url)['name']
    
    def getNameofPlaylist(self, uri):
        '''Returns the name of a playlist given the uri'''
        id = uri.split("spotify:playlist:")[1]
        return self.spotifyClient.playlist(id)['name']
    
    def getPlaylistFileFromSettings(self):
        '''Gets the name of the playlist file name from settings'''
        settingsFile = open("Config\\settings", "r")
        fileName = self.playlistURLToFileName(settingsFile.readlines()[2])
        settingsFile.close()
        return fileName
    
    def getSongTime(self):
        '''Gets the time of the current song playing in spotify'''
        playback = self.spotifyClient.current_playback()

        # If somthing is playing
        if playback:
            songTime = playback["progress_ms"] / 1000 
            return songTime
        else:
            messagebox.showwarning("Song timing", "No song is currently playing.")
            return -1
        
    def getLocalPlayTime(self):
        '''Gets the time of the current song playing in pygame'''
        return mixer.music.get_pos() / 1000
    
    def sanitizeFilename(self, name):
        '''Replaces invalid filename characters'''
        name = name.strip().replace(" ", "_")
        return re.sub(r'[<>:"/\\|?*]', "_", name)
    
    def playlistURLToFileName(self, url):
        '''Converts from url to uri to name to sanitized filename '''
        try:
            return self.sanitizeFilename(self.getNameofPlaylist(self.convertUrlToUri(url)))
        except:
            return False

    def searchForBestSong(self, name):
        '''Uses spotify's search to look for the 20 best songs'''
        return self.spotifyClient.search(q = name, type = "track", limit = 30)

    def remakeOneSong(self):
        '''Deleats one song with the search algorithum'''
        #Uses Spotify's search to look through the main file for the song requested, then adds that song to play next 
        songsFile = open("Songs\\masterSongFile", "r")
        masterLines = songsFile.readlines()

        while True:
            songQuery = simpledialog.askstring("Delete Songs", "Please enter the song you would like to delete")
            if songQuery == None:
                return
            found = False
            # Searching for the song
            for track in self.searchForBestSong(songQuery)["tracks"]["items"]:
                for index, line in enumerate(masterLines):
                    if track["external_urls"]["spotify"] in line:
                        theLineindex = index
                        theSong = track["name"]
                        theUrl = track["external_urls"]["spotify"]
                        found = True
            if found:
                areYouSure = messagebox.askyesno("Delete Songs", "Are you sure you want to delete the song \"" + theSong + "\"?")
                if areYouSure:
                    break
            else:
                messagebox.showinfo("Search", "No saved song was found using the query: \"" + songQuery + "\". try narrowing it down by searching with the author as well.")

        masterLines.pop(theLineindex)
        
        songsFile = open("Songs\\masterSongFile", "w")
        songsFile.writelines(masterLines)
        songsFile.close()


        if not messagebox.askyesno("Delete Songs", theSong + " has been removed. Would you also like to delete the mp3/ogg file?"):
            return
        
        try:
            song_path = "Songs\\LocalSongsOGG\\" + self.sanitizeFilename(theUrl) + ".ogg"
            os.remove(song_path)
        except:
            pass
        messagebox.showinfo("Delete Songs", theSong + " has been removed.")

    def remakeSongsInPlaylist(self, playlistURL):
        '''Deletes all songs from the given playlist'''
        if not self.isValidPlaylist():
            messagebox.showerror("Invalid Input", "Please enter a valid playlist in the provided box")
            return

        if not messagebox.askyesno("Delete Songs", "Are you sure that you want to delete the song timings for all songs from the playlist " + self.playlistURLToFileName(playlistURL) + "?"):
            return
        
        # Creates a list of new songs
        tracks = self.spotifyClient.playlist_tracks(playlistURL)['items']

        # Extract track URLs
        urls = []
        for track in tracks:
            if track["track"]:
                urls.append(track["track"]["external_urls"]["spotify"])

        # Deletes all lines that match any url of the playlist
        masterSongFile = open("Songs\\masterSongFile", "r")
        masterLines = masterSongFile.readlines()
        masterSongFile.close()

        masterSongFile = open("Songs\\masterSongFile", "w")

        # If a line doesnt contain any of the deleted urls, add it back
        for line in masterLines:
            found = False
            for url in urls:
                if url in line:
                    found = True
                    break

            if not found:
                masterSongFile.write(line)

        if not messagebox.askyesno("Delete Songs", "The song timings have been removed. Would you also like to delete the mp3/ogg file?"):
            return
        
        # Gets the place where the songs are stored
        localSongsDir = "Songs\\LocalSongsOGG"

        # Removes every song file that has a url we want to delete
        for file in os.listdir(localSongsDir):
            for url in urls:
                if self.sanitizeFilename(url) in file:
                    try:
                        song_path = "Songs\\LocalSongsOGG\\" + self.sanitizeFilename(url) + ".ogg"
                        os.remove(song_path)
                    except:
                        pass
                    break
        messagebox.showinfo("Delete Songs", "All songs from " + self.playlistURLToFileName(playlistURL) + " have been removed.")


    def deleteSongFile(self):
        '''Deletes the contents of the masterSongFile'''
        open("Songs\\masterSongFile", "w").close()

    def removeHotkeys(self):
        '''Removes any hotkeys'''
        keyboard.remove_all_hotkeys()

    def resetRounds(self):
        '''Resets the rounds and pauses playback'''
        mixer.music.fadeout(5000)
        self.roundNumber = 1

    def playSong(self, url, fade = 0):
        '''Plays a song using pygame mixer given the url and how long you want the fade to be'''
        song_path = "Songs\\LocalSongsOGG\\" + self.sanitizeFilename(url) + ".ogg"
        mixer.music.load(song_path)

        mixer.music.play(loops = -1, fade_ms = fade)
    
    def setVolumeHigh(self):
        '''Sets the volume to the high volume'''
        settingFile = open("Config\\settings", "r")
        fileLines = settingFile.readlines()
        settingFile.close()
        volume = int(fileLines[0][0:3])
        mixer.music.set_volume(volume / 100)

    def setVolumeLow(self):
        '''Sets the volume to the low volume'''
        settingFile = open("Config\\settings", "r")
        fileLines = settingFile.readlines()
        settingFile.close()
        volume = int(fileLines[0][3:6])
        mixer.music.set_volume(volume / 100)

    def getVolumeHigh(self):
        '''Gets the volume from the settings'''
        settingFile = open("Config\\settings", "r")
        fileLines = settingFile.readlines()
        settingFile.close()
        return float(fileLines[0][0:3]) // 100

    def getVolumeLow(self):
        '''Gets the volume from the settings'''
        settingFile = open("Config\\settings", "r")
        fileLines = settingFile.readlines()
        settingFile.close()
        return float(fileLines[0][3:6]) // 100

    def pausePlay(self):
        '''Pauses music if it is playing and plays music if it is paused with a debounce'''

        if time.time() - self.lastPauseTime < 0.5:
            return
        self.lastPauseTime = time.time()
        if mixer.music.get_busy():
            mixer.music.pause()
        else:
            mixer.music.unpause()
    def unloadSong(self):
        '''Unloads they current song to be able to delete it'''
        mixer.music.unload()

    def setNextSong(self, set):
        '''Sets the next song'''
        self.nextSongs.append(set)

    def getNextSongs(self):
        '''Gets a list of the next songs'''
        return self.nextSongs[:]
    
    def downloadSong(self, url):
        '''Downloads the song specified by query using spotdl and the command line, if the song already exists then return None'''      
        
        # Looks in the current working directory for the song file and spotdl
        cwd = os.getcwd()
        cwdUser = cwd[:cwd[9:].find("\\") + 9]

        spotdlPath = cwdUser + "\\AppData\\Roaming\\Python\\Python313\\Scripts\\spotdl.exe"
        outputPath = cwd + "\\Songs\\LocalSongsOGG"
        fileName = self.sanitizeFilename(url) + ".ogg"
        
        # if file already exists
        for file in os.listdir(outputPath):
            if file == fileName:
                return
        try:
            try:
                subprocess.run([spotdlPath, url, "--format", "ogg", "--output", outputPath], check=True)
            except FileNotFoundError:
                try:
                    subprocess.run([spotdlPath.replace("Roaming", "Local\\Programs"), url, "--format", "ogg", "--output", outputPath], check=True)
                except Exception as e:
                    messagebox.showerror("Your spotdl is installed in the wrong place. Make sure it is installed under \\AppData\\Roaming\\Python\\Python313\\Scripts\\spotdl.exe\nOr under \\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\spotdl.exe")
                    return False

            # Finding and renaming the file
            newFilePath = os.path.join(outputPath, fileName) 

            # List all files in the directory
            ogg_files = os.listdir(outputPath)

            # Find the most recently modified file
            latest_file = None
            latest_mtime = 0

            # Loop through the filtered ogg files to find the one with the most recent modification
            for file in ogg_files:
                file_path = os.path.join(outputPath, file)
                file_mtime = os.path.getmtime(file_path)

                if file_mtime > latest_mtime:
                    latest_mtime = file_mtime
                    latest_file = file

            # Return the path of the most recently modified file, the one we just downloaded
            downloadedFilePath = os.path.join(outputPath, latest_file)

            # If the most recent downloaded song is already named then it is not the new unrenamed song
            if "https___open.spotify.com_track_" in downloadedFilePath:
                messagebox.showerror("Error Downloading", "Error Downloading " + url + ", SpotDL can't find this song code 1")
                return False

            os.rename(downloadedFilePath, newFilePath)

            return True
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error Downloading", "Error Downloading " + url + ", SpotDL can't find this song")
            return False
        
if __name__ == "__main__":
    '''
    # Testing pygame.mixer
    startTime = time.time()
    mixer.init()

    print("init time: ", time.time() - startTime)
    startTime = time.time()

    mixer.music.load("Songs\\LocalSongsOGG\\TestSong.ogg")

    print("load time: ", time.time() - startTime)
    # startTime = time.time()

    mixer.music.play(loops = -1, fade_ms = 5000)

    print("play time: ", time.time() - startTime)
    # startTime = time.time()

    mixer.music.set_pos(0)

    print("setp time: ", time.time() - startTime)
    startTime = time.time()

    time.sleep(7)
    
    startTime = time.time()
    mixer.music.unload()

    print("unlo time: ", time.time() - startTime)'
    '''
    # spotifyIntern = SpotifyInteractor(1920, 1080)
    # spotifyIntern.downloadSavedSongs()