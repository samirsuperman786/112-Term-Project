from panda3d.core import *
from direct.task.Task import Task
from direct.showbase import DirectObject
import direct.directbase.DirectStart
import random
from Utils.StringHelper import *
from panda3d.physics import *
from direct.filter.CommonFilters import CommonFilters

#got lighting from optional lecture
def setupLighting(activeScreen):
	#add one light per face, so each face is nicely illuminated
	filters = CommonFilters(base.win, base.cam)
	filters.setCartoonInk(.4)

	plight1 = PointLight('plight')
	plight1.setColor(VBase4(1, 1, 1, 1))
	plight1NodePath = activeScreen.attachNewNode(plight1)
	plight1NodePath.setPos(0, 0, 500)
	activeScreen.setLight(plight1NodePath)

	plight2 = PointLight('plight')
	plight2.setColor(VBase4(1, 1, 1, 1))
	plight2NodePath = activeScreen.attachNewNode(plight2)
	plight2NodePath.setPos(0, 0, -500)
	activeScreen.setLight(plight2NodePath)

	plight3 = PointLight('plight')
	plight3.setColor(VBase4(1, 1, 1, 1))
	plight3NodePath = activeScreen.attachNewNode(plight3)
	plight3NodePath.setPos(0, -500, 0)
	activeScreen.setLight(plight3NodePath)

	plight4 = PointLight('plight')
	plight4.setColor(VBase4(1, 1, 1, 1))
	plight4NodePath = activeScreen.attachNewNode(plight4)
	plight4NodePath.setPos(0, 500, 0)
	activeScreen.setLight(plight4NodePath)

	plight5 = PointLight('plight')
	plight5.setColor(VBase4(1, 1, 1, 1))
	plight5NodePath = activeScreen.attachNewNode(plight5)
	plight5NodePath.setPos(500,0, 0)
	activeScreen.setLight(plight5NodePath)

	plight6 = PointLight('plight')
	plight6.setColor(VBase4(1, 1, 1, 1))
	plight6NodePath = activeScreen.attachNewNode(plight6)
	plight6NodePath.setPos(-500,0, 0)
	activeScreen.setLight(plight6NodePath)

#got landscape from https://free3d.com/3d-model/desert-26147.html
def setupMenuBackground(activeScreen):
	scene = loader.loadModel("Graphics/models/landscape.egg")
	scene.reparentTo(activeScreen)
	scene.setScale(1)
	scenePos = (3.5, 4, -.3)
	scene.setPos(scenePos)
	Fish(activeScreen)

class Fish(object):
	def __init__(self, activeScreen):
		fish = loader.loadModel("Graphics/models/fish.egg")
		fish.reparentTo(activeScreen)
		fish.setPos(0, 6, -.3)
		self.rate = -2
		self.increasing = True
		taskMgr.doMethodLater(.02, self.move, "word", extraArgs = [fish], appendTask = True)

	def move(self, fish, task):
		(p, y, r) = fish.getHpr()
		fish.setHpr(p + self.rate, y, r)
		return task.again

#default background from panda3d
def loadBackground(activeScreen):
	scene = loader.loadModel("models/environment")
	scene.reparentTo(activeScreen)
	scene.setScale(.25)
	scene.setPos(60, 20, -2)

def loadPrettyLayout(myName, friendName, activeScreen):
	(x,y,z) = (-1,0,-.5)
	space = 2
	createTextAt(x, y, z, myName, activeScreen, "black", .1)
	createTextAt(x+space, y, z, friendName, activeScreen, "black", .1)

def createGravity():
    #add gravity
    base.enableParticles()
    gravityFN=ForceNode('world-forces')
    gravityFNP=render.attachNewNode(gravityFN)
    gravityForce=LinearVectorForce(0,0,-3) #gravity acceleration
    gravityFN.addForce(gravityForce)
    base.physicsMgr.addLinearForce(gravityForce)