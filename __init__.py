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
from Utils.StringHelper import *

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
    data.friend = ""
    data.transcript = []
    data.words = []
    data.otherPlayers = dict()
    #data.myPID = None

def clearPersonalData():
    global data
    data.state = ""
    data.myName = ""
    data.friend = ""
    data.transcript = []
    data.words = []

def initializeConstants():
    global data
    data.centerScreenPos = (.35, 0, .1)
    data.logoutButtonLoc = (-.4, 1.1, -.25)
    data.menuButtonLoc = (-.4, 1.1, -.25)

def loadModels():
    global data
    loadClouds(data.activeScreen3d)
    loadBackground(data.activeScreen3d)
    newWordTimer = .7
    moveCloudTimer = .02
    taskMgr.doMethodLater(newWordTimer, getNewWord, "word")
    taskMgr.doMethodLater(moveCloudTimer, moveClouds, "cloud")

#Updates the display and gets new words
def update(task):
    while (serverMsg.qsize() > 0):
        msg = serverMsg.get(False)
        try:
            #print("received: ", msg, "\n")
            msg = msg.split()
            command = msg[0]
            global data
            if(command== "myIDis"):
                pass
                #data.myPID = msg[1]
                #data.otherPlayers[data.myPID] =[]
            elif(command == "myMicIs"):
                data.micIndex = int(msg[1])
            elif(command == "newPlayer"):
                #newPID = msg[1]
                #data.otherPlayers[newPID] = list()
                pass
            elif(command == "loginEvent"):
                playerName = msg[2]
                if(playerName!=data.myName):
                    data.otherPlayers[playerName] = list()
                if(data.state=="menu"):
                    updateMenu()
            elif(command == "logoffEvent"):
                playerName = msg[2]
                if(playerName in data.otherPlayers):
                    del data.otherPlayers[playerName]
                if(data.state=="menu"):
                    updateMenu()
                elif(data.state== "inCall"):
                    if(data.friend == playerName):
                        Word(data.activeScreen3d, -8, 35, 10,
                         "Disconnected", "red", server)
                        data.friend = ""
                        stopListener()
                        data.state = "menu"
                        taskMgr.doMethodLater(3, goBackToMenu, "back")
            elif(command == "tryDial"):
                if(data.state=="menu"):
                    player1 = msg[2]
                    player2 = msg[3]
                    if(player1 == data.myName):
                        #acceptMenu(player1, player2)
                        dialingMenu(data.myName, player2)
                        #dialFriend(data.myName, player2)
                    elif(player2 == data.myName):
                        acceptMenu(player2, player1)
                        #dialFriend(data.myName, player1)
            elif(command == "acceptCall"):
                player1 = msg[2]
                player2 = msg[3]
                if(data.myName == player1 or data.myName == player2):
                    dialFriend()
            elif(command == "declineCall"):
                player1 = msg[2]
                player2 = msg[3]
                if(data.myName==player1 or data.myName == player2):
                    goBackToMenu()
                    data.friend = None 
            elif(command == "newWord"):
                if(data.state=="inCall"):
                    label = msg[2]
                    playerName = msg[3]
                    (x,y,z) = (8, 35, 10)
                    color = "red"
                    textLine = data.friend + ": " + label
                    if(playerName ==data.myName):
                        x = -8
                        color = "blue"
                        textLine = data.myName + ": " + label
                    data.transcript.append(textLine)
                    newWord = Word(data.activeScreen3d, x, y, z, label, color, server)
                    data.otherPlayers[playerName].append(newWord)
            elif(command == "popWord"):
                if(data.state=="inCall"):
                    label = msg[2]
                    (x, y, z) = (int(msg[3]), int(msg[4]), int(msg[5]))
                    for player in data.otherPlayers:
                        for word in data.otherPlayers[player]:
                            if(word.getText()==label):
                                word.getObj().setPos(x,y,z)
        except:
            print(msg)
            print("failed")
        serverMsg.task_done()
    return task.cont

#grabs words from listenermanager
def getNewWord(task):
    global data
    (startX, startY, startZ) = (-8, 35, 10)
    if(phrases.empty()==False):
        label = phrases.get()
        msg = "newWord %s %s\n" % (label, data.myName)
        server.send(msg.encode())

    for player in data.otherPlayers:
        for word in data.otherPlayers[player]:
            if(word.move()==False):
                data.otherPlayers[player].remove(word)
    return task.again

def createLogoutButton():
    global data
    (cx, cy, cz) = data.logoutButtonLoc
    clickableOption(cx, cy, cz, "Logout", goBackToLogin, data.activeScreen3d)

def createMenuButton():
    global data
    (cx, cy, cz) = data.menuButtonLoc
    clickableOption(cx, cy, cz, "Menu", goBackToMenu, data.activeScreen3d)

def goBackToLogin():
    global data
    if(data.myName!=""):
        userLogOff()
    clearScreen()
    loginScreen()

def goBackToMenu(tmp=None):
    global data
    if(data.state=="inCall"):
        declineCall()
    data.state = "menu"
    # msg = "loginEvent %s\n" % data.myName
    # server.send(msg.encode())
    updateMenu()

def start():
    global data
    loginScreen()
    setupLighting(render)
    base.run()

def loginScreen():
    global data
    clearPersonalData()
    data.state = "login"
    setupMenuBackground(data.activeScreen3d)
    (cx, cy, cz) = data.centerScreenPos
    createTextAt(cx, cy, cz, "What's your name?", data.activeScreen2d)
    entry = DirectEntry(text = "", scale=.2, command=passwordScreen,
    initialText="", numLines = 2, focus=1,
     frameSize = (-1.0,0,0,0))
    entry.setPos(-.2,0,-.1)
    entry.reparentTo(data.activeScreen2d)

def passwordScreen(playerName, attempts = 0):
    global data
    clearScreen()
    setupMenuBackground(data.activeScreen3d)
    (cx, cy, cz) = data.centerScreenPos
    (shiftedX, shiftedY, shiftedZ) = (-.55, 0, -.3)
    wrongNodePath = None
    if(attempts!=0):
        createTextAt(-.3, 0, -.2, "X", data.activeScreen2d, "red")
    data.state = "password"
    entry = DirectEntry(text = "", scale=.2, command=menuScreen,
     extraArgs = [playerName], obscured=1, initialText="",
      numLines = 2, focus=1, frameSize = (-1.0,0,0,0))
    entry.setPos(cx + shiftedX, cy + shiftedY, cz + shiftedZ)
    entry.reparentTo(data.activeScreen2d)
    if(isTracked(playerName)==False):
        toDisplay = "New player!\nEnter a new password: \n"
    else:
        toDisplay = "Welcome back!\nEnter your password: \n"

    createTextAt(cx, cy, cz + .1, toDisplay, data.activeScreen2d)
    createLogoutButton()

def menuScreen(input, playerName):
    global data
    if(isTracked(playerName)==False): newPlayer(playerName, input)
    if(doPasswordsMatch(input, getStoredPassword(playerName))==False):
        passwordScreen(playerName, 1)
        return
    data.otherPlayers[playerName] = list()
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
    toDisplay = "Click to Call: \n"
    online = getOnlinePlayers()
    space = 0
    if(len(online)==1):
        toDisplay+= "No players online!"
    for player in online:
        if(player == data.myName): continue
        PlayerGraphic(-.2 + space, 2, -.2, player, data.myName, server, data.activeScreen3d)
        space += .2
    createTextAt(1.3, 0, -.9, data.myName, data.activeScreen2d)
    createTextAt(.35, 0, .2, toDisplay, data.activeScreen2d)
    createLogoutButton()

def acceptMenu(playerName, friend):
    global data
    data.state = "inCall"
    data.friend = friend
    print("Incoming call!")
    clearScreen()
    createTextAt(.4,1,.2, "Incoming call from\n" + friend, data.activeScreen2d)
    setupMenuBackground(data.activeScreen3d)
    clickableOption(.2, 1.1, -.2, "Decline", declineCall, data.activeScreen3d, "red")
    clickableOption(-.1, 1.1, -.2, "Accept", acceptCall, data.activeScreen3d, "green")
    createMenuButton()

def dialingMenu(playerName, friend):
    global data
    data.state = "calling"
    data.friend = friend
    print("Dialing!")
    clearScreen()
    setupMenuBackground(data.activeScreen3d)
    clickableOption(.2, 1.1, -.2, "Hangup", declineCall, data.activeScreen3d, "red") 
    createTextAt(.4, 1, .2, "Calling " + friend, data.activeScreen2d)
    createMenuButton()

def dialFriend():
    global data
    data.state = "inCall"
    clearScreen()
    initializeListener(data.micIndex)
    loadPrettyLayout(data.myName, data.friend, data.activeScreen2d)
    #base.disableMouse()
    createGravity()
    clickableOption(-.25, 1.1, -.25, "Transcript", downloadTranscript, data.activeScreen3d)
    loadModels()
    createMenuButton()

def acceptCall():
    global data
    msg = "acceptCall %s %s\n" % (data.myName, data.friend)
    server.send(msg.encode())

def declineCall():
    global data
    msg = "declineCall %s %s\n" % (data.myName, data.friend)
    server.send(msg.encode())
    data.friend = None

def clearScreen():
    global data
    for path in data.activeScreen3d.getChildren():
        path.detachNode()

    for path in data.activeScreen2d.getChildren():
        path.detachNode()

def userLogOff():
    global data
    msg = "logoffEvent %s\n" % data.myName
    server.send(msg.encode())
    data.state = "logoff"
    setOnlineStatus(data.myName, False)
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
    initializeConstants()
    taskMgr.doMethodLater(.2, update, "update")
    initializeVariables()
    serverMsg = Queue(100)
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    start()
