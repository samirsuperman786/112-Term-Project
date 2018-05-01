from panda3d.core import *
from direct.showbase import DirectObject
from Utils.Picker import *
import direct.directbase.DirectStart
from panda3d.physics import *
import random
from Utils.StringHelper import *

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
		path = "Graphics/models/" + color + "sphere.egg"
		#sound from http://soundbible.com/670-Swooshing.html
		self.mySound = base.loader.loadSfx("Graphics/sounds/swoosh.ogg")
		self.sphere = loader.loadModel(path)
		self.sphere.setScale(1.2)
		self.myPicker = Picker(self.onHit, activeScreen, self.sphere)
		self.sphere.setPos(self.x, self.y, self.z)

		self.dy =0
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