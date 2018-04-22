from panda3d.core import *
def setupScene(displayInstance, render):
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

	# Load the environment model.
	displayInstance.scene = loader.loadModel("models/environment")
	# Reparent the model to render.
	displayInstance.scene.reparentTo(render)
	# Apply scale and position transforms on the model.
	displayInstance.scene.setScale(0.25, 0.25, 0.25)
	displayInstance.scene.setPos(-20, 50, 0)
