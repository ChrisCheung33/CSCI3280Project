import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import simpleaudio as sa
import wave
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

# filename = "./music/ZenZenZense.wav"
def create_visualize_music(filename, music_length = 0):
    # Open the audio file using the wave.open() method
    wav_obj = wave.open(filename, 'rb')

    # Read all frames of the opened sound wave using readframes() function
    audio_frames = wav_obj.readframes(wav_obj.getnframes())

    # Convert audio frames to numpy array
    audio_frames = np.frombuffer(audio_frames, dtype=np.int16)

    # Store the frame rate in a variable using the getframerate() function
    frame_rate = wav_obj.getframerate()
    
    duration = len(audio_frames) / frame_rate * 2
    
    print(audio_frames[frame_rate*5:frame_rate*5+frame_rate])

    # Create a list of frames for the animation
    frames = []
    fig = plt.figure()
    fig.set_facecolor('black')
    for i in range(0, len(audio_frames), int(frame_rate/2)):
        # Plot a segment of the audio signal
        segment = audio_frames[i:i+frame_rate]
        segment = np.abs(segment)
        parts = np.array_split(segment, 40)

        for i, part in enumerate(parts):
            if i % 2 == 0:
                mean_value = np.mean(part)
                part[:] = mean_value
            else:
                part[:] = 0

        line, = plt.plot(segment)
        plt.axhline(y=0,color = "darkgrey" ,linestyle='-')
        plt.ylim([0, 60000])
        frames.append([line])

    # Play Music For Testing
    # wave_obj = sa.WaveObject.from_wave_file(filename)
    # play_obj = wave_obj.play()

    # Create an animation from the frames
    plt.axis('off')
    ani = animation.ArtistAnimation(fig, frames, interval=music_length/duration*1000*0.65, blit=True, repeat=False)
    plt.show()
    # return plt

def visualize_music(filename,savepath = None, music_length = 0, function = None):
    
    plt = create_visualize_music(filename,music_length)
    if function != None:
        function()
    return plt