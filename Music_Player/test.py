import mutagen
import os

file_path = './music/heartache.wav'

audio = mutagen.File(file_path)

print(audio.pprint())

artist = audio.tags['TPE1']
print(artist)
album = audio.tags['TALB']
print(album)
title = audio.tags['TIT2']
print(title)
length = audio.info.length
length = round(length)
print(length, "seconds")
# covert length to minutes and seconds
minutes = length // 60
seconds = length % 60
print(minutes, "minutes", seconds, "seconds")
# show in mm:ss format
if seconds < 10:
    print(str(minutes) + ":0" + str(seconds))
else:
    print(str(minutes) + ":" + str(seconds))
filename = os.path.basename(file_path)
print(filename)

# get the bit depth of the audio file
bit_depth = audio.info.bits_per_sample
print(bit_depth, "bit")

# get lyrics from the audio file
lyrics = audio.tags['TXXX:LYRICS']
print(lyrics)
