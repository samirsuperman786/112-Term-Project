#!/usr/bin/env python3

# code adapted from:
# https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py

import time

import speech_recognition as sr
import queue

phrases = queue.Queue()

#starts the listener
def initializeListener():
    r = sr.Recognizer()
    m = sr.Microphone()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) 
        r.listen_in_background(m, translate, 1)

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