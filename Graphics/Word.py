from panda3d.core import *
from direct.showbase import DirectObject
from Utils.Picker import *
import direct.directbase.DirectStart
from panda3d.physics import *

#Word object which tracks and moves its location
class Word(DirectObject.DirectObject):
	def __init__(self, color, render, x, y, z, label):
		self.x = x
		self.y = y
		self.z = z
		self.label = label 
		path = "Graphics/models/" + color + "sphere.egg"
		self.sphere = loader.loadModel(path)
		mousePicker = Picker()
		mousePicker.makePickable(self.sphere)
		#self.sphere.reparentTo(render)
		self.sphere.setPos(self.x, self.y, self.z)
		text = TextNode(label)
		text.setText(label)
		text.setAlign(TextNode.ACenter)
		textNode = self.sphere.attachNewNode(text)
		textNode.setPos(0,-2,0)
		####
		node = NodePath(label)
		node.reparentTo(render)
		an = ActorNode(label)
		anp = node.attachNewNode(an)
		base.physicsMgr.attachPhysicalNode(an)
		self.sphere.reparentTo(anp)
		an.getPhysicsObject().setMass(10)

		gravityFN=ForceNode('world-forces')
		gravityFNP=render.attachNewNode(gravityFN)
		gravityForce=LinearVectorForce(2,2,-4.9) #gravity acceleration
		gravityFN.addForce(gravityForce)
		 
		base.physicsMgr.addLinearForce(gravityForce)

		
	def move(self):
		(dx, dy, dz) = (0, 0, -.1)
		(self.x, self.y, self.z) = (dx + self.x, dy + self.y, dz + self.z) 
		self.sphere.setPos(self.x, self.y, self.z)
		if(self.z<-5):
		 	self.sphere.removeNode()
		 	return False
		return True
