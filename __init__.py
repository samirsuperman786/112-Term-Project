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
from Graphics.MenuBobble import *

import socket
import threading
from queue import Queue
import copy

nodePaths = []
state = "login"
myName = ""
micIndex = None
leftRegion = (-4, 35, 8)

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
        setupScene(render)# load lights and the fancy background
        loadBackground(self)
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
            print(msg)
            try:
                print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]
                if(command== "myIDis"):
                    self.myPID = msg[1]
                    self.otherPlayers[self.myPID] =[]
                elif(command == "myMicIs"):
                    global micIndex
                    self.micIndex = micIndex =  int(msg[1])
                elif(command == "newPlayer"):
                    newPID = msg[1]
                    self.otherPlayers[newPID] = []
                elif(command == "loginEvent" or command == "logoffEvent"):
                    if(state=="menu"):
                        updateMenu()
                elif(command == "callEvent"):
                    if(state=="menu"):
                        player1 = msg[2]
                        player2 = msg[3]
                        if(player1 == myName):
                            dialFriend(myName, player2)
                        elif(player2 == myName):
                            dialFriend(myName, player1)
                elif(command == "newWord"):
                    if(state=="inCall"):
                        PID = msg[1]
                        label = msg[2]
                        (x,y,z) = (8, 35, 10)
                        if(PID ==self.myPID):
                            x = -8
                        newWord = Word(render, x, y, z, label)
                        self.otherPlayers[PID].append(newWord)
            except:
                print(msg)
                print("failed")
            serverMsg.task_done()
        return task.cont

    #grabs words from listenermanager
    def getNewWord(self, task):
        (startX, startY, startZ) = (-8, 35, 10)
        if(phrases.empty()==False):
            label = phrases.get()
            msg = "newWord %s\n" % (label)
            server.send(msg.encode())

        for player in self.otherPlayers:
            for word in self.otherPlayers[player]:
                if(word.move()==False):
                    self.otherPlayers[player].remove(word)
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
    setupScene(render)
    base.run()
 
def loginScreen():
    clearScreen()
    text = TextNode("Username")
    text.setText("Username")
    text.setTextColor(0, 0, 0, 1)
    textNodePath = aspect2d.attachNewNode(text)
    textNodePath.setScale(.15)
    textNodePath.setPos(0,0,.2)
    entry = DirectEntry(text = "", scale=.2, command=menuScreen,
    initialText="", numLines = 2, focus=1,
     frameSize = (-1.0,0,0,0))

    #pGraphic = PlayerGraphic(-.2, 2, -.2, "player", "myName", server)
    global nodePaths
    nodePaths.append(textNodePath)
    nodePaths.append(entry)

def menuScreen(playerName):
    clearScreen()
    global myName
    myName= playerName
    global state
    state="menu"
    msg = "loginEvent %s\n" % myName
    server.send(msg.encode())
    setOnlineStatus(playerName, True)
    if(isTracked(playerName)==False): newPlayer(playerName)
    updateMenu()

def updateMenu():
    global nodePaths
    clearScreen()
    text = TextNode("Online Players")
    text.setTextColor(0, 0, 0, 1)
    toDisplay = "Click to Call! \n"
    online = getOnlinePlayers()
    space = 0
    if(len(online)==1):
        toDisplay+= "No players online!"
    for player in online:
        if(player == myName): continue
        # pGraphic = PlayerGraphic(render, -10 + space, 49, -5, player, myName, server)
        pGraphic = PlayerGraphic(-.2, 2, -.2, player, myName, server)
        nodePaths.append(pGraphic.getBobble())
        space += 5
    text.setText(toDisplay)
    textNodePath = aspect2d.attachNewNode(text)
    textNodePath.setScale(.15)
    textNodePath.setPos(-.2,0,.2)
    nodePaths.append(textNodePath)

def dialFriend(playerName, friend):
    clearScreen()
    global state
    state = "inCall"
    initializeListener(micIndex)
    game.loadModels()
    loadPrettyLayout(playerName, friend)
    #base.disableMouse()
    createGravity()

def clearScreen():
    global nodePaths
    for path in nodePaths:
        path.removeNode()
    nodePaths = []

def userLogOff():
    setOnlineStatus(myName, False)
    msg = "logoffEvent %s\n" % myName
    server.send(msg.encode())

if __name__ == "__main__":
    base.exitFunc = userLogOff
    game = Display()
    serverMsg = Queue(100)
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    start()
