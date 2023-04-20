import mutagen

from mutagen.wave import WAVE
import soundfile as sf
import os
import struct
import tkinter as tk

# file_path = './music/ZenZenZense.wav'
# file_path = './music/heartache.wav'
file_path = './music/numb.wav'

# data, samplerate = sf.read(file_path)


# audio = mutagen.File(file_path)
audio = WAVE(file_path)

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
lyrics = audio.tags['TXXX:LYRICS']
print(lyrics)


from PIL import ImageTk, Image
# get album art from the audio file
album_art = audio.tags['APIC:']
album_art_data = album_art.data
album_art_format = album_art.mime.split('/')[1]
print(album_art_format)
# print(album_art[0:10])
# album_art = album_art.decode('utf-8')

# show the album art in a window
root = tk.Tk()
root.title("Album Art")
root.geometry("800x800")
root.resizable(False, False)
# img = tk.BitmapImage(data=album_art)
img = ImageTk.PhotoImage(data=album_art_data, format=album_art_format)
# image = Image.open("test.jpeg")
# print(image)
# img = ImageTk.PhotoImage(image)

# resize the image to fixed size 300x300
# img = img.resize((300, 300), Image.ANTIALIAS)

panel = tk.Label(root, image = img)

panel.pack(side = "bottom", fill = "both", expand = "yes")

root.mainloop()