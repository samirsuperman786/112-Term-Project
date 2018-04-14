from panda3d.core import *

class Word(object):
	words = []
	def __init__(self, render, x, y, z, label):
		self.x = x
		self.y = y
		self.z = z
		self.label = label 
		self.sphere = loader.loadModel("Graphics/models/sphere.egg")
		self.sphere.reparentTo(render)
		self.sphere.setPos(self.x, self.y, self.z)
		text = TextNode(label)
		text.setText(label)
		text.setAlign(TextNode.ACenter)
		textNode = self.sphere.attachNewNode(text)
		textNode.setPos(0,-2,0)
		Word.words.append(self)

	def move(self):
		(dx, dy, dz) = (0, 0, -.1)
		(self.x, self.y, self.z) = (dx + self.x, dy + self.y, dz + self.z) 

		self.sphere.setPos(self.x, self.y, self.z)
		if(self.z<-5):
			Word.words.remove(self)
			self.sphere.removeNode()