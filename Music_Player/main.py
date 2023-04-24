import pickle
import shutil
import threading
import tkinter as tk
import tkinter.ttk as ttk
import fnmatch
import struct
import os
import numpy as np
# import simpleaudio as sa
import database
import soundfile as sf
from io import BytesIO
from PIL import ImageTk, Image
import ast
import time
import music_visualization
import socket
from scipy.io import wavfile
from pygame import mixer
from scipy.io import wavfile
from pygame import mixer
import wave
# import pyaudio

host_name = socket.gethostname()
host_ip = '192.168.1.102'# socket.gethostbyname(host_name)
print(host_ip)
port = 9611

# COLOR = ['#FFFBEB', '#495579', '#263159', '#251749']
COLOR = ['#2C3639', '#3F4E4F', '#A27B5C', '#DCD7C9']

TARGET_SIZE = (256, 256)
TARGET_SIZE_SMALL = (50, 50)

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
showing_visualize_music = False #Use for turn on/off the visualize_music
frame = 0 #show the number of frame, use for gif animation
v_plt = None

song_length = 0

#action for the play button: to select a song to be play
def select():
    
    if play_obj and mixer is not None:
        play_obj.stop()
        mixer.quit()

    # get the selected song from the treeview
    selected_song = tree.focus()
    if selected_song == "":
        print("No song selected")
        mixer.init()
        return
    selected_song_name = tree.item(selected_song)['values'][0]
    selected_song_path = database.get_filename(selected_song_name)
    
    global song_length
    song_length = database.get_length(selected_song_path)

    # playmusic(rootpath + selected_song_path)
    play_thread = threading.Thread(target=playmusic, args=(rootpath + selected_song_path,), daemon=True)
    play_thread.start()
    
    
#action for the stop button: to clear a song when it is activated
def stop():
    global v_plt
    if v_plt != None:
        v_plt.close()
        v_plt = None
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
        print("Mixer is busy")
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
        # print(keys)
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
    mixer.init(sample_rate, -bits_per_sample, num_channels, 1024)
    # load audio_array into mixer
    play_obj = mixer.Sound(audio_array)
    play_obj.play()
    change_vol()

    filename = os.path.basename(file_path)
    label.config(text = "Now playing: " + database.get_title(filename))
    show_lyrics(file_path)
    show_art(file_path)
    
    global frame
    frame = 0

    # get length of the song
    length = database.get_length(filename)

    pb.start(int(10 * length))

    # play_obj.wait_done()
    while(mixer.get_busy()):
        pass

    pb.stop()
    # playButton['image'] = play_image
    # play_next()


def add_song():
    database.load_from_csv(database.database_path)
    song = database.upload_wav()
    # print("Song: " + song)
    if song == "":
        return
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
    artist = database.get_artist(filename)
    # get the album of the song
    album = database.get_album(filename)
    # get the lyrics of the song
    lyrics = database.get_lyrics(filename)
    
    # create a new window
    editWindow = tk.Toplevel()
    editWindow.title("Edit")
    editWindow.geometry("400x600")
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
    # create a label for the lyrics of the song
    lyricsLabel = tk.Label(editFrame, text = "Lyrics", bg = COLOR[1], fg = COLOR[3], font = ("poppins", 14))
    lyricsLabel.grid(row = 3, column = 0, padx = 5, pady = 5)
    
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
    # create an entry for the lyrics of the song
    lyricsEntry = tk.Text(editFrame, width = 30, height = 12, bg = COLOR[1], fg = COLOR[3], font = ("poppins", 14))
    lyricsEntry.grid(row = 3, column = 1, padx = 5, pady = 5)
    lyricsEntry.insert(tk.END, lyrics)

    # create a button for save the changes
    saveButton = tk.Button(editFrame, text = "Save", bg = COLOR[0], fg = COLOR[1], font = ("poppins", 14), command = lambda: save_changes(filename, nameEntry.get(), artistEntry.get(), albumEntry.get(), lyricsEntry.get(1.0, "end-1c"), editWindow))
    saveButton.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5)

def audio_stream():
    server_socket = socket.socket()
    server_socket.bind((host_ip, (port-1)))
    server_socket.listen(5)
    
    CHUNK = 1024
    wf = wave.open("temp.wav", 'rb')
    p = pyaudio.PyAudio()
    
    print('server listening at',(host_ip, (port-1)))
   
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    client_socket,addr = server_socket.accept()
 
    data = None
    while True:
        if client_socket:
            while True:
                data = wf.readframes(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)

# let the user for network connection
def network_connection():
    # create a new window
    NetworkConnectionWindow = tk.Toplevel()
    NetworkConnectionWindow.title("Network Connection")
    NetworkConnectionWindow.geometry("400x600")
    NetworkConnectionWindow.resizable(False, False)
    NetworkConnectionWindow.configure(bg = COLOR[1])
    # create a frame
    network_frame = tk.Frame(NetworkConnectionWindow, bg=COLOR[1])
    network_frame.pack(padx=15, pady=15, anchor='center')

    # create a label for the IP address input field
    ip_address_label = tk.Label(network_frame, text="IP Address", bg=COLOR[1], fg=COLOR[3], font=("poppins", 14))
    ip_address_label.grid(row=0, column=0, padx=5, pady=5)

    # create an entry for the IP address input field
    ip_address_entry = tk.Entry(network_frame, width=30, bg=COLOR[1], fg=COLOR[3], font=("poppins", 14))
    ip_address_entry.grid(row=0, column=1, padx=5, pady=5)

    def connect_to_target():
        # read IP address of the local PC
        my_ip_address = socket.gethostbyname(socket.gethostname())
        # read target IP address
        target_ip_address = ip_address_entry.get()
        # establish TCP connection to target PC
        try:
            target_port = 9610 # use the port number used by the server code
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip_address, target_port))
            print("Connected to target PC at IP address:", target_ip_address)
            # send data to target PC
            # ...
            s.close()
        except socket.error as e:
            print("Error connecting to target PC:", e)

    # create a button for applying the network connection
    apply_button = tk.Button(network_frame, text='Apply', bg = COLOR[0], fg = COLOR[1], font=("poppins", 14), command=connect_to_target)
    apply_button.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5)

def save_changes(filename, title, artist, album, lyrics, editWindow):
    # get the selected song
    selected = tree.selection()
    
    # update the database
    database.update_music(filename, title, album, artist, lyrics)

    length = database.get_format_length(database.get_length(filename))
    
    if artist == "none":
        artist = "None"

    if album == "none":
        album = "None"

    # update the treeview
    tree.item(selected, values = (title, artist, album, length))

    # close the window
    editWindow.destroy()

# remove the selected song from the database, the treeview and from the folder
def remove_song():
    # get the selected song
    selected = tree.selection()
    if all(selected):
        return
    # get the filename of the song
    filename = tree.item(selected, 'values')[0]
    # remove the song from the database
    if filename == "" or filename is None:
        return
    database.remove_music(filename)
    # remove the song from the treeview
    tree.delete(selected)
    # remove the song from the folder
    os.remove(rootpath + filename)

    print(f"{filename} removed")

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
        if row['artist'] == 'none':
            row['artist'] = 'None'

        if row['album'] == 'none':
            row['album'] = 'None'
            
        tree.insert("", "end", values = (row['title'], row['artist'], row['album'], database.get_format_length(row['length'])))
 

def visualize_music(song_name,pause_event,resume_event,stop_event):
    global frame
    global showing_visualize_music
    
    song_path = database.get_filename(song_name)
    music_length = database.get_length(song_path)
    max_frame = 0

    # Load the music visualize gif
    loaded_img = Image.open("./visualize/{}.gif".format(song_name))
    max_frame = loaded_img.n_frames
    
    # Time interval
    music_length_correction = 2 if(music_length<59) else 0.92
    time_interval = music_length/max_frame*music_length_correction
    
    for frame in range(max_frame):
        
        if stop_event.is_set():
            stop_event.clear()
            break

        if pause_event.is_set() == False:
            print("Max Frame:",max_frame," Current Frame:",frame)
            try:
                loaded_img.seek(frame)
            except:
                show_art("")
            resized_img = loaded_img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(resized_img)
            panel.config(image = img)
            panel.image = img
        
        if resume_event.is_set():
            pause_event.clear()
            resume_event.clear()
        
        time.sleep(time_interval)
    

# def show_visualize_music():
#     global showing_visualize_music
#     global visual_thread
#     global pause_event
#     global resume_event
#     global stop_event
    
#     if(showing_visualize_music):
#         showing_visualize_music = False
#         pause_event.set()
#     else:
#         if(tree.selection()):
#             showing_visualize_music = True
#             selected_song = tree.focus()
#             selected_song_name = tree.item(selected_song)['values'][0]
            
#             try:
#                 # Check the visualize gif of the song exist
#                 loaded_img = Image.open("./visualize/{}.gif".format(selected_song_name))
#             except:
#                 #Stop the song
#                 stop()
#                 #Visualize the song
#                 music_visualization.create_visualize_music(rootpath+selected_song_path, "./visualize/{}.gif".format(selected_song_name))
#             if(visual_thread == None or visual_thread.is_alive() == False):
#                 print("Hello")
#                 visual_thread = threading.Thread(target=visualize_music,args=(selected_song_name,pause_event,resume_event,stop_event))
#                 visual_thread.start()
#             else:
#                 resume_event.set()

def show_visualize_music():
    global v_plt
    if(tree.selection()):
        showing_visualize_music = True
        selected_song = tree.focus()
        selected_song_name = tree.item(selected_song)['values'][0]
        music_length = database.get_length(database.get_filename(selected_song_name))
        v_plt = music_visualization.visualize_music(rootpath+database.get_filename(selected_song_name),music_length = music_length,function = select())

def change_vol(_=None):
    if play_obj:
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

enterButton = tk.Button(searchFrame, text = "Enter", bg = COLOR[3], fg = COLOR[0], font = ("poppins", 14), command = search)
enterButton.pack(padx = 15, pady = 15, anchor = 'center', side='left')

tree = ttk.Treeview(mainFrame, columns = ("Name", "Artist", "Album", "Time"), show = "headings", height = "12")
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

manageFrame = tk.Frame(mainFrame, bg = COLOR[3])
manageFrame.pack(padx = 15, pady = 15, anchor = 'e')

# Button for add song
add_image = ImageTk.PhotoImage(Image.open("./images/add.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
addButton = tk.Button(manageFrame, text = 'Add', image = add_image, bg = COLOR[3], borderwidth = 0, command = add_song)
addButton.pack(pady = 15, side = 'left')

# Button for edit song
edit_image = ImageTk.PhotoImage(Image.open("./images/edit.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
editButton = tk.Button(manageFrame, text = 'Edit', image = edit_image, bg = COLOR[3], borderwidth = 0, command = edit_song)
editButton.pack(pady = 15, side = 'left')

# Button for remove song
remove_image = ImageTk.PhotoImage(Image.open("./images/remove.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
removeButton = tk.Button(manageFrame, text = 'Remove', image = remove_image, bg = COLOR[3], borderwidth = 0, command = remove_song)
removeButton.pack(pady = 15, side = 'left')

# Button for network_connection
network_connection_image = ImageTk.PhotoImage(Image.open("./images/network_connection.png").resize(TARGET_SIZE_SMALL, Image.Resampling.LANCZOS))
editButton = tk.Button(manageFrame, text = 'Edit', image = network_connection_image, bg = COLOR[3], borderwidth = 0, command = network_connection)
editButton.pack(pady = 15, side = 'left')


music_info = tk.Frame(canvas, bg = COLOR[1], width=800)
music_info.pack(padx = 15, pady = 15, anchor = 'center', expand=True, fill='both')

loaded_img = Image.open("./images/art.jpeg")
resized_img = loaded_img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(resized_img)
panel = tk.Label(music_info, image = img, bg=COLOR[1])
panel.image = img
panel.pack(side = "top")

label = tk.Label(music_info, text = 'Choose a song to play', bg = COLOR[1], fg = COLOR[3], font = ('poppins',24))
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
    showvalue=0,
    from_ = 0,
    to = 100,
    orient = tk.HORIZONTAL,
    resolution = 1,
    command=change_vol
)
vol.pack(side='left')

vol.set(30)

top = tk.Frame(music_info, bg = COLOR[1])
top.pack(padx = 15, pady = 15, anchor = 'center')

#Button for visualize song
wave_image = ImageTk.PhotoImage(Image.open("./images/wave.png").resize((32,32), Image.Resampling.LANCZOS))
button = tk.Button(panel, text='Button', image = wave_image, bg = COLOR[3], borderwidth = 0, command= show_visualize_music)
button.place(relx=1.0, rely=1.0, anchor='se')

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

lyricsText = tk.Text(music_info, state=tk.DISABLED, bg = COLOR[3], fg = COLOR[0], font = ('poppins',14), width = 50, height = 12)
lyricsText.pack(padx = 15, pady = 15, side = 'top')


def read_file_to_treeview(rootpath, pattern):
    filename_list = []
    for root, dirs, files in os.walk(rootpath):
        for filename in fnmatch.filter(files, pattern):
            filename_list.append(os.path.basename(filename))

    filename_list.sort()
    # print(filename_list)
    for filename in filename_list:
        # get the name of the song
        name = database.get_title(filename)
        # get the artist of the song
        artist = database.get_artist(filename)
        if artist == "none":
            artist = "None"
        # get the album of the song
        album = database.get_album(filename)
        if album == "none":
            album = "None"
        # get the time of the song
        time = database.get_length(filename)
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
    # print(song)
    # get the lyrics of the song
    lyrics = database.get_lyrics(song)
    # show the lyrics in the text box
    lyricsText.delete('1.0', 'end')
    lyricsText.insert('1.0', lyrics)
    lyricsText.config(state=tk.DISABLED)

def show_art(file_path):
        # get filename without the extension

        song = os.path.basename(file_path)
        try:
            album_art_data = database.get_album_art(song)
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