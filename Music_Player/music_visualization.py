import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import simpleaudio as sa
import wave
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# filename = "./music/ZenZenZense.wav"

def create_visualize_music(filename,savepath = None):
    # Open the audio file using the wave.open() method
    wav_obj = wave.open(filename, 'rb')

    # Read all frames of the opened sound wave using readframes() function
    audio_frames = wav_obj.readframes(wav_obj.getnframes())

    # Convert audio frames to numpy array
    audio_frames = np.frombuffer(audio_frames, dtype=np.int16)

    # Store the frame rate in a variable using the getframerate() function
    frame_rate = wav_obj.getframerate()
    
    duration = len(audio_frames) / frame_rate

    # Create a list of frames for the animation
    frames = []
    fig = plt.figure()
    fig.set_facecolor('black')
    for i in range(0, len(audio_frames), int(frame_rate/4)):
        # Plot a segment of the audio signal
        if i%frame_rate/frame_rate == 0:
            segment = audio_frames[i:i+frame_rate]
        else:
            segment = audio_frames[i:i+frame_rate]*0.75
        line, = plt.plot(segment)
        plt.ylim([-frame_rate, frame_rate])
        frames.append([line])

    # Play Music For Testing
    # wave_obj = sa.WaveObject.from_wave_file(filename)
    # play_obj = wave_obj.play()

    # Create an animation from the frames
    plt.axis('off')
    ani = animation.ArtistAnimation(fig, frames, interval=0.25*1000, blit=True, repeat=False)
    
    # def on_animation_complete():
    #     plt.close()
    
    # ani.event_source.stop()
    # ani.event_source = fig.canvas.new_timer(interval=(duration * 1000))
    # ani.event_source.add_callback(on_animation_complete)
    # ani.event_source.start()

    # Uncomment the following line to save the animation as a video file
    # ani.save(savepath)
    plt.show()