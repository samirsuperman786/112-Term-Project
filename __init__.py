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
import random

server = None

class Struct(object): pass
data = Struct()

def runGame():
    global data
    initializeConstants()
    initializeVariables()
    loginScreen()
    setupLighting(render)
    startTasks()
    base.run()

#connects to server
def connectToServer():
    global server
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

#sets up default values
def initializeVariables():
    global data
    data.activeScreen3d = render.attachNewNode("activescreen")
    data.activeScreen2d = aspect2d.attachNewNode("activescreen")
    data.buttonScreen = render.attachNewNode("buttons")
    data.micIndex = None
    data.otherPlayers = dict()
    clearPersonalData()

#clears all data thats important per player
def clearPersonalData():
    global data
    data.state = ""
    data.myName = ""
    data.friend = ""
    data.transcript = []
    data.words = []
    data.friendButton = None
    data.buttons = []
    data.ringtone = None
    data.music = None

#stores important locations
def initializeConstants():
    global data
    data.centerScreenPos = (.35, 0, .1)
    data.logoutButtonLoc = (-.4, 1.1, -.25)
    data.menuButtonLoc = data.logoutButtonLoc
    data.friendButtonLoc = (-.1, 1.1, -.25)

#loads clouds and scene
def loadModels():
    global data
    loadClouds(data.activeScreen3d)
    loadBackground(data.activeScreen3d)

def loadMusic():
    global data
    data.music = base.loader.loadSfx("Graphics/sounds/relaxing.ogg")
    data.music.play() 

#starts all tasks to run in background
def startTasks():
    newWordTimer = .7
    moveCloudTimer = .02
    updateTimer = .2
    taskMgr.doMethodLater(updateTimer, update, "update")
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
                if(playerName!=data.myName):
                    if(playerName in data.otherPlayers):
                        del data.otherPlayers[playerName]
                    if(data.state=="menu"):
                        updateMenu()
                    elif(data.state== "inCall"):
                        if(data.friend == playerName):
                            data.friend = ""
                            stopListener()
                            goBackToMenu()
            elif(command == "tryDial"):
                if(data.state=="menu"):
                    player1 = msg[2]
                    player2 = msg[3]
                    if(player1 == data.myName):
                        dialingMenu(data.myName, player2)
                    elif(player2 == data.myName):
                        acceptMenu(data.myName, player1)
            elif(command == "acceptCall"):
                player1 = msg[2]
                player2 = msg[3]
                if(data.myName == player1 or data.myName == player2):
                    dialFriend()
            elif(command == "declineCall"):
                player1 = msg[2]
                player2 = msg[3]
                if(data.myName==player1 or data.myName == player2):
                    data.friend = None 
                    goBackToMenu()
            elif(command == "newWord"):
                if(data.state=="inCall"):
                    label = msg[2]
                    playerName = msg[3]
                    if(data.myName==playerName or data.friend ==playerName):
                        (x,y,z) = (8, 35, 10)
                        color = "red"
                        textLine = data.friend + ": " + label
                        if(playerName ==data.myName):
                            x = -8
                            color = "blue"
                            textLine = data.myName + ": " + label
                        data.transcript.append(textLine)
                        newWord = Word(playerName, data.activeScreen3d, x, y, z, label, color, server)
                        data.otherPlayers[playerName].append(newWord)
            elif(command == "moveWord"):
                if(data.state=="inCall"):
                    label = msg[2]
                    playerName = msg[3]
                    for word in data.otherPlayers[playerName]:
                        if(word.getText()==label):
                            word.throwWord()
        except:
            print(msg)
            print("failed")
        serverMsg.task_done()
    return task.cont

#grabs words from listenermanager
def getNewWord(task):
    global data
    global phrases
    (startX, startY, startZ) = (-8, 35, 10)
    if(phrases.empty()==False):
        label = phrases.get()
        msg = "newWord %s %s\n" % (label, data.myName)
        server.send(msg.encode())

    for player in data.otherPlayers:
        newWordList = []
        for word in data.otherPlayers[player]:
            if(word.move()):
                newWordList.append(word)
        data.otherPlayers[player] = newWordList
    return task.again

def createLogoutButton():
    global data
    (cx, cy, cz) = data.logoutButtonLoc
    co = clickableOption(cx, cy, cz, "Logout", goBackToLogin, data.buttonScreen)
    data.buttons.append(co)

def createMenuButton():
    global data
    (cx, cy, cz) = data.menuButtonLoc
    co = clickableOption(cx, cy, cz, "Menu", goBackToMenu, data.buttonScreen)
    data.buttons.append(co)

def removeFriendButton():
    global data
    if(data.friendButton!=None):
        data.friendButton.destroy()
        data.friendButton.getObj().removeNode()

def createAddFriendButton():
    global data
    removeFriendButton()
    
    if(data.friend in getFriends(data.myName)):
        text = "UnFriend"
        color = "red"
    else:
        text = "Friend"
        color = "green"
    (cx, cy, cz) = data.friendButtonLoc
    co = clickableOption(cx, cy, cz, text, toggleFriend, data.buttonScreen, color)
    data.friendButton = co

#toggles whether to add/remove a friend
def toggleFriend():
    global data
    if(data.friend in getFriends(data.myName)):
        removeFriend(data.myName, data.friend)
    else:
        addFriend(data.myName, data.friend)
    createAddFriendButton()

def goBackToLogin():
    global data
    if(data.myName!=""):
        userLogOff()
    loginScreen()

def goBackToMenu(tmp=None):
    global data
    data.state = "menu"
    updateMenu()
    loadMusic()

def loginScreen():
    global data
    clearScreen()
    clearPersonalData()
    data.state = "login"
    loadMusic()
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

def updateMenu():
    global data
    clearScreen()
    stopRinging()
    setupMenuBackground(data.activeScreen3d)
    toDisplay = "Online Players:"
    online = getOnlinePlayers()
    space = 0
    (cx, cy, cz) = data.centerScreenPos
    if(len(online)==1):
        toDisplay+= "\nNo players online!"
    for player in online:
        if(player == data.myName): continue
        color = "blue"
        if(player in getFriends(data.myName)):
            color = "green"
        co = PlayerGraphic(-.2 + space, 2, -.2, player, data.myName, server, data.activeScreen3d, color)
        data.buttons.append(co)
        space += .2
    createTextAt(1.3, 0, -.9, data.myName, data.activeScreen2d)
    createTextAt(cx, cy, cz, toDisplay, data.activeScreen2d)
    createLogoutButton()

def acceptMenu(playerName, friend):
    global data
    data.state = "calling"
    data.friend = friend
    print("Incoming call!")
    clearScreen()
    stopMusic()
    createTextAt(.4,1,.2, "Incoming call from\n" + friend, data.activeScreen2d)
    setupMenuBackground(data.activeScreen3d)
    co1 = clickableOption(.2, 1.1, -.2, "Decline", declineCall, data.buttonScreen, "red")
    co2 = clickableOption(-.1, 1.1, -.2, "Accept", acceptCall, data.buttonScreen, "green")
    data.buttons.append(co1)
    data.buttons.append(co2)
    #ringtone http://soundbible.com/1407-Phone-Ringing.html
    data.ringtone = base.loader.loadSfx("Graphics/sounds/ringtone.ogg")
    data.ringtone.play()

def dialingMenu(playerName, friend):
    global data
    data.state = "calling"
    data.friend = friend
    print("Dialing!")
    clearScreen()
    stopMusic()
    setupMenuBackground(data.activeScreen3d)
    co = clickableOption(.2, 1.1, -.2, "Hangup", declineCall, data.buttonScreen, "red") 
    data.buttons.append(co)
    createTextAt(.4, 1, .2, "Calling " + friend, data.activeScreen2d)

def dialFriend():
    global data
    data.state = "inCall"
    clearScreen()
    stopRinging()
    initializeListener(data.micIndex)
    loadPrettyLayout(data.myName, data.friend, data.activeScreen2d)
    createGravity()
    co = clickableOption(-.25, 1.1, -.25, "Transcript", downloadTranscript, data.buttonScreen)
    data.buttons.append(co)
    loadModels()
    (x,y,z) = data.menuButtonLoc
    co = clickableOption(x, y, z, "Hangup", declineCall, data.buttonScreen, "red") 
    data.buttons.append(co)
    createAddFriendButton()

def acceptCall():
    global data
    msg = "acceptCall %s %s\n" % (data.myName, data.friend)
    server.send(msg.encode())

def declineCall():
    global data
    msg = "declineCall %s %s\n" % (data.myName, data.friend)
    server.send(msg.encode())

def stopRinging():
    global data
    if(data.ringtone!=None):
        data.ringtone.stop()
        data.ringtone = None

def stopMusic():
    global data
    if(data.music!=None):
        data.music.stop()
        data.music = None

def clearScreen():
    global data

    for button in data.buttons:
        button.destroy()

    data.buttons = []

    for path in data.buttonScreen.getChildren():
        path.removeNode()

    for path in data.activeScreen3d.getChildren():
        path.removeNode()

    for path in data.activeScreen2d.getChildren():
        path.removeNode()

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

def setupWindow():
    wp = WindowProperties() 
    wp.setSize(1920, 1080) 
    wp.setTitle("ChatWorld")
    base.win.requestProperties(wp) 
    base.disableMouse()

if __name__ == "__main__":
    connectToServer()
    base.exitFunc = userLogOff
    setupWindow()
    serverMsg = Queue(100)
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    runGame()