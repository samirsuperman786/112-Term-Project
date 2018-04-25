from panda3d.core import *
from direct.task.Task import Task
from direct.showbase import DirectObject
import direct.directbase.DirectStart

#got landscape from https://free3d.com/3d-model/desert-26147.html
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

	scene = loader.loadModel("Graphics/models/landscape.egg")
	scene.reparentTo(render)
	scene.setScale(1)
	scene.setPos(3.5, 4, -.3)

def loadBackground(displayInstance):
	# # Load the environment model.
	displayInstance.scene = loader.loadModel("models/environment")
	# Reparent the model to render.
	displayInstance.scene.reparentTo(render)
	# Apply scale and position transforms on the model.
	displayInstance.scene.setScale(1, 1, 1)
	displayInstance.scene.setPos(50, 50, -2)

	# displayInstance.ocean = loader.loadModel("Graphics/models/ocean.egg")
	# displayInstance.ocean.reparentTo(render)
	# displayInstance.ocean.setPos(0, 30, -2)
	#displayInstance.ocean.setScale(.5)

def loadPrettyLayout(myName, friendName):
		(x,y,z) = (-4, 15, -2)
		createDiamond(x, y, z, myName)
		createDiamond(x+8, y, z, friendName)

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



