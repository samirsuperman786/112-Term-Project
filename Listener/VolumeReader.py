import pyaudio
import numpy as np
import sounddevice as sd

global soundLevel
soundLevel = 0
volumeMultiplier = 1
time = 0

#starts the volume lisetener
def initializeVolume():
    stream = sd.InputStream(callback=convertSoundVolume)
    with stream: 
        while True:
            sd.sleep(1000)

#converts sound levels
def convertSoundVolume(indata, frames, time, status):
    global soundLevel
    volume_norm = np.linalg.norm(indata) * 10
    soundLevel= int(volume_norm)

#gets how loud the sound is
def getSoundVolume():
	return soundLevel