import tkinter as tk
import fnmatch
import struct
import os
from pygame import mixer
import numpy as np
import simpleaudio as sa

#design of the UI of the music player
canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("600x800")
canvas.config(bg = 'white')

#file for music
rootpath = "./music/"#path for the music play list
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
    # Window
    # mixer.music.load(rootpath + "//" +listBox.get("anchor")
    # Mac/linux
    mixer.music.load(rootpath + listBox.get("anchor"))
    # mixer.music.play()
    play(rootpath + listBox.get("anchor"))
#action for the stop button: to clear a song when it is activated
def stop():
    mixer.music.stop()
    listBox.select_clear('active') 
#action for the next button: to select the next song, by adding 1 to the current playing song
def play_next():
    next_song = listBox.curselection()
    next_song = next_song[0] + 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)
    # Window
    # mixer.music.load(rootpath + "\\" + next_song_name)
    # Mac/linux
    mixer.music.load(rootpath + next_song_name)
    # mixer.music.play()
    play()
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
#action for the prev button: to select the previous song, by minus 1 to the current playing song
def play_prev():
    next_song = listBox.curselection()
    next_song = next_song[0] - 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)

    # Window
    # mixer.music.load(rootpath + "\\" + next_song_name)
    # Mac/linux
    mixer.music.load(rootpath + next_song_name)

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

def play(filename):
    print("Now Playing Music:",filename)
    # Open the wav file
    with open(filename, 'rb') as f:
        # Read the RIFF header
        riff_header = f.read(12)
        # Read the fmt subchunk
        fmt_header = f.read(8)
        fmt_size = struct.unpack('<I', fmt_header[4:8])[0]
        fmt_data = f.read(fmt_size)
        # Get the sample rate and number of channels
        sample_rate, n_channels = struct.unpack('<2I', fmt_data[4:12])
        # Read the data subchunk
        data_header = f.read(8)
        data_size = struct.unpack('<I', data_header[4:8])[0]
        data = f.read(data_size)
    # Convert data to numpy array
    np_data = np.frombuffer(data, dtype=np.int16)
    # Normalize data
    np_data = np_data / np.iinfo(np.int16).max
    print(np_data)
    # Set n_channels to 2 (stereo)
    n_channels = 2
    # Play the audio using simpleaudio's play_buffer function
    play_obj = sa.play_buffer(np_data, n_channels, 2, sample_rate)
    # play_obj.wait_done()

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