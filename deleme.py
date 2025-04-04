import os
import tkinter as tk
from tkinter import ttk
import time
from threading import Thread

# Function to simulate song downloading and update the progress bar
def download_songs(progress_bar, song_list):
    total_songs = len(song_list)
    current_song = 0

    for song in song_list:
        # Simulate the download process (spotdl logic should be here)
        # You need to replace this with actual code that downloads with spotdl
        # and tracks progress
        for i in range(101):
            progress_bar['value'] = i
            window.update_idletasks()
            time.sleep(0.05)  # Simulate downloading for 5 seconds

        current_song += 1
        progress_bar['value'] = (current_song / total_songs) * 100
        window.update_idletasks()

    # Once done, inform user
    progress_label.config(text="Download Complete!")

def start_download():
    song_list = ['song1', 'song2', 'song3']  # List of songs (Replace with actual data)
    thread = Thread(target=download_songs, args=(progress_bar, song_list))
    thread.start()

# Tkinter Setup
window = tk.Tk()
window.title("Song Downloader")

# Label to show progress
progress_label = tk.Label(window, text="Downloading songs...", font=("Arial", 14))
progress_label.pack(pady=20)

# Progress bar
progress_bar = ttk.Progressbar(window, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(pady=10)

# Start download button
start_button = tk.Button(window, text="Start Download", command=start_download)
start_button.pack(pady=20)

# Run the Tkinter event loop
window.mainloop()
