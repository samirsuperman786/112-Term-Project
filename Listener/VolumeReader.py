import pyaudio
import numpy as np
import sounddevice as sd

global soundLevel
soundLevel = [100]
soundCache = 100
volumeMultiplier = 2

#starts the volume lisetener
def initializeVolume():
    stream = sd.InputStream(callback=convertSoundVolume)
    with stream: 
        while True:
            sd.sleep(1000)

#converts sound levels
def convertSoundVolume(indata, frames, time, status):
    global soundLevel
    volume_norm = np.linalg.norm(indata) * 10 * volumeMultiplier
    soundLevel.append(int(volume_norm))
    #stores the past soundCache # of volume
    if(len(soundLevel)>soundCache):
        soundLevel.pop(0)

#gets how loud the sound is
def getSoundVolume():
    return max(soundLevel)