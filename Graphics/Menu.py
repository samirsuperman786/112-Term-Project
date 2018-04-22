import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *
from Database.DatabaseManager import *

enteredText = ""

#callback function to set  text 
def checkUserName():
	if(isTracked(enteredText)):
		playerName = enteredText
		friends = getFriends(playerName)
		loadFriendsMenu(playerName, friends)
	else:
		newPlayer(playerName)
		loadFriendsMenu(playerName, [])
 
#clear the text
def clearText():
	entry.enterText('')
 
def layout():
	entry = DirectEntry(text = "", scale=.2, command=checkUserName,
	initialText="", numLines = 2, focus=1,
	 frameSize = (0,0,0, 0))
	entry.setPos(-1,0,.3)

def loadFriendsMenu(playerName, friends):
	dialFriend(playerName, "bob")

def dialFriend(playerName, friend):
	game = Display()
	serverMsg = Queue(100)
	threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
	base.disableMouse()
	createGravity()
	base.run()