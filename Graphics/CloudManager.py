from panda3d.core import *
import random

clouds = []
rainDrops = []

#loads clouds and places them with spacing
def loadClouds(activeScreen):
	global clouds
	global rainDrops
	clouds = []
	rainDrops = []
	(x, y, z) = (-10, 20, 5)
	numClouds = 4
	spacing = 35/numClouds

	for i in range(numClouds):
		position = ((spacing * i) + x, y, z)
		clouds.append(Cloud(activeScreen, position))

	loadRain(activeScreen)

def loadRain(activeScreen):
	(x, y, z) = (-5, 10, 5)
	numRainDrops = 10
	spacing = 1

	for i in range(numRainDrops):
		z = random.randint(0, 10)
		position = ((spacing * i) + x, y, z)
		rainDrops.append(RainDrop(activeScreen, position))

#moves all clouds every task interval
def moveClouds(task):
	for cloud in clouds:
		cloud.move()
	for rain in rainDrops:
		rain.move()
	return task.again

#Cloud object that tracks position
class Cloud(object):
	def __init__(self, activeScreen, position):
		path = "Graphics/models/cloud.egg"
		(x, y, z) = position
		self.cloud = loader.loadModel(path)
		self.position = position
		self.cloud.reparentTo(activeScreen)
		self.cloud.setPos(x, y, z)
		self.speed = .1

	def move(self):	
		(x,y,z) = self.position
		if(x<-10 or x>10):
			self.speed*=-1
		x+=self.speed
		self.position = (x, y, z)
		self.cloud.setPos(x, y, z)

#Cloud object that tracks position
class RainDrop(object):
	def __init__(self, activeScreen, position):
		path = "Graphics/models/rain.egg"
		(x, y, z) = position
		self.rainDrop = loader.loadModel(path)
		self.rainDrop.reparentTo(activeScreen)
		self.rainDrop.setPos(x, y, z)
		self.speed = .1

	def move(self):	
		(x,y,z) = self.rainDrop.getPos()
		z-=self.speed
		self.rainDrop.setPos(x, y, z)
		if(z<-5):
			self.rainDrop.setPos(x, y, z+10)
