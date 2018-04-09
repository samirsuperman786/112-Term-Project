#!/usr/bin/env python3

# code adapted from:
# https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py

import time

import speech_recognition as sr
import queue
import pyaudio
import numpy as np
import sounddevice as sd

global soundLevel
soundLevel = [100]
soundCache = 100
volumeMultiplier = 2
phrases = queue.Queue()

#starts the listener
def initializeListener():
    r = sr.Recognizer()
    m = sr.Microphone()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) 
        r.listen_in_background(m, translate, 1)

#starts the volume lisetener
def initializeVolume():
    stream = sd.InputStream(callback=convertSoundVolume)
    with stream: 
        while True:
            sd.sleep(10 *1000)

#translates audio to text
def translate(recognizer, audio):
    try:
        word = recognizer.recognize_google(audio)
        print(word)
        #adds to our word queue
        phrases.put(word)
    except sr.UnknownValueError:
        print("...")
    except sr.RequestError as e:
        print("Google Speech Recognition not configured; {0}".format(e))

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