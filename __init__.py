from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import sys, math, os, random
from direct.gui.OnscreenText import OnscreenText

#for basic intervals
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import *

#for task managers
from direct.task.Task import Task
import time

from Listener.ListenerManager import *
from Listener.VolumeReader import *

from threading import Thread
from Graphics.Word import *

import socket
import threading
from queue import Queue

HOST = "localhost" # put your IP address here if playing on multiple computers
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

        ShowBase.__init__(self)
        self.words = []

        self.otherPlayers = dict()
        self.myPID = None
        #load all the things
        self.loadBackground() # load lights and the fancy background
        self.loadModels()
        #key movement
        self.createKeyControls()

        self.keyMap = {}
        #timerFired
        taskMgr.doMethodLater(.2, self.update, "update")
        taskMgr.doMethodLater(1, self.getNewWord, "word")

    #loads the background
    def loadBackground(self):
        #add one light per face, so each face is nicely illuminated
        plight1 = PointLight('plight')
        plight1.setColor(VBase4(1, 1, 1, 1))
        plight1NodePath = render.attachNewNode(plight1)
        plight1NodePath.setPos(0, 0, 500)
        render.setLight(plight1NodePath)

        plight2 = PointLight('plight')
        plight2.setColor(VBase4(1, 1, 1, 1))
        plight2NodePath = render.attachNewNode(plight2)
        plight2NodePath.setPos(0, 0, -500)
        render.setLight(plight2NodePath)

        plight3 = PointLight('plight')
        plight3.setColor(VBase4(1, 1, 1, 1))
        plight3NodePath = render.attachNewNode(plight3)
        plight3NodePath.setPos(0, -500, 0)
        render.setLight(plight3NodePath)

        plight4 = PointLight('plight')
        plight4.setColor(VBase4(1, 1, 1, 1))
        plight4NodePath = render.attachNewNode(plight4)
        plight4NodePath.setPos(0, 500, 0)
        render.setLight(plight4NodePath)

        plight5 = PointLight('plight')
        plight5.setColor(VBase4(1, 1, 1, 1))
        plight5NodePath = render.attachNewNode(plight5)
        plight5NodePath.setPos(500,0, 0)
        render.setLight(plight5NodePath)

        plight6 = PointLight('plight')
        plight6.setColor(VBase4(1, 1, 1, 1))
        plight6NodePath = render.attachNewNode(plight6)
        plight6NodePath.setPos(-500,0, 0)
        render.setLight(plight6NodePath)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-20, 50, 0)

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
                if(word.move()==False):
                    self.otherPlayers[player].remove(word)
        return task.cont

    def getNewWord(self, task):
        (startX, startY, startZ) = (-4, 20, 10)
        if(phrases.empty()==False):
            label = phrases.get()
            word = Word(self.myPID, render, startX, startY, startZ, label)
            self.otherPlayers[self.myPID].append(word)
            msg = "newWord %s %d %d %d\n" % (label, startX + 8, startY, startZ)
            server.send(msg.encode())
        return task.again

if __name__ == "__main__":
    initializeListener()
    game = Display()
    serverMsg = Queue(100)
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    base.run()