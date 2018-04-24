from panda3d.core import *
from Utils.Picker import * 
class PlayerGraphic(object):
	def __init__(self, render, x, y, z, label, myPlayerName, server):
		self.x = x
		self.y = y
		self.z = z
		self.label = label
		self.server = server 
		self.myPlayerName = myPlayerName
		self.called = False
		path = "Graphics/models/greensphere.egg"
		self.sphere = loader.loadModel(path)
		self.myPicker = Picker(self.onHit)
		self.myPicker.makePickable(self.sphere, label)
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

	def onHit(self):
		ob = self.myPicker.getObjectHit(base.mouseWatcherNode.getMouse()) 
		#print(ob)
		if(ob!=None and self.called == False):
			self.called = True
			selection = ob.getTag("pickable")
			print(selection)
			msg = "callEvent %s %s\n"% (self.myPlayerName, selection)
			self.server.send(msg.encode())