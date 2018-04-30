from panda3d.core import *
from Utils.Picker import * 
from direct.showbase import DirectObject
import direct.directbase.DirectStart
from Utils.StringHelper import *

class clickableOption(object):
	def __init__(self, x, y, z, label, funcOnPress, activeScreen, color= "red"):
		self.x = x
		self.y = y
		self.z = z
		self.label = label
		self.funcOnPress = funcOnPress
		path = "Graphics/models/" + color + "sphere.egg"
		self.sphere = loader.loadModel(path)
		self.myPicker = Picker(self.onHit, activeScreen)
		self.myPicker.makePickable(self.sphere, label, label)
		self.sphere.setPos(self.x, self.y, self.z)
		self.sphere.setScale(.02)
		createTextAt(0, -2, .3, label, self.sphere, "black", 1.2)
		# text = TextNode(label)
		# text.setText(label)
		# text.setAlign(TextNode.ACenter)
		# text.setTextColor(0, 0, 0, 1)
		# textNode = self.sphere.attachNewNode(text)
		# textNode.setScale(1.2)
		# textNode.setPos(0,-2,.3)
		self.sphere.reparentTo(activeScreen)

	def onHit(self):
		if(base.mouseWatcherNode.hasMouse()):
			ob = self.myPicker.getObjectHit(base.mouseWatcherNode.getMouse()) 
			if(ob!=None):
				self.funcOnPress()


#calling selection
class PlayerGraphic(object):
	def __init__(self, x, y, z, label, myPlayerName, server, activeScreen):
		self.x = x
		self.y = y
		self.z = z
		self.label = label
		self.server = server 
		self.myPlayerName = myPlayerName
		self.called = False
		path = "Graphics/models/greensphere.egg"
		self.sphere = loader.loadModel(path)
		self.myPicker = Picker(self.onHit, activeScreen)
		self.myPicker.makePickable(self.sphere, label)
		self.sphere.setPos(self.x, self.y, self.z)
		self.sphere.setScale(.07)
		text = TextNode(label)
		text.setText(label)
		text.setAlign(TextNode.ACenter)
		text.setTextColor(0, 0, 0, 1)
		textNode = self.sphere.attachNewNode(text)
		textNode.setScale(1.2)
		textNode.setPos(0,-2,.3)
		self.sphere.reparentTo(activeScreen)
		
	def move(self, dx, dy, dz):
		(self.x, self.y, self.z) = (dx + self.x, dy + self.y, dz + self.z) 
		self.sphere.setPos(self.x, self.y, self.z)

	def getBobble(self):
		return self.sphere

	def onHit(self):
		if(base.mouseWatcherNode.hasMouse()):
			ob = self.myPicker.getObjectHit(base.mouseWatcherNode.getMouse()) 
			if(ob!=None and self.called == False):
				self.called = True
				selection = ob.getTag("pickable")
				msg = "tryDial %s %s\n"% (self.myPlayerName, selection)
				self.server.send(msg.encode())