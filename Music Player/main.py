import tkinter as tk
import fnmatch
import os
from pygame import mixer

#design of the UI of the music player
canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("800x800")
canvas.config(bg = 'white')

#file for music
rootpath = "C:\\"#path for the music play list
pattern = "*.wav"

mixer.init()
prev_image = tk.PhotoImage(file = "prev.png")
stop_image = tk.PhotoImage(file = "stop.png")
play_image = tk.PhotoImage(file = "play.png")
pause_image = tk.PhotoImage(file = "pause.png")
next_image = tk.PhotoImage(file = "next.png")

#action for the play button: to select a song to be play
def select():
    label.config(text = listBox.get("anchor"))
    mixer.music.load(rootpath + "\\" + listBox.get("anchor"))
    mixer.music.play()
#action for the stop button: to clear a song when it is activated
def stop():
    mixer.music.stop()
    listBox.select_clear('active') 
#action for the next button: to select the next song, by adding 1 to the current playing song
def play_next():
    next_song = list.curselection()
    next_song = next_song[0] + 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)
    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
#action for the prev button: to select the previous song, by minus 1 to the current playing song
def play_prev():
    next_song = list.curselection()
    next_song = next_song[0] - 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)
    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
#action for the pause button: to pause the song when it is playing and unpuase it  when it is paused
def pause_song():
    if pauseButton["text"] == "Pause":
        mixer.music.pause()
        pauseButton["text"] == "Play"
    else:
        mixer.music.unpause()
        pauseButton["text"] == "Pause"

listBox = tk.Listbox(canvas, fg = "cyan", bg = "white", width = 100, font = ('poppins',14))
listBox.pack(padx = 15, pady = 15)

label = tk.Label(canvas, text = '', bg = 'black', fg = 'yellow', font = ('poppins',14))
label.pack(pady = 15)

top = tk.Frame(canvas, bg = "black")
top.pack(padx = 15, pady = 15, anchor = 'center')

#Button for previous song
prevButton = tk.Button(canvas, text = 'Prev', image = prev_image, bg = 'black', borderwidth = 0, command= play_prev)
prevButton.pack(pady = 15, in_ = top, side = 'left')

#Button for stop song
stopButton = tk.Button(canvas, text = 'Stop', image = stop_image, bg = 'black', borderwidth = 0, command = stop)
stopButton.pack(pady = 15, in_ = top, side = 'left')

#Button for play song
playButton = tk.Button(canvas, text = 'Play', image = play_image, bg = 'black', borderwidth = 0, command = select)
playButton.pack(pady = 15, in_ = top, side = 'left')

#Button for pause song
pauseButton = tk.Button(canvas, text = 'Pause', image = stop_image, bg = 'black', borderwidth = 0, command = pause_song)
pauseButton.pack(pady = 15, in_ = top, side = 'left')

#Button for next song
nextButton = tk.Button(canvas, text = 'Next', image = next_image, bg = 'black', borderwidth = 0, command = play_next)
nextButton.pack(pady = 15, in_ = top, side = 'left')

#read the file
for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        listBox.insert('end', filename)


canvas.mainloop()