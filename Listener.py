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
volumeMultiplier = 2
q = queue.Queue()

def initializeListener():
    r = sr.Recognizer()
    m = sr.Microphone()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) 
        r.listen_in_background(m, translate, 1)

def translate(recognizer, audio):
    try:
        word = recognizer.recognize_google(audio)
        print(word)
        q.put(word)
    except sr.UnknownValueError:
        print("...")
    except sr.RequestError as e:
        print("Google Speech Recognition not configured; {0}".format(e))

def volumeListener(indata, frames, time, status):
    global soundLevel
    volume_norm = np.linalg.norm(indata) * 10 * volumeMultiplier
    soundLevel.append(int(volume_norm))
    if(len(soundLevel)>100):
        soundLevel.pop(0)

def getSoundVolume():
    return max(soundLevel)

def soundVolume():
    stream = sd.InputStream(callback=volumeListener)
    with stream: 
        while True:
            sd.sleep(10 *1000)