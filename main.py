import tkinter
from tkinter import ttk
from tkinter import *
import sv_ttk
import extra_functions
import face_detect


root = tkinter.Tk()
root.geometry("1080x720")

canvas=Canvas(root, width=1080, height=720) # line creation in background
canvas.pack()

canvas.create_line(360,0,360,720, fill="white", width=2)
canvas.create_line(0, 300, 360, 300, fill="white", width=2)
canvas.create_line(0, 620, 360, 620, fill="white", width=2)


filters_text = Label(root, text="Filters Selection", font=("Courier", 16))
filters_text.place(x=63,y=5)

# modal options for different filters 
mode1_button = ttk.Button(root, text="Mode 1")
mode1_button.place(x=75, y=50)

mode2_button = ttk.Button(root, text="Mode 2")
mode2_button.place(x=200, y=50)

mode3_button = ttk.Button(root, text="Mode 3")
mode3_button.place(x=75, y=125)

mode4_button = ttk.Button(root, text="Mode 4")
mode4_button.place(x=200, y=125)


help_hypertext = Label(root, text="need help?", font=("Courier", 10, 'underline'))
help_hypertext.place(x=135, y=190)
help_hypertext.bind("<Button-1>", lambda e: extra_functions.callback("http://www.google.com"))

app = face_detect.FacialRecognitionApp(root)

# copy clipboard panel
copy_clipboard = Label(root, text="Copy to clipboard", font=("Courier", 10, 'underline'))
copy_clipboard.place(x=105, y=660)
copy_clipboard.bind("<Button-1>", lambda e: extra_functions.callback("http://www.google.com"))

# This is where the magic happens
sv_ttk.set_theme("dark")
root.mainloop() #hear event loops


