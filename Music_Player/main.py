import shutil
import tkinter as tk
import tkinter.ttk as ttk
import fnmatch
import struct
import os
import numpy as np
import simpleaudio as sa
import database
import soundfile as sf
from io import BytesIO
from PIL import ImageTk, Image
import ast

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

    # get the selected song from the treeview
    selected_song = tree.focus()
    selected_song_name = tree.item(selected_song)['values'][0]
    selected_song_path = database.get_filename(selected_song_name)
    
    playmusic(rootpath + selected_song_path)

    
#action for the stop button: to clear a song when it is activated
def stop():
    sa.stop_all()
    label.config(text = "Choose a song to play")
    show_art("")
    tree.selection_remove(tree.focus())
    canvas.focus()

#action for the next button: to select the next song, by adding 1 to the current playing song
def play_next():
    selected_item = tree.selection()
    if selected_item:
        next_item = tree.index(selected_item[0]) + 1
        if next_item < len(tree.get_children()):
            tree.focus(tree.get_children()[next_item])
            tree.selection_set(tree.get_children()[next_item])
        else:
            tree.focus(tree.get_children()[0])
            tree.selection_set(tree.get_children()[0])

    selected_song = tree.focus()
    selected_song_name = tree.item(selected_song)['values'][0]
    selected_song_path = database.get_filename(selected_song_name)

    play_obj.stop()
    playmusic(rootpath + selected_song_path)


#action for the prev button: to select the previous song, by minus 1 to the current playing song
def play_prev():
    selected_item = tree.selection()
    if selected_item:
        next_item = tree.index(selected_item[0]) - 1
        if next_item >= 0:
            tree.focus(tree.get_children()[next_item])
            tree.selection_set(tree.get_children()[next_item])
        else:
            tree.focus(tree.get_children()[-1])
            tree.selection_set(tree.get_children()[-1])

    selected_song = tree.focus()
    selected_song_name = tree.item(selected_song)['values'][0]
    selected_song_path = database.get_filename(selected_song_name)

    play_obj.stop()
    playmusic(rootpath + selected_song_path)

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
        audio = sf.SoundFile(file_path)

        keys = list(audio.copy_metadata().keys())
        print(keys)
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
    filename = os.path.basename(file_path)
    label.config(text = "Now playing: " + database.get_title(filename))
    show_lyrics(file_path)
    show_art(file_path)


def add_song():
    database.load_from_csv(database.database_path)
    song = database.upload_wav()
    print("Song: " + song)
    destination_file = save_wav(song)
    # remove the music/ part of the path
    destination_file = destination_file[6:]
    database.save_to_csv(database.database_path)
    for row in tree.get_children():
        tree.delete(row)
    read_file_to_treeview(rootpath, pattern)

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

tree = ttk.Treeview(canvas, columns = ("Name", "Artist", "Album", "Time"), show = "headings", height = "5")
tree.heading("Name", text = "Name")
tree.heading("Artist", text = "Artist")
tree.heading("Album", text = "Album")
tree.heading("Time", text = "Time")
tree.pack(padx = 15, pady = 15)

music_info = tk.Frame(canvas, bg = "black")
music_info.pack(padx = 15, pady = 15, anchor = 'center')

label = tk.Label(music_info, text = 'Choose a song to play', bg = 'black', fg = 'yellow', font = ('poppins',14))
label.pack(pady = 15, side='top')

TARGET_SIZE = (128, 128)
loaded_img = Image.open("./images/art.jpeg")
resized_img = loaded_img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(resized_img)
panel = tk.Label(music_info, image = img)
panel.image = img
panel.pack(side = "left", fill = "both", expand = "yes")

lyricsText = tk.Text(music_info, bg = 'black', fg = 'yellow', font = ('poppins',14), width = 100, height = 10)
lyricsText.pack(padx = 15, pady = 15, side = 'right')

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

def read_file_to_treeview(rootpath, pattern):
    filename_list = []
    for root, dirs, files in os.walk(rootpath):
        for filename in fnmatch.filter(files, pattern):
            filename_list.append(os.path.basename(filename))

    filename_list.sort()
    print(filename_list)
    for filename in filename_list:
        # get the name of the song
        name = database.music_df.loc[database.music_df['filename'] == filename, 'title'].values[0]
        # get the artist of the song
        artist = database.music_df.loc[database.music_df['filename'] == filename, 'artist'].values[0]
        # get the album of the song
        album = database.music_df.loc[database.music_df['filename'] == filename, 'album'].values[0]
        # get the time of the song
        time = database.music_df.loc[database.music_df['filename'] == filename, 'length'].values[0]
        # insert the song in the treeview
        tree.insert("", "end", values = (name, artist, album, database.get_format_length(time)))



# show lyrics of the song in the text box
def show_lyrics(song):
    # get filename without the extension
    song = os.path.basename(song)
    print(song)
    # get the lyrics of the song
    lyrics = database.music_df.loc[database.music_df['filename'] == song, 'lyrics'].values[0]
    # show the lyrics in the text box
    lyricsText.delete('1.0', 'end')
    lyricsText.insert('1.0', lyrics)

def show_art(file_path):
        # get filename without the extension

        song = os.path.basename(file_path)
        try:
            album_art_data = database.music_df.loc[database.music_df['filename'] == song, 'album_art'].values[0]
        except:
            album_art_data = None

        if album_art_data is None:
            loaded_img = Image.open("./images/art.jpeg")
        else:
            loaded_img = Image.open(BytesIO(ast.literal_eval(album_art_data)))

        resized_img = loaded_img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(resized_img)
        panel.config(image = img)
        panel.image = img

database.load_from_csv(database.database_path)
read_file_to_treeview(rootpath, pattern)

canvas.mainloop()