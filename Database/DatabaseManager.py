from pymongo import MongoClient
#Assumes you have a running Mongod instance on port 27017
client = MongoClient()

db = client.userdb

def isTracked(name):
	return db.profiles.find_one({"name":name})!=None

def newPlayer(name):
	profile = {"name" : name,
		"friendsList" : []}
	db.profiles.insert_one(profile).inserted_id

def getFriends(name):
	try:
		return db.profiles.find_one({"name": name})["friendsList"]
	except:
		return None

def addFriend(name, partner):
	oldFriends = getFriends(name)
	oldFriends.append(partner)
	newFriends = list(set(oldFriends))
	db.profiles.update_one({"name":name}, {"$set": {"friendsList": newFriends}})

def removeFriend(name, partner):
	oldFriends = getFriends(name)
	oldFriends.remove(partner)
	db.profiles.update_one({"name":name}, {"$set": {"friendsList": oldFriends}})