import tkinter as tk
from tkinter import *

window = tk.Tk()
window.title("settings")
window.geometry('1280x650')

bgImage = PhotoImage(file = "ValorantBG.gif")

settingsCanvas = Canvas(window, width = 1280, height = 700)
settingsCanvas.pack(fill = "both", expand = True)

settingsCanvas.create_image(0, 0, image = bgImage, anchor = "nw")

settingsCanvas.create_text(640, 200, text = "Volume", font = ("Helvetica", 30), fill = "orange")

volumeScale = Scale(window, from_ = 0, to_ = 100, orient=tk.HORIZONTAL, resolution = 1)
confirmButton = Button(window, text = "Save")

volumeScaleWindow   = settingsCanvas.create_window(640, 300, window = volumeScale)
confirmButtonWindow = settingsCanvas.create_window(640, 600, window = confirmButton)

window.mainloop()