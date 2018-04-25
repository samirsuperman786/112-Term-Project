from pymongo import MongoClient
client = MongoClient()

db = client.userdb

#checks if we have the player in the database
def isTracked(name):
	return db.profiles.find_one({"name":name})!=None

#creates a player profile in the database
def newPlayer(name):
	profile = {"name" : name,
		"friendsList" : [],
		"isOnline" : True}
	db.profiles.insert_one(profile).inserted_id

def setOnlineStatus(name, state):
	db.profiles.update_one({"name":name}, {"$set": {"isOnline": state}})

def getOnlinePlayers():
	online = []
	for profile in db.profiles.find():
		if(profile["isOnline"]):
			online.append(profile["name"])
	return online

#retrieves a players friend list
def getFriends(name):
	try:
		return db.profiles.find_one({"name": name})["friendsList"]
	except:
		return None

#adds a friend to a players friendslist
def addFriend(name, partner):
	oldFriends = getFriends(name)
	oldFriends.append(partner)
	newFriends = list(set(oldFriends))
	db.profiles.update_one({"name":name}, {"$set": {"friendsList": newFriends}})

#removes a freiend from a players friendslist
def removeFriend(name, partner):
	oldFriends = getFriends(name)
	oldFriends.remove(partner)
	db.profiles.update_one({"name":name}, {"$set": {"friendsList": oldFriends}})

def clearProfiles():
	db.profiles.remove()

def setOffline():
	for profile in db.profiles.find():
		db.profiles.update_one(profile, {"$set": {"isOnline": False}})
