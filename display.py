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

class Display(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)
        self.words = []

        #load all the things
        self.loadBackground() # load lights and the fancy background
        self.loadModels()
        #key movement
        self.createKeyControls()

        self.keyMap = {}
        timer = 0.2
        taskMgr.doMethodLater(timer, self.move, "move")
        taskMgr.doMethodLater(1, self.getNewWord, "word")

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

    def move(self, task):
        (dx, dy, dz) = (0, 0, -.1)
        for word in self.words:
            (sphere, text) = word
            (x, y, z) = sphere.getPos()
            sphere.setPos(x + dx, y + dy, z + dz)
        return task.cont

    def getNewWord(self, task):
        if(phrases.empty()==False):
            (text, volume) = phrases.get()
            self.createText(text, (0, 20, 10))
        return task.again

    def createText(self, word, loc):
        #sphere
        text = TextNode(word)
        sphere = (loader.loadModel("Graphics/models/sphere.egg"))
        self.words.append((sphere, text))
        sphere.reparentTo(render)
        sphere.setPos(loc)
        text.setText(word)
        textNodePath = sphere.attachNewNode(text)
        text.setAlign(TextNode.ACenter)
        textNodePath.setScale(1)
        textNodePath.setPos(0,-2,0)

initializeListener()
game = Display()
game.createText("hi", (0, 20, 10))
base.run()





