import simpleaudio as sa
import time

wave_obj = sa.WaveObject.from_wave_file("file_example (1).wav")
play_obj = wave_obj.play()

time.sleep(3)
play_obj.pause()
print("paused")

time.sleep(3)
play_obj.resume()
print("resumed")

time.sleep(3)
play_obj.stop()
print("stopped")

play_obj.wait_done()