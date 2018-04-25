from panda3d.core import *
from direct.task.Task import Task
from direct.showbase import DirectObject
import direct.directbase.DirectStart

#got lighting from optional lecture
def setupScene(render):
	#add one light per face, so each face is nicely illuminated
	plight1 = PointLight('plight')
	plight1.setColor(VBase4(1, 1, 1, 1))
	plight1NodePath = render.attachNewNode(plight1)
	plight1NodePath.setPos(0, 0, 500)
	render.setLight(plight1NodePath)

	plight2 = PointLight('plight')
	plight2.setColor(VBase4(1, 1, 1, 1))
	plight2NodePath = render.attachNewNode(plight2)
	plight2NodePath.setPos(0, 0, -500)
	render.setLight(plight2NodePath)

	plight3 = PointLight('plight')
	plight3.setColor(VBase4(1, 1, 1, 1))
	plight3NodePath = render.attachNewNode(plight3)
	plight3NodePath.setPos(0, -500, 0)
	render.setLight(plight3NodePath)

	plight4 = PointLight('plight')
	plight4.setColor(VBase4(1, 1, 1, 1))
	plight4NodePath = render.attachNewNode(plight4)
	plight4NodePath.setPos(0, 500, 0)
	render.setLight(plight4NodePath)

	plight5 = PointLight('plight')
	plight5.setColor(VBase4(1, 1, 1, 1))
	plight5NodePath = render.attachNewNode(plight5)
	plight5NodePath.setPos(500,0, 0)
	render.setLight(plight5NodePath)

	plight6 = PointLight('plight')
	plight6.setColor(VBase4(1, 1, 1, 1))
	plight6NodePath = render.attachNewNode(plight6)
	plight6NodePath.setPos(-500,0, 0)
	render.setLight(plight6NodePath)


#got landscape from https://free3d.com/3d-model/desert-26147.html
def setupMenuBackground(render):
	scene = loader.loadModel("Graphics/models/landscape.egg")
	scene.reparentTo(render)
	scene.setScale(1)
	scenePos = (3.5, 4, -.3)
	scene.setPos(scenePos)
	# firstLoc = (-.9, 2, .5)
	# secondLoc = (-.9, 2, -.3) 
	# introAnimation(firstLoc)
	# introAnimation(secondLoc)
	return scene

#default background from panda3d
def loadBackground(render):
	scene = loader.loadModel("models/environment")
	scene.reparentTo(render)
	scene.setScale(.25)
	scene.setPos(60, 20, -2)

def loadPrettyLayout(myName, friendName):
		(x,y,z) = (-4, 15, -2)
		space = 8
		createDiamond(x, y, z, myName)
		createDiamond(x+space, y, z, friendName)

        # taskMgr.doMethodLater(1, rotateDiamond,
        #  extraArgs = [diamond1], appendTask = True)

def createDiamond(x,y,z, myName):
	# diamond = loader.loadModel("Graphics/models/icon.egg")
	# diamond.reparentTo(render)
	text = TextNode(myName)
	text.setText(myName)
	text.setTextColor(0, 0, 0, 1)

	# textNode = diamond.attachNewNode(text)
	textNode = render.attachNewNode(text)
	text.setAlign(TextNode.ACenter)
	textNode.setScale(.7)
	textNode.setPos(x,y,z)
	#textNode.setHpr(-90,0,0)
	#diamond.setScale(.5)

	# diamond.setPos(x,y,z)
	# diamond.setHpr(90,0,0)

def rotateDiamond(obj, task):
	(y,p,r) = obj.getHpr()
	obj.setHpr(y,p,r+4)
	return task.again

class introAnimation(object):
	def __init__(self, x, y, z):
		self.star = loader.loadModel("Graphics/models/star.egg")
		self.star.reparentTo(render)
		self.speedX = .01
		self.star.setScale(.05)
		self.bound = x
		self.star.setPos(x,y,z)
		taskMgr.doMethodLater(.005, self.animate, "starAnimation")

	def animate(self, task):
		(x,y,z) = self.star.getPos()
		self.star.setPos(x + self.speedX, y, z)
		if(x> self.bound):
			self.star.setPos(self.bound, y, z)
		return task.again





