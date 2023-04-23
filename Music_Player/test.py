# import mutagen

# from mutagen.wave import WAVE
# import soundfile as sf
# import os
# import struct
# import tkinter as tk
# from io import BytesIO
# import database
# import ast

# file_path = './music/ZenZenZense.wav'
# file_path = './music/heartache.wav'
file_path = './music/numb.wav'

# data, samplerate = sf.read(file_path)


# audio = mutagen.File(file_path)
# audio = WAVE(file_path)

# audio = sf.SoundFile(file_path)
# filename = os.path.basename(file_path)
# print(filename)
# print(audio.__getattr__('artist'))
# print(audio.__getattr__('title'))
# print(audio.__getattr__('album'))

# # # get duration of the audio file
# duration = audio.frames / audio.samplerate

# print(round(duration, 2), "seconds")
# # # covert length to minutes and seconds
# minutes = int(duration / 60)
# seconds = int(duration % 60)
# print(minutes, "minutes", seconds, "seconds")

# with open(file_path, 'rb') as wave_file:
#     # audio.seek(-2, 2)
#     lyrics = struct.unpack('<H', wave_file.read(2))[0]
#     print(lyrics)

# print(audio.__getattr__('lyrics'))
# # get lyrics from the audio file
# print(audio.__getattr__('lyrics'))

# print(audio.pprint())

# artist = audio.tags['TPE1']
# print(artist)
# album = audio.tags['TALB']
# print(album)
# title = audio.tags['TIT2']
# print(title)
# length = audio.info.length
# length = round(length)
# print(length, "seconds")
# # covert length to minutes and seconds
# minutes = length // 60
# seconds = length % 60
# print(minutes, "minutes", seconds, "seconds")
# # show in mm:ss format
# if seconds < 10:
#     print(str(minutes) + ":0" + str(seconds))
# else:
#     print(str(minutes) + ":" + str(seconds))
# filename = os.path.basename(file_path)
# print(filename)

# # get the bit depth of the audio file
# bit_depth = audio.info.bits_per_sample
# print(bit_depth, "bit")

# # get lyrics from the audio file
# lyrics = audio.tags['TXXX:LYRICS']
# print(lyrics)


# from PIL import ImageTk, Image
# get album art from the audio file
# album_art = audio.tags['APIC:']
# album_art = database.get_album_art(file_path)
# print(album_art)
# album_art_data = album_art.data
# print(album_art_data)
# print(album_art_data[:20])
# album_art_format = album_art.mime.split('/')[1]
# print(album_art_format)
# print(album_art[0:10])
# album_art = album_art.decode('utf-8')

# show the album art in a window
# root = tk.Tk()
# root.title("Album Art")
# root.geometry("800x800")
# root.resizable(True, True)
# img = tk.BitmapImage(data=album_art)
# img = ImageTk.PhotoImage(data=album_art_data, format=album_art_format)

# music_info = tk.Frame(root, bg = "black")
# music_info.pack(padx = 15, pady = 15, anchor = 'center')

# # resize the image to fixed size (256, 256)
# TARGET_SIZE = (128, 128)
# loaded_img = Image.open(BytesIO(album_art_data))
# print(loaded_img)
# resized_img = loaded_img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
# img = ImageTk.PhotoImage(resized_img)

# panel = tk.Label(root, image = img)

# panel.pack(side = "bottom", fill = "both", expand = "yes", in_ = music_info)

# root.mainloop()

# string_data = "b'\\xff\\xd8\\xff'"
# byte_data = ast.literal_eval(string_data)
# print(byte_data)
# print(type(byte_data))

# import tkinter as tk
# from tkinter import ttk

# root = tk.Tk()

# tree = ttk.Treeview(root)
# tree.pack()

# for i in range(10):
#     tree.insert("", "end", text=f"Item {i}")

# def focus_next_row():
#     selected_item = tree.selection()
#     if selected_item:
#         next_item = tree.index(selected_item[0]) + 1
#         if next_item < len(tree.get_children()):
#             tree.focus(tree.get_children()[next_item])
#             tree.selection_set(tree.get_children()[next_item])

# tree.bind("<Down>", focus_next_row)

# button = tk.Button(root, text="Focus next row", command=focus_next_row)
# button.pack()

# root.mainloop()

# import pandas as pd

# df = pd.DataFrame([
#   ["1", "太郎"],
#   ["2", "花子"]],
#   columns=['id', '名前'])

# print(df)

# # test.csvとして出力
# df.to_csv("test.csv")

# import tkinter as tk
# from PIL import Image, ImageTk

# root = tk.Tk()

# button = tk.Button(self.left_menu)
# button_load = Image.open('./images/add.png')
# root.button_img = ImageTk.PhotoImage(button_load)
# button.config(image=root.button_img)

# button_1.pack(side='top')

import tkinter as tk
from pygame import mixer

root = tk.Tk()
root.title("Music Player")
root.geometry("800x800")
root.resizable(True, True)

def play_music():
    mixer.init()
    audio = mixer.music.load(file_path)
    mixer.music.play()

def change_vol(_=None):
    mixer.music.set_volume(vol.get() / 100)

vol = tk.Scale(
    root,
    from_ = 0,
    to = 100,
    orient = tk.HORIZONTAL,
    resolution = 1,
    command=change_vol
)
vol.pack()

vol.set(30)

play_music()

root.mainloop()

# from tkinter import ttk
# import tkinter as tk
# from tkinter.messagebox import showinfo


# # root window
# root = tk.Tk()
# root.geometry('300x120')
# root.title('Progressbar Demo')


# def update_progress_label():
#     return f"Current Progress: {pb['value']}%"


# def progress():
#     if pb['value'] < 100:
#         pb['value'] += 20
#         value_label['text'] = update_progress_label()
#     else:
#         showinfo(message='The progress completed!')


# def stop():
#     pb.stop()
#     value_label['text'] = update_progress_label()


# progressbar
# pb = ttk.Progressbar(
#     root,
#     orient='horizontal',
#     mode='determinate',
#     length=280
# )
# # place the progressbar
# pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

# # label
# value_label = ttk.Label(root, text=update_progress_label())
# value_label.grid(column=0, row=1, columnspan=2)

# start_button = ttk.Button(
#     root,
#     text='Start',
#     # command=pb.start
# )
# start_button.grid(column=0, row=1, padx=10, pady=10, sticky=tk.E)

# pb.start(6*10)

# # start button
# start_button = ttk.Button(
#     root,
#     text='Progress',
#     command=progress
# )
# start_button.grid(column=0, row=2, padx=10, pady=10, sticky=tk.E)

# stop_button = ttk.Button(
#     root,
#     text='Stop',
#     command=stop
# )
# stop_button.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)


# root.mainloop()

# from tkinter import *
# from tkinter.ttk import *
# import time

# ws = Tk()
# ws.title('PythonGuides')
# ws.geometry('400x250+1000+300')

# def step():
#     for i in range(5):
#         ws.update_idletasks()
#         pb1['value'] += 20
        
#         time.sleep(1)

# pb1 = Progressbar(ws, orient=HORIZONTAL, length=100, mode='indeterminate')
# pb1.pack(expand=True)

# Button(ws, text='Start', command=step).pack()

# ws.mainloop()

# COLOR = ['#FFFBEB', '#495579', '#263159', '#251749']