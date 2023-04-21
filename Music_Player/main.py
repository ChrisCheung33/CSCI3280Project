import shutil
import tkinter as tk
import fnmatch
import struct
import os
import numpy as np
import simpleaudio as sa
import database
import soundfile as sf
from io import BytesIO
from PIL import ImageTk, Image

#design of the UI of the music player
canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("880x800")
canvas.config(bg = 'white')
canvas.resizable(True, True)

#file for music
rootpath = "./music/"#path for the music play list
pattern = "*.wav"

prev_image = tk.PhotoImage(file = "./images/prev.png")
stop_image = tk.PhotoImage(file = "./images/stop.png")
play_image = tk.PhotoImage(file = "./images/play.png")
pause_image = tk.PhotoImage(file = "./images/pause.png")
next_image = tk.PhotoImage(file = "./images/next.png")
add_image = tk.PhotoImage(file = "./images/add.png")

play_obj = None

#action for the play button: to select a song to be play
def select():
    sa.stop_all()
    label.config(text = listBox.get("anchor"))
    playmusic(rootpath + listBox.get("anchor"))
    show_lyrics(rootpath + listBox.get("anchor"))
    show_art(rootpath + listBox.get("anchor"))
    
#action for the stop button: to clear a song when it is activated
def stop():
    # play_obj.stop()
    sa.stop_all()
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
        pauseButton["text"] = "Play"
    else:
        play_obj.resume()
        pauseButton["text"] = "Pause"

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
    bytes_per_sample = bits_per_sample // 8
    if bits_per_sample == 16:
        data_type = np.int16
    elif bits_per_sample == 8:
        data_type = np.int8
    elif bits_per_sample == 24:
        data, sample_rate = sf.read(file_path)
        sf.write(file_path, data, sample_rate, subtype='PCM_16')
        playmusic(file_path)
        return
    else:
        raise ValueError('File has unsupported bit depth.')
    
    audio_array = np.frombuffer(raw_data, dtype=data_type)
        

    # Reshape the array for stereo audio
    if num_channels == 2:
        audio_array = audio_array.reshape(-1, 2)

    global play_obj
    play_obj = sa.play_buffer(audio_array, num_channels, 2, sample_rate)
    # play_obj = sd.play(audio_array, sample_rate)

def add_song():
    database.load_from_csv(database.database_path)
    song = database.upload_wav()
    print("Song: " + song)
    destination_file = save_wav(song)
    # remove the music/ part of the path
    destination_file = destination_file[6:]
    database.save_to_csv(database.database_path)
    # listBox.insert('end', destination_file)
    listBox.delete('0','end')
    read_file(rootpath, pattern)

# save a .wav file to the music folder
def save_wav(file_path):
    directory = "music"
    if not os.path.exists(directory):
        print("Creating directory " + directory + "...")
        os.makedirs(directory)

    print("Copying file to " + directory + "...")
    print("File path: " + file_path)
    source_file = file_path
    filename = os.path.basename(source_file)
    destination_file = os.path.join(directory, filename)

    shutil.copy2(source_file, destination_file)
    return destination_file

listBox = tk.Listbox(canvas, fg = "cyan", bg = "white", width = 100, font = ('poppins',14))
listBox.pack(padx = 15, pady = 15)

music_info = tk.Frame(canvas, bg = "black")
music_info.pack(padx = 15, pady = 15, anchor = 'center')

label = tk.Label(canvas, text = '', bg = 'black', fg = 'yellow', font = ('poppins',14))
label.pack(pady = 15, side='left', in_ = music_info)

TARGET_SIZE = (128, 128)
loaded_img = Image.open("./images/art.jpeg")
resized_img = loaded_img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(resized_img)
panel = tk.Label(canvas, image = img)
panel.image = img
panel.pack(side = "left", in_ = music_info, fill = "both", expand = "yes")

lyricsText = tk.Text(canvas, bg = 'black', fg = 'yellow', font = ('poppins',14), width = 100, height = 10)
lyricsText.pack(padx = 15, pady = 15)

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

# Button for add song
addButton = tk.Button(canvas, text = 'Add', image = add_image, bg = 'black', borderwidth = 0, command = add_song)
addButton.pack(pady = 15, in_ = top, side = 'left')

#read the file
def read_file(rootpath, pattern):
    filename_list = []
    for root, dirs, files in os.walk(rootpath):
        for filename in fnmatch.filter(files, pattern):
            filename_list.append(filename)

    filename_list.sort()
    for filename in filename_list:
        listBox.insert('end', filename)


read_file(rootpath, pattern)

# show lyrics of the song in the text box
def show_lyrics(song):
    # get the lyrics of the song
    lyrics = database.get_lyrics(song)
    # show the lyrics in the text box
    lyricsText.delete('1.0', 'end')
    lyricsText.insert('1.0', lyrics)

def show_art(file_path):
        album_art = database.get_album_art(file_path)
        if album_art is None:
            print("No album art found")
            return
        album_art_data = album_art.data
        # album_art_format = album_art.mime.split('/')[1]

        loaded_img = Image.open(BytesIO(album_art_data))
        # loaded_img = Image.open("./images/art.jpeg")
        resized_img = loaded_img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(resized_img)
        panel.config(image = img)
        panel.image = img

canvas.mainloop()