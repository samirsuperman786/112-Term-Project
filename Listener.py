#!/usr/bin/env python3

# code adapted from:
# https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py

import time

import speech_recognition as sr
import queue
import pyaudio

r = None
m = None
q = queue.Queue()
q.put("hi")

def initializeSpeech():
    r = sr.Recognizer()
    m = sr.Microphone()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        r.listen_in_background(m, callback, 1.8)
    #for _ in range(50): time.sleep(0.1)

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        word = recognizer.recognize_google(audio)
        print(word)
        q.put(word)

    except sr.UnknownValueError:
        print("...")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))