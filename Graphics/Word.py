from panda3d.core import *

#Word object which tracks and moves its location
class Word(object):
	def __init__(self, color, render, x, y, z, label):
		self.x = x
		self.y = y
		self.z = z
		self.label = label 
		path = "Graphics/models/" + color + "sphere.egg"
		self.sphere = loader.loadModel(path)
		self.sphere.reparentTo(render)
		self.sphere.setPos(self.x, self.y, self.z)
		text = TextNode(label)
		text.setText(label)
		text.setAlign(TextNode.ACenter)
		textNode = self.sphere.attachNewNode(text)
		textNode.setPos(0,-2,0)

	def move(self):
		(dx, dy, dz) = (0, 0, -.1)
		(self.x, self.y, self.z) = (dx + self.x, dy + self.y, dz + self.z) 
		self.sphere.setPos(self.x, self.y, self.z)
		if(self.z<-5):
		 	self.sphere.removeNode()
		 	return False
		return True