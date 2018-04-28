#Server code adapted from optional lectures

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
from Graphics.MenuBobble import *

import socket
import threading
from queue import Queue
import copy
import time
import datetime


class Struct(object): pass
data = Struct()
data.activeScreen3d = render.attachNewNode("activescreen")
data.activeScreen2d = aspect2d.attachNewNode("activescreen")
# nodePaths = []
# state = ""
# myName = ""
# micIndex = None
# leftRegion = (-4, 35, 8)
# scene = None

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
        global data
        loadClouds(data.activeScreen3d)
        loadBackground(data.activeScreen3d)
        #timerFired
        newWordTimer = .7
        moveCloudTimer = .02
        taskMgr.doMethodLater(newWordTimer, self.getNewWord, "word")
        taskMgr.doMethodLater(moveCloudTimer, moveClouds, "cloud")

    #Updates the display and gets new words
    def update(self, task):
        while (serverMsg.qsize() > 0):
            msg = serverMsg.get(False)
            try:
                #print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]
                global data
                if(command== "myIDis"):
                    self.myPID = msg[1]
                    self.otherPlayers[self.myPID] =[]
                elif(command == "myMicIs"):
                    data.micIndex = int(msg[1])
                    self.micIndex = int(msg[1])
                elif(command == "newPlayer"):
                    newPID = msg[1]
                    self.otherPlayers[newPID] = list()
                elif(command == "loginEvent" or command == "logoffEvent"):
                    if(data.state=="menu"):
                        updateMenu()
                    elif(data.state== "inCall"):
                        player = msg[2]
                        if(data.friend == player):
                            phrases.put("Disconnected")
                            data.friend = ""
                            stopListener()
                            taskMgr.doMethodLater(3, goBackToMenu, "back")
                elif(command == "callEvent"):
                    if(data.state=="menu"):
                        data.state = "inCall"
                        player1 = msg[2]
                        player2 = msg[3]
                        if(player1 == data.myName):
                            dialFriend(data.myName, player2)
                        elif(player2 == data.myName):
                            dialFriend(data.myName, player1)
                elif(command == "newWord"):
                    if(data.state=="inCall"):
                        PID = msg[1]
                        label = msg[2]
                        (x,y,z) = (8, 35, 10)
                        color = "red"
                        textLine = data.friend + ": " + label
                        if(PID ==self.myPID):
                            x = -8
                            color = "blue"
                            textLine = data.myName + ": " + label
                        data.transcript.append(textLine)
                        newWord = Word(data.activeScreen3d, x, y, z, label, color)
                        self.otherPlayers[PID].append(newWord)
                elif(command == "popWord"):
                    if(data.state=="inCall"):
                        PID = msg[1]
                        label = msg[2]
                        (x, y, z) = msg[3], msg[4], msg[5]
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

def initializeVariables():
    global data
    data.state = ""
    data.myName = ""
    data.micIndex = None
    data.leftRegion = (-4, 35, 8)
    data.friend = ""
    data.transcript = []

def goBackToLogin():
    global data
    if(data.myName!=""):
        userLogOff()
    clearScreen()
    loginScreen()

def goBackToMenu(tmp):
    global data
    data.state="menu"
    msg = "loginEvent %s\n" % data.myName
    server.send(msg.encode())
    updateMenu()

def start():
    global data
    loginScreen()
    setupLighting(render)
    clickableOption(-.4, 1.1, -.25, "Menu", goBackToLogin, render)
    base.run()

def loginScreen():
    global data
    initializeVariables()
    data.state = "login"
    setupMenuBackground(data.activeScreen3d)
    text = TextNode("Username")
    text.setText("What's your name?")
    text.setTextColor(0, 0, 0, 1)
    textNodePath = data.activeScreen2d.attachNewNode(text)
    textNodePath.setScale(.15)
    textNodePath.setPos(-.2,0,.1)
    entry = DirectEntry(text = "", scale=.2, command=passwordScreen,
    initialText="", numLines = 2, focus=1,
     frameSize = (-1.0,0,0,0))
    entry.setPos(-.2,0,-.1)
    entry.reparentTo(data.activeScreen2d)

def passwordScreen(playerName, attempts = 0):
    global data
    clearScreen()
    setupMenuBackground(data.activeScreen3d)
    wrongNodePath = None
    if(attempts!=0):
        wrongEntry= TextNode("wrong")
        wrongEntry.setTextColor(256, 0, 0, 1)
        wrongEntry.setText("X")
        wrongNodePath = data.activeScreen2d.attachNewNode(wrongEntry)
        wrongNodePath.setScale(.15)
        wrongNodePath.setPos(-.3,0,-.2)
    data.state = "password"
    entry = DirectEntry(text = "", scale=.2, command=menuScreen,
     extraArgs = [playerName], obscured=1, initialText="",
      numLines = 2, focus=1, frameSize = (-1.0,0,0,0))
    entry.setPos(-.2,0,-.2)
    entry.reparentTo(data.activeScreen2d)
    text = TextNode("password")
    text.setTextColor(0, 0, 0, 1)
    if(isTracked(playerName)==False):
        toDisplay = "New player!\nEnter a new password: \n"
    else:
        toDisplay = "Welcome back!\nEnter your password: \n"
    text.setText(toDisplay)
    textNodePath = data.activeScreen2d.attachNewNode(text)
    textNodePath.setScale(.15)
    textNodePath.setPos(-.2,0,.2)

def menuScreen(input, playerName):
    global data
    if(isTracked(playerName)==False): newPlayer(playerName, input)
    if(doPasswordsMatch(input, getStoredPassword(playerName))==False):
        passwordScreen(playerName, 1)
        return
    data.myName= playerName
    data.state="menu"
    msg = "loginEvent %s\n" % data.myName
    server.send(msg.encode())
    setOnlineStatus(data.myName, True)
    updateMenu()

def updateMenu():
    global data
    clearScreen()
    setupMenuBackground(data.activeScreen3d)
    text = TextNode("Online Players")
    text.setTextColor(0, 0, 0, 1)
    toDisplay = "Click to Call: \n"
    online = getOnlinePlayers()
    space = 0
    if(len(online)==1):
        toDisplay+= "No players online!"
    for player in online:
        if(player == data.myName): continue
        PlayerGraphic(-.2, 2, -.2, player, data.myName, server, data.activeScreen3d)
        space += 5
    text.setText(toDisplay)
    textNodePath = data.activeScreen2d.attachNewNode(text)
    textNodePath.setScale(.15)
    textNodePath.setPos(-.2,0,.2)

def dialFriend(playerName, friend):
    global data
    print("DIALING!")
    data.friend = friend
    clearScreen()
    initializeListener(data.micIndex)
    loadPrettyLayout(playerName, friend, data.activeScreen2d)
    #base.disableMouse()
    createGravity()
    clickableOption(-.25, 1.1, -.25, "Transcript", downloadTranscript, data.activeScreen3d)
    game.loadModels()

def clearScreen():
    global data
    for path in data.activeScreen3d.getChildren():
        path.detachNode()

    for path in data.activeScreen2d.getChildren():
        path.detachNode()

def userLogOff():
    global data
    setOnlineStatus(data.myName, False)
    msg = "logoffEvent %s\n" % data.myName
    server.send(msg.encode())
    stopListener()

def downloadTranscript():
    ts = time.time()
    fileName = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
    path = os.environ["HOMEPATH"] + os.sep + "Desktop" + os.sep + fileName + ".txt"
    f = open(path,"w+")
    for line in data.transcript:
        f.write(line + "\n")
    f.close()

if __name__ == "__main__":
    base.exitFunc = userLogOff
    wp = WindowProperties() 
    wp.setSize(1920, 1080) 
    wp.setTitle("ChatWorld")
    base.win.requestProperties(wp) 
    base.disableMouse()
    game = Display()
    serverMsg = Queue(100)
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    start()
