import shutil
import threading
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

from scipy.io import wavfile

from pygame import mixer

# COLOR = ['#FFFBEB', '#495579', '#263159', '#251749']
COLOR = ['#2C3639', '#3F4E4F', '#A27B5C', '#DCD7C9']

#design of the UI of the music player
canvas = tk.Tk()
canvas.attributes("-fullscreen", True)
canvas.title("Music Player")
# canvas.geometry("1000x800")
canvas.config(bg = COLOR[1])
canvas.resizable(True, True)

s = ttk.Style()
s.theme_use('clam')
# s.theme_use('classic')
# s.theme_use('default')
# s.theme_use('alt')
s.configure("blue.Horizontal.TProgressbar", foreground=COLOR[2], background=COLOR[2], troughcolor=COLOR[3],)
s.configure('Treeview', rowheight=40)

#file for music
rootpath = "./music/"#path for the music play list
pattern = "*.wav"

play_obj = None

song_length = 0

#action for the play button: to select a song to be play
def select():
    
    if play_obj:
        play_obj.stop()
        mixer.quit()

    # get the selected song from the treeview
    selected_song = tree.focus()
    selected_song_name = tree.item(selected_song)['values'][0]
    selected_song_path = database.get_filename(selected_song_name)
    
    global song_length
    song_length = database.get_length(rootpath + selected_song_path)

    # playmusic(rootpath + selected_song_path)
    play_thread = threading.Thread(target=playmusic, args=(rootpath + selected_song_path,), daemon=True)
    play_thread.start()
    
    
#action for the stop button: to clear a song when it is activated
def stop():
    if play_obj:
        play_obj.stop()
    label.config(text = "Choose a song to play")
    show_lyrics("")
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

    select()


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

    select()
    

def startpb():
    pb.start(int(song_length * 10))

#action for the pause button: to pause the song when it is playing and unpuase it  when it is paused
def pause_song():
    if pauseButton["text"] == "Pause" and mixer.get_busy():
        pauseButton['image'] = play_image
        mixer.pause()
        pbCurrent = pb['value']
        pb.stop()
        pb.config(value=pbCurrent)
        pauseButton["text"] = "Play"
    elif pauseButton["text"] == "Play" and mixer.get_busy():
        pauseButton['image'] = pause_image
        mixer.unpause()
        start_thread = threading.Thread(target=startpb, daemon=True)
        start_thread.start()
        pauseButton["text"] = "Pause"

def playmusic(file_path):
    if mixer.get_busy():
        pause_song()

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
        # data_chunk_id = wave_file.read(4)
        # data_chunk_size = struct.unpack('<I', wave_file.read(4))[0]
        # raw_data = wave_file.read(data_chunk_size)
        sample_rate, raw_data = wavfile.read(file_path)

    # Convert raw byte data to NumPy array with proper data type
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
        try:
            print("Trying to reshape")
            audio_array = audio_array.reshape(-1, 2)
        except:
            print("Reshaping failed")
            print(audio_array.shape)

    global play_obj
    # play_obj = sa.play_buffer(audio_array, num_channels, 2, sample_rate)
    mixer.init(sample_rate, -bits_per_sample, num_channels, 1024)
    # load audio_array into mixer
    play_obj = mixer.Sound(audio_array)
    play_obj.play()
    change_vol()

    # playButton['image'] = replay_image

    # play_obj = mixer.music.load(file_path)
    filename = os.path.basename(file_path)
    label.config(text = "Now playing: " + database.get_title(filename))
    show_lyrics(file_path)
    show_art(file_path)

    # get length of the song
    data, samplerate = sf.read(file_path)
    length = len(data) / samplerate

    pb.start(int(10 * length))

    # play_obj.wait_done()
    while(mixer.get_busy()):
        pass

    pb.stop()
    # playButton['image'] = play_image


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

# let the user to edit the information like the name of the song, artist and album and store it in the database
def edit_song():
    # get the selected song
    selected = tree.selection()
    # get the title of the selected song
    name = tree.item(selected, 'values')[0]
    # get the filename of the song
    filename = database.get_filename(name)
    # get the artist of the song
    artist = database.music_df.loc[database.music_df['filename'] == filename, 'artist'].values[0]
    # get the album of the song
    album = database.music_df.loc[database.music_df['filename'] == filename, 'album'].values[0]
    
    # create a new window
    editWindow = tk.Toplevel()
    editWindow.title("Edit")
    editWindow.geometry("400x200")
    editWindow.resizable(False, False)
    editWindow.configure(bg = COLOR[1])
    # create a frame
    editFrame = tk.Frame(editWindow, bg = COLOR[1])
    editFrame.pack(padx = 15, pady = 15, anchor = 'center')
    # create a label for the name of the song
    nameLabel = tk.Label(editFrame, text = "Name", bg = COLOR[1], fg = COLOR[3], font = ("poppins", 14))
    nameLabel.grid(row = 0, column = 0, padx = 5, pady = 5)
    # create a label for the artist of the song
    artistLabel = tk.Label(editFrame, text = "Artist", bg = COLOR[1], fg = COLOR[3], font = ("poppins", 14))
    artistLabel.grid(row = 1, column = 0, padx = 5, pady = 5)
    # create a label for the album of the song
    albumLabel = tk.Label(editFrame, text = "Album", bg = COLOR[1], fg = COLOR[3], font = ("poppins", 14))
    albumLabel.grid(row = 2, column = 0, padx = 5, pady = 5)
    # create an entry for the name of the song
    nameEntry = tk.Entry(editFrame, width = 30, bg = COLOR[1], fg = COLOR[3], font = ("poppins", 14))
    nameEntry.grid(row = 0, column = 1, padx = 5, pady = 5)
    nameEntry.insert(0, name)
    # create an entry for the artist of the song
    artistEntry = tk.Entry(editFrame, width = 30, bg = COLOR[1], fg = COLOR[3], font = ("poppins", 14))
    artistEntry.grid(row = 1, column = 1, padx = 5, pady = 5)
    artistEntry.insert(0, artist)
    # create an entry for the album of the song
    albumEntry = tk.Entry(editFrame, width = 30, bg = COLOR[1], fg = COLOR[3], font = ("poppins", 14))
    albumEntry.grid(row = 2, column = 1, padx = 5, pady = 5)
    albumEntry.insert(0, album)

    # create a button for save the changes
    saveButton = tk.Button(editFrame, text = "Save", bg = COLOR[0], fg = COLOR[1], font = ("poppins", 14), command = lambda: save_changes(filename, nameEntry.get(), artistEntry.get(), albumEntry.get(), editWindow))
    saveButton.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 5)


def save_changes(filename, title, artist, album, editWindow):
    # get the selected song
    selected = tree.selection()
    
    # update the database
    database.update_music(filename, title, album, artist)

    length = database.get_format_length(database.music_df.loc[database.music_df['filename'] == filename, 'length'].values[0])
    
    # update the treeview
    tree.item(selected, values = (title, artist, album, length))

    # close the window
    editWindow.destroy()

# search for songs in the database and show them in the treeview
# the search is case insensitive
# the search is done by the title, artist and album
def search():
    # get the text from the search bar
    search = searchBar.get()
    # clear the treeview
    for row in tree.get_children():
        tree.delete(row)
    # get the songs that match the search
    search_result = database.search(search)
    # add the songs to the treeview
    for index, row in search_result.iterrows():
        tree.insert("", "end", values = (row['title'], row['artist'], row['album'], database.get_format_length(row['length'])))

def change_vol(_=None):
    play_obj.set_volume(vol.get() / 100)

# create a main frame
mainFrame = tk.Frame(canvas, bg = COLOR[3])
mainFrame.pack(side = 'right', fill = 'both')

# frame for search
searchFrame = tk.Frame(mainFrame, bg = COLOR[3])
searchFrame.pack(padx = 15, pady = 15, anchor = 'center')

searchLabel = tk.Label(searchFrame, text = "Search:", bg = COLOR[3], fg = COLOR[0], font = ("poppins", 14))
searchLabel.pack(padx = 15, pady = 15, anchor = 'center', side='left')

searchBar = tk.Entry(searchFrame, width = 60, bg = COLOR[3], fg = COLOR[0], font = ("poppins", 14))
searchBar.pack(padx = 15, pady = 15, anchor = 'center', side='left')

enterButton = tk.Button(searchFrame, text = "Enter", bg = COLOR[0], fg = COLOR[1], font = ("poppins", 14), command = search)
enterButton.pack(padx = 15, pady = 15, anchor = 'center', side='left')

tree = ttk.Treeview(mainFrame, columns = ("Name", "Artist", "Album", "Time"), show = "headings", height = "20")
tree.heading("Name", text = "Name")
tree.heading("Artist", text = "Artist")
tree.heading("Album", text = "Album")
tree.heading("Time", text = "Time")
tree.column("Name", width = 350)
tree.column("Artist", width = 200)
tree.column("Album", width = 200)
tree.column("Time", width = 50)
tree.pack(padx = 15, pady = 15)
ttk.Style().configure("Treeview", background=COLOR[3], 
foreground=COLOR[0], fieldbackground=COLOR[1])

music_info = tk.Frame(canvas, bg = COLOR[1], width=800)
music_info.pack(padx = 15, pady = 15, anchor = 'center', expand=True, fill='both')

TARGET_SIZE = (256, 256)
loaded_img = Image.open("./images/art.jpeg")
resized_img = loaded_img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(resized_img)
panel = tk.Label(music_info, image = img, bg=COLOR[1])
panel.image = img
panel.pack(side = "top")

label = tk.Label(music_info, text = 'Choose a song to play', bg = COLOR[1], fg = COLOR[3], font = ('poppins',14))
label.pack(pady = 15, side='top')

# progressbar
pb = ttk.Progressbar(
    music_info,
    # style='black.Horizontal.TProgressbar',
    style='blue.Horizontal.TProgressbar',
    orient='horizontal',
    mode='determinate',
    length=400,
)
pb.pack(pady=20, side='top')

# volume frame
volume_info = tk.Frame(music_info, bg = COLOR[1])
volume_info.pack(side='top')

# volume label
vol_label = tk.Label(volume_info, text = 'Volume', bg = COLOR[1], fg = COLOR[3], font = ('poppins',14))
vol_label.pack(pady = 15, side='left')

vol = tk.Scale(
    volume_info,
    length=200,
    bg=COLOR[1],
    fg=COLOR[3],
    troughcolor=COLOR[3],
    from_ = 0,
    to = 100,
    orient = tk.HORIZONTAL,
    resolution = 1,
    command=change_vol
)
vol.pack(side='left')

vol.set(30)

lyricsText = tk.Text(music_info, state=tk.DISABLED, bg = COLOR[3], fg = COLOR[0], font = ('poppins',14), width = 50, height = 15)
lyricsText.pack(padx = 15, pady = 15, side = 'bottom')

top = tk.Frame(music_info, bg = COLOR[1])
top.pack(padx = 15, pady = 15, anchor = 'center')


TARGET_SIZE_SMALL = (64, 64)

#Button for previous song
prev_image = ImageTk.PhotoImage(Image.open("./images/prev.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
prevButton = tk.Button(top, text = 'Prev', image = prev_image, bg = COLOR[1], borderwidth = 0, command= play_prev)
prevButton.pack(pady = 15, side = 'left')

#Button for stop song
stop_image = ImageTk.PhotoImage(Image.open("./images/stop.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
stopButton = tk.Button(top, text = 'Stop', image = stop_image, bg = COLOR[1], borderwidth = 0, command = stop)
stopButton.pack(pady = 15, side = 'left')

replay_image = ImageTk.PhotoImage(Image.open("./images/replay.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))

#Button for play song
play_image = ImageTk.PhotoImage(Image.open("./images/play.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
playButton = tk.Button(top, text = 'Play', image = play_image, bg = COLOR[1], borderwidth = 0, command = select)
playButton.pack(pady = 15, side = 'left')

#Button for pause song
pause_image = ImageTk.PhotoImage(Image.open("./images/pause.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
pauseButton = tk.Button(top, text = 'Pause', image = pause_image, bg = COLOR[1], borderwidth = 0, command = pause_song)
pauseButton.pack(pady = 15, side = 'left')

#Button for next song
next_image = ImageTk.PhotoImage(Image.open("./images/next.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
nextButton = tk.Button(top, text = 'Next', image = next_image, bg = COLOR[1], borderwidth = 0, command = play_next)
nextButton.pack(pady = 15, side = 'left')

# Button for add song
add_image = ImageTk.PhotoImage(Image.open("./images/add.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
addButton = tk.Button(top, text = 'Add', image = add_image, bg = COLOR[1], borderwidth = 0, command = add_song)
addButton.pack(pady = 15, side = 'left')

# Button for edit song
edit_image = ImageTk.PhotoImage(Image.open("./images/edit.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
editButton = tk.Button(top, text = 'Edit', image = edit_image, bg = COLOR[1], borderwidth = 0, command = edit_song)
editButton.pack(pady = 15, side = 'left')

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
def show_lyrics(song=""):
    lyricsText.config(state=tk.NORMAL)
    if song == "":
        lyricsText.delete('1.0', 'end')
        return
    # get filename without the extension
    song = os.path.basename(song)
    print(song)
    # get the lyrics of the song
    lyrics = database.music_df.loc[database.music_df['filename'] == song, 'lyrics'].values[0]
    # show the lyrics in the text box
    lyricsText.delete('1.0', 'end')
    lyricsText.insert('1.0', lyrics)
    lyricsText.config(state=tk.DISABLED)

def show_art(file_path):
        # get filename without the extension

        song = os.path.basename(file_path)
        try:
            album_art_data = database.music_df.loc[database.music_df['filename'] == song, 'album_art'].values[0]
        except:
            album_art_data = None

        if album_art_data is None or album_art_data == "null" or type(album_art_data) != str or file_path=="":
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