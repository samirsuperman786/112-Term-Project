#adapted from https://www.panda3d.org/manual/index.php?title=Example_for_Clicking_on_3D_Objects&oldid=3196
from direct.showbase import DirectObject 
#for collision stuff 
from panda3d.core import * 
from Graphics.Word import *

class Picker(DirectObject.DirectObject): 
   def __init__(self, funcToCall, activeScreen): 
      #setup collision stuff 
      self.mySound = base.loader.loadSfx("Graphics/sounds/pop.ogg")
      self.activeScreen = activeScreen
      self.myTraverser = CollisionTraverser()
      self.queue= CollisionHandlerQueue() 

      self.pickerNode=CollisionNode('mouseRay') 
      self.pickerNP=camera.attachNewNode(self.pickerNode) 

      self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask()) 

      self.pickerRay=CollisionRay() 

      self.pickerNode.addSolid(self.pickerRay) 

      self.myTraverser.addCollider(self.pickerNP, self.queue)

      #this holds the object that has been picked 
      self.pickedObj=None 
      self.tag = ""

      self.accept('mouse1', funcToCall) 

   #this function is meant to flag an object as being somthing we can pick 
   def makePickable(self, newObj, val = "True", tagName = "pickable"): 
      newObj.setTag(tagName, val)
      self.val = val
      self.tag = tagName

   #this function finds the closest object to the camera that has been hit by our ray 
   def getObjectHit(self, mpos): #mpos is the position of the mouse on the screen 
      self.pickedObj=None #be sure to reset this 
      self.pickerRay.setFromLens(base.camNode, mpos.getX(),mpos.getY()) 
      self.myTraverser.traverse(self.activeScreen) 
      if self.queue.getNumEntries() > 0: 
         self.queue.sortEntries() 
         self.pickedObj=self.queue.getEntry(0).getIntoNodePath() 

         parent=self.pickedObj.getParent() 
         self.pickedObj=None 

         while parent != self.activeScreen: 
            tag = parent.getTag(self.tag)
            if tag==self.val:
               self.pickedObj=parent
               self.mySound.play()
               return parent 
            else: 
               parent=parent.getParent() 
      return None 

   def getPickedObj(self): 
         return self.pickedObj 