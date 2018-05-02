from panda3d.core import *
from direct.showbase import DirectObject
from Utils.Picker import *
import direct.directbase.DirectStart
from panda3d.physics import *
import random
from Utils.StringHelper import *
import math

#Word object which tracks and moves its location
class Word(DirectObject.DirectObject):
	def __init__(self, myName, activeScreen, x, y, z, label, color, server,):
		self.x = x
		self.y = y
		self.z = z
		self.label = label
		self.server = server
		self.activeScreen = activeScreen
		self.myName = myName
		self.color = color
		path = "Graphics/models/" + color + "sphere.egg"
		#sound from http://soundbible.com/670-Swooshing.html
		self.mySound = base.loader.loadSfx("Graphics/sounds/swoosh.ogg")
		self.sphere = loader.loadModel(path)
		self.sphere.setScale(1.2)
		self.myPicker = Picker(self.onHit, activeScreen, self.sphere)
		self.sphere.setPos(self.x, self.y, self.z)

		self.dy =0
		self.r = 0
		self.stop = False
		createTextAt(0, -2, 0, label, self.sphere, "black", .8)
		####
		node = NodePath(label)
		node.reparentTo(activeScreen)
		an = ActorNode(label)
		anp = node.attachNewNode(an)
		base.physicsMgr.attachPhysicalNode(an)
		self.sphere.reparentTo(anp)
		an.getPhysicsObject().setMass(3)
		self.animations = list()
		self.pulse()

	def pulse(self):
		self.r = 2
		colors = ["blue", "green", "red"]
		for i in range(1, 5):
			angle = (- 2 * math.pi)/i
			x = self.r * math.cos(angle)
			z = self.r * math.sin(angle)
			color = random.choice(colors)
			animation = loader.loadModel("Graphics/models/" + self.color + "sphere.egg")
			animation.reparentTo(self.sphere)
			animation.setPos(x, -2, z)
			animation.setScale(.05)
			self.animations.append(animation)
		taskMgr.doMethodLater(.02, self.moveAnimations, "word")

	def moveAnimations(self, task):
		self.r *= 1.05
		for i in range(len(self.animations)):
			animation = self.animations[i] 
			angle = (- 2 * math.pi)/(i + 1)
			x = self.r * math.cos(angle)
			z = self.r * math.sin(angle)
			animation.setPos(x, -2, z)
		if(self.r<10):
			return task.again

	def getText(self):
		return self.label

	def getObj(self):
		return self.sphere
		
	def move(self):
		(x, y, z) = self.sphere.getPos(self.activeScreen)
		if(z<-10):
			self.myPicker.destroy()
			self.stop = True
			return False
		return True

	def throwWord(self):
		#self.mySound.play()
		taskMgr.doMethodLater(.02, self.spiralWord, "word")

	def spiralWord(self, task):
		if(self.stop==False):
			(x, y, z) = self.sphere.getPos()
			d = .1
			self.dy += d
			self.sphere.setPos(x, y + self.dy, z)
			if(self.dy>10):
				self.dy = 0
				return None
			return task.again

	def onHit(self):
		if(base.mouseWatcherNode.hasMouse()):
			ob = self.myPicker.getObjectHit(base.mouseWatcherNode.getMouse()) 
			if(ob!=None):
				msg = "moveWord %s %s\n" % (self.label, self.myName)
				self.server.send(msg.encode()) 