from panda3d.core import *
class PlayerGraphic(object):
	def __init__(self, render, x, y, z, label):
		self.x = x
		self.y = y
		self.z = z
		self.label = label 
		path = "Graphics/models/greensphere.egg"
		self.sphere = loader.loadModel(path)
		#self.sphere.reparentTo(render)
		self.sphere.setPos(self.x, self.y, self.z)
		text = TextNode(label)
		text.setText(label)

		text.setAlign(TextNode.ACenter)
		textNode = self.sphere.attachNewNode(text)
		textNode.setScale(1.4)
		textNode.setPos(0,-2,0)
		self.sphere.reparentTo(render)
		
	def move(self, dx, dy, dz):
		(self.x, self.y, self.z) = (dx + self.x, dy + self.y, dz + self.z) 
		self.sphere.setPos(self.x, self.y, self.z)

	def getBobble(self):
		return self.sphere