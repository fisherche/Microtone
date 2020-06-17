import sounddevice
import numpy as np 
import time

class AudioDevice():
    def __init__(self):
        self.samples = 44100
        self.amplification = 0.4
        self.duration = 8
        self.eaSample = np.arange(self.duration * self.samples)


    def makeAudible(self,frequency, duration=None):
        if duration == None:
            duration = self.duration
        waveform = np.sin(2 * np.pi * self.eaSample * frequency / self.samples)
        waveScaled = waveform * self.amplification
        sounddevice.play(waveScaled,self.samples)
        time.sleep(duration)
        sounddevice.stop()
    