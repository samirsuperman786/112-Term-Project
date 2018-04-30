from panda3d.core import *
from direct.showbase import DirectObject
import direct.directbase.DirectStart

def createTextAt(x, y, z, label, activeScreen, color = "black", scale =.15):
	(r, g, b) = (0, 0, 0)
	if(color=="red"):
		(r, g, b) = (256, 0, 0)
	text = TextNode(label)
	text.setText(label)
	text.setTextColor(r, g, b, 1)
	
	text.setAlign(TextNode.ACenter)
	textNode = activeScreen.attachNewNode(text)
	textNode.setScale(scale)
	textNode.setPos(x, y, z)