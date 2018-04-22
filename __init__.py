#Server code and panda3d code adapted from optional lectures

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import sys, math, os, random
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import *

from direct.task.Task import Task
import time

from Listener.ListenerManager import *
from Listener.VolumeReader import *

from threading import Thread
from Graphics.Word import *
from Graphics.CloudManager import *
from Graphics.SceneManager import *

import socket
import threading
from queue import Queue

HOST = "localhost"
PORT = 50011

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("Connected to server!")

#handles server messages
def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

#The main window 
class Display(ShowBase):
    #sets up the initial parameters
    def __init__(self):
        #ShowBase.__init__(self)
        self.words = []
        self.otherPlayers = dict()
        self.myPID = None
        #load all the things
        setupScene(self, render)# load lights and the fancy background
        self.loadModels()
        loadClouds(render)
        #key movement
        self.createKeyControls()
        self.keyMap = {}
        #timerFired
        updateTimer = .2
        newWordTimer = 1
        moveCloudTimer = .01
        taskMgr.doMethodLater(updateTimer, self.update, "update")
        taskMgr.doMethodLater(newWordTimer, self.getNewWord, "word")
        taskMgr.doMethodLater(moveCloudTimer, moveClouds, "cloud")

    def loadModels(self):
        pass

    def setKey(self, key, value):
        self.keyMap[key] = value

    def createKeyControls(self):
        pass

    #Updates the display and gets new words
    def update(self, task):
        while (serverMsg.qsize() > 0):
            msg = serverMsg.get(False)
            try:
                print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]
                if(command== "myIDis"):
                    self.myPID = msg[1]
                    self.otherPlayers[self.myPID] =[]
                elif(command == "myMicIs"):
                    micIndex = int(msg[1])
                    initializeListener(micIndex)
                elif(command == "newPlayer"):
                    newPID = msg[1]
                    self.otherPlayers[newPID] = []
                elif(command == "newWord"):
                    PID = msg[1]
                    label = msg[2]
                    x = int(msg[3])
                    y = int(msg[4])
                    z = int(msg[5])
                    newWord = Word(PID, render, x, y, z, label)
                    self.otherPlayers[PID].append(newWord)
            except:
                print(msg)
                print("failed")
            serverMsg.task_done()

        for player in self.otherPlayers:
            for word in self.otherPlayers[player]:
                pass
                # if(word.move()==False):
                #     self.otherPlayers[player].remove(word)
        return task.cont

    #grabs words from listenermanager
    def getNewWord(self, task):
        (startX, startY, startZ) = (-4, 30, 10)
        if(phrases.empty()==False):
            label = phrases.get()
            word = Word(self.myPID, render, startX, startY, startZ, label)
            self.otherPlayers[self.myPID].append(word)
            msg = "newWord %s %d %d %d\n" % (label, startX + 8, startY, startZ)
            server.send(msg.encode())
        return task.again

if __name__ == "__main__":
    game = Display()
    serverMsg = Queue(100)
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    #base.disableMouse()
    base.enableParticles()
    base.run()
