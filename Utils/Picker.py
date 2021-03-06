#adapted from https://www.panda3d.org/manual/index.php?title=Example_for_Clicking_on_3D_Objects&oldid=3196
from direct.showbase import DirectObject 
#for collision stuff 
from panda3d.core import * 
from Graphics.Word import *

class Picker(DirectObject.DirectObject): 
   def __init__(self, funcToCall, activeScreen, newObj, val = "True", tagName = "pickable"): 
      #setup collision stuff 
      self.activeScreen = activeScreen
      self.myTraverser = CollisionTraverser()
      self.queue= CollisionHandlerQueue() 

      self.pickerNode=CollisionNode('mouseRay') 
      self.pickerNP=camera.attachNewNode(self.pickerNode) 

      self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask()) 

      self.pickerRay=CollisionRay() 

      self.pickerNode.addSolid(self.pickerRay) 

      self.myTraverser.addCollider(self.pickerNP, self.queue)

      self.pickedObj=None 

      self.newObj = newObj
      self.newObj.setTag(tagName, val)
      self.val = val
      self.tag = tagName
      self.accept('mouse1', funcToCall) 

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
               return parent 
            else: 
               parent=parent.getParent() 
      return None 

   def getPickedObj(self): 
      return self.pickedObj 

   def destroy(self):
      self.ignoreAll()
      self.pickerNP.remove_node()
      self.myTraverser.clearColliders()
      self.newObj.removeNode()
      if(self.pickedObj!=None):
         self.pickedObj.removeNode()  
      
