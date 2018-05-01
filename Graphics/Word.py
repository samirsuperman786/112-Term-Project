from panda3d.core import *
from direct.showbase import DirectObject
from Utils.Picker import *
import direct.directbase.DirectStart
from panda3d.physics import *
import random
from Utils.StringHelper import *

#Word object which tracks and moves its location
class Word(DirectObject.DirectObject):
	def __init__(self, activeScreen, x, y, z, label, color, server):
		self.x = x
		self.y = y
		self.z = z
		self.label = label
		self.server = server
		path = "Graphics/models/" + color + "sphere.egg"
		self.sphere = loader.loadModel(path)
		self.sphere.setScale(1.1)
		self.myPicker = Picker(self.onHit, activeScreen, self.sphere)
		self.sphere.setPos(self.x, self.y, self.z)

		createTextAt(0, -2, 0, label, self.sphere, "black", 1.3)
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
		(x, y, z) = self.sphere.getPos() 
		if(z<-5):
			self.sphere.removeNode()
			return False
		return True

	def onHit(self):
		if(base.mouseWatcherNode.hasMouse()):
			ob = self.myPicker.getObjectHit(base.mouseWatcherNode.getMouse()) 
			if(ob!=None):
				(choice1, choice2) = (self.getChoice(), self.getChoice())
				newPos = None
				if(choice1 == "move" or choice2 == "move"):
					(x,y,z) = ob.getPos()
					(dx,dy,dz) = (random.randint(0,5),random.randint(0,5),random.randint(0,5))
					newPos = x+dx,y+dy,z+dz
				else:
					newPos = (0,0,-20)
				(x, y, z) = newPos
				ob.setPos(newPos)
				msg = "popWord %s\n" % (self.label)
				#self.server.send(msg.encode())
				self.myPicker.destroy() 

	def getChoice(self):
		return random.choice(["pop", "move", "move"])

