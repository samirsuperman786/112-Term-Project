#Code adapted from optional lecture

from pymongo import MongoClient
#Assumes you have a running Mongod instance on port 27017
client = MongoClient()

db = client.userdb

#checks if we have the player in the database
def isTracked(name):
	return db.profiles.find_one({"name":name})!=None

#creates a player profile in the database
def newPlayer(name):
	profile = {"name" : name,
		"friendsList" : []}
	db.profiles.insert_one(profile).inserted_id

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
