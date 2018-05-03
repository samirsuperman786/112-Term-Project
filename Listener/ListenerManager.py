#!/usr/bin/env python3

# code adapted from:
# https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py

import time

import speech_recognition as sr
import queue

stop = None
phrases = queue.Queue()


#starts the listener
def initializeListener(micIndex):
    global stop
    global phrases
    phrases.put("Connected!")
    r = sr.Recognizer()
    m = sr.Microphone(device_index=micIndex)
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration = 0.5) 
        stop = r.listen_in_background(m, translate, 2)

def stopListener():
    global stop
    global phrases
    if(stop!=None):
        stop(False)
        phrases.queue.clear()

#translates audio to text
def translate(recognizer, audio):
    global phrases
    try:
        sentence = recognizer.recognize_google(audio)
        #adds to our word queue
        for w in sentence.split(" "):
            phrases.put(w)
    except sr.UnknownValueError:
        print("...")
    except sr.RequestError as e:
        print("Google Speech Recognition not configured; {0}".format(e))
