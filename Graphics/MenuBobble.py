from panda3d.core import *
from Utils.Picker import * 
from direct.showbase import DirectObject
import direct.directbase.DirectStart
from Utils.StringHelper import *

class Option(object):
	def __init__(self, x, y, z, label, activeScreen, color):
		(self.x, self.y, self.z) = (x, y, z)
		self.label = label
		color = color
		path = "Graphics/models/" + color + "sphere.egg"
		self.sphere = loader.loadModel(path)
		self.sphere.setPos(self.x, self.y, self.z)
		self.sphere.reparentTo(activeScreen)
		self.mySound = base.loader.loadSfx("Graphics/sounds/pop.ogg")
		createTextAt(0, -2, .3, label, self.sphere, "black", 1)

	def getObj(self):
		return self.sphere

	def destroy(self):
		self.myPicker.destroy()

class clickableOption(Option):
	def __init__(self, x, y, z, label, funcOnPress, activeScreen, color= "red"):
		super().__init__(x, y, z, label, activeScreen, color)
		self.funcOnPress = funcOnPress
		self.myPicker = Picker(self.onHit, activeScreen, self.sphere, label, label)
		self.sphere.setScale(.025)

	def onHit(self):
		if(base.mouseWatcherNode.hasMouse()):
			ob = self.myPicker.getObjectHit(base.mouseWatcherNode.getMouse()) 
			if(ob!=None):
				self.funcOnPress()
				self.mySound.play()


#calling selection
class PlayerGraphic(Option):
	def __init__(self, x, y, z, label, myPlayerName, server, activeScreen, color):
		super().__init__(x, y, z, label, activeScreen, color)
		self.server = server 
		self.myPlayerName = myPlayerName
		self.myPicker = Picker(self.onHit, activeScreen, self.sphere, label)
		self.sphere.setScale(.04)
		
	def move(self, dx, dy, dz):
		(self.x, self.y, self.z) = (dx + self.x, dy + self.y, dz + self.z) 
		self.sphere.setPos(self.x, self.y, self.z)

	def onHit(self):
		if(base.mouseWatcherNode.hasMouse()):
			ob = self.myPicker.getObjectHit(base.mouseWatcherNode.getMouse()) 
			if(ob!=None):
				selection = ob.getTag("pickable")
				msg = "tryDial %s %s\n"% (self.myPlayerName, selection)
				self.server.send(msg.encode())
				self.mySound.play()