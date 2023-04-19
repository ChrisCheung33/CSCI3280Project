import tkinter as tk
import fnmatch
import struct
import os
import numpy as np
import simpleaudio as sa

#design of the UI of the music player
canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("800x800")
canvas.config(bg = 'white')

#file for music
rootpath = "./music/"#path for the music play list
pattern = "*.wav"

prev_image = tk.PhotoImage(file = "prev.png")
stop_image = tk.PhotoImage(file = "stop.png")
play_image = tk.PhotoImage(file = "play.png")
pause_image = tk.PhotoImage(file = "pause.png")
next_image = tk.PhotoImage(file = "next.png")

play_obj = None

#action for the play button: to select a song to be play
def select():
    label.config(text = listBox.get("anchor"))
    playmusic(rootpath + listBox.get("anchor"))
    
#action for the stop button: to clear a song when it is activated
def stop():
    play_obj.stop()
    listBox.select_clear('active') 

#action for the next button: to select the next song, by adding 1 to the current playing song
def play_next():
    next_song = listBox.curselection()
    next_song = next_song[0] + 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)
    play_obj.stop()
    playmusic(rootpath + next_song_name)
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
#action for the prev button: to select the previous song, by minus 1 to the current playing song
def play_prev():
    next_song = listBox.curselection()
    next_song = next_song[0] - 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)
    play_obj.stop()
    playmusic(rootpath + next_song_name)
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
#action for the pause button: to pause the song when it is playing and unpuase it  when it is paused
def pause_song():
    if pauseButton["text"] == "Pause":
        play_obj.pause()
        pauseButton["text"] == "Play"
    else:
        play_obj.resume()
        pauseButton["text"] == "Pause"

def playmusic(file_path):
    with open(file_path, 'rb') as wave_file:
        # Check that the file is a WAV file
        riff_chunk_id = wave_file.read(4)
        riff_chunk_size = struct.unpack('<I', wave_file.read(4))[0]
        riff_format = wave_file.read(4)
        if riff_chunk_id != b'RIFF' or riff_format != b'WAVE':
            raise ValueError('File is not a WAV file.')

        # Read the header information
        fmt_chunk_id = wave_file.read(4)
        fmt_chunk_size = struct.unpack('<I', wave_file.read(4))[0]
        audio_format = struct.unpack('<H', wave_file.read(2))[0]
        num_channels = struct.unpack('<H', wave_file.read(2))[0]
        sample_rate = struct.unpack('<I', wave_file.read(4))[0]
        byte_rate = struct.unpack('<I', wave_file.read(4))[0]
        block_align = struct.unpack('<H', wave_file.read(2))[0]
        bits_per_sample = struct.unpack('<H', wave_file.read(2))[0]

        # Verify that the audio format is PCM
        if audio_format != 1:
            raise ValueError('File is not in PCM format.')

        # Read the data chunk
        data_chunk_id = wave_file.read(4)
        data_chunk_size = struct.unpack('<I', wave_file.read(4))[0]
        raw_data = wave_file.read(data_chunk_size)

    # Convert raw byte data to NumPy array with proper data type
    if bits_per_sample == 16:
        data_type = np.int16
    elif bits_per_sample == 8:
        data_type = np.int8
    else:
        raise ValueError('File has unsupported bit depth.')
    audio_array = np.frombuffer(raw_data, dtype=data_type)

    # Reshape the array for stereo audio
    if num_channels == 2:
        audio_array = audio_array.reshape(-1, 2)

    global play_obj
    play_obj = sa.play_buffer(audio_array, num_channels, 2, sample_rate)

    


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
pauseButton = tk.Button(canvas, text = 'Pause', image = pause_image, bg = 'black', borderwidth = 0, command = pause_song)
pauseButton.pack(pady = 15, in_ = top, side = 'left')

#Button for next song
nextButton = tk.Button(canvas, text = 'Next', image = next_image, bg = 'black', borderwidth = 0, command = play_next)
nextButton.pack(pady = 15, in_ = top, side = 'left')

#read the file
for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        listBox.insert('end', filename)


canvas.mainloop()