#Server code and panda3d code adapted from optional lectures

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import sys, math, os, random
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import *
from direct.gui.DirectGui import *

from direct.task.Task import Task
import time

from Listener.ListenerManager import *
from Listener.VolumeReader import *

from threading import Thread
from Graphics.Word import *
from Graphics.CloudManager import *
from Graphics.SceneManager import *
from Database.DatabaseManager import *
from Utils.CustomString import *

import socket
import threading
from queue import Queue
import copy

nodePaths = []
state = "login"
myName = ""

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
        updateTimer = .2
        taskMgr.doMethodLater(updateTimer, self.update, "update")
        
    def loadModels(self):
        setupScene(self, render)# load lights and the fancy background
        loadClouds(render)
        #timerFired
        newWordTimer = 1
        moveCloudTimer = .01
        taskMgr.doMethodLater(newWordTimer, self.getNewWord, "word")
        taskMgr.doMethodLater(moveCloudTimer, moveClouds, "cloud")

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
                    self.micIndex = int(msg[1])
                elif(command == "newPlayer"):
                    newPID = msg[1]
                    self.otherPlayers[newPID] = []
                    updateMenu(myName)
                elif(command == "loginEvent"):
                    updateMenu(myName)
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
                if(word.move()==False):
                    self.otherPlayers[player].remove(word)
        return task.cont

    #grabs words from listenermanager
    def getNewWord(self, task):
        (startX, startY, startZ) = (-4, 35, 6)
        if(phrases.empty()==False):
            label = phrases.get()
            word = Word(self.myPID, render, startX, startY, startZ, label)
            self.otherPlayers[self.myPID].append(word)
            msg = "newWord %s %d %d %d\n" % (label, startX + 8, startY, startZ)
            server.send(msg.encode())
        return task.again

def createGravity():
    #add gravity
    base.enableParticles()
    gravityFN=ForceNode('world-forces')
    gravityFNP=render.attachNewNode(gravityFN)
    gravityForce=LinearVectorForce(0,0,-3) #gravity acceleration
    gravityFN.addForce(gravityForce)
    base.physicsMgr.addLinearForce(gravityForce)

def start():
    loginScreen()
    base.run()
 
def loginScreen():
    clearScreen()
    text = TextNode("Username")
    text.setText("Username")
    textNodePath = aspect2d.attachNewNode(text)
    textNodePath.setScale(.15)
    textNodePath.setPos(-.9,0,0)
    entry = DirectEntry(text = "", scale=.2, command=menuScreen,
    initialText="", numLines = 2, focus=1,
     frameSize = (-.3,0,0,0))

    nodePaths.append(textNodePath)
    nodePaths.append(entry)

def menuScreen(playerName):
    state="menu"
    msg = "loginEvent"
    server.send(msg.encode())
    global myName
    myName= playerName
    setOnlineStatus(playerName, True)
    clearScreen()
    if(isTracked(playerName)==False): newPlayer(playerName)
    updateMenu(playerName)

def updateMenu(playerName):
    clearScreen()
    text = TextNode("Online Players")
    toDisplay = "Welcome back " + playerName + "!\n\n"\
     + "\nOnline players: \n"
    online = getOnlinePlayers()
    for player in online:
        if(player == playerName): continue
        toDisplay += player + "\n"
    if(len(online)==0):
        toDisplay+= "No players online!"
    text.setText(toDisplay)
    textNodePath = aspect2d.attachNewNode(text)
    textNodePath.setScale(.15)
    textNodePath.setPos(-.9,0,.7)
    nodePaths.append(textNodePath)

def dialFriend(playerName, friend):
    state = "inCall"
    initializeListener(micIndex)
    game.loadModels()
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    base.disableMouse()
    createGravity()

def clearScreen():
    global nodePaths
    tmp = copy.copy(nodePaths)
    for path in tmp:
        path.removeNode()
        nodePaths.remove(path)

def userLogOff():
    setOnlineStatus(myName, False)

if __name__ == "__main__":
    base.exitFunc = userLogOff
    serverMsg = Queue(100)
    game = Display()
    start()
