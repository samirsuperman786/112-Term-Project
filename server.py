#Code adapted from optional lecture

import socket
import threading
from queue import Queue
from Database.DatabaseManager import *

HOST = "localhost" # put your IP address here if playing on multiple computers
PORT = 50011
BACKLOG = 3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
setOffline()
print("Looking for connections!")

def handleClient(client, serverChannel, cID, clientele):
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8")
      command = msg.split("\n")
      while (len(command) > 1):
        readyMsg = command[0]
        msg = "\n".join(command[1:])
        serverChannel.put(str(cID) + " " + readyMsg)
        command = msg.split("\n")
    except:
      # we failed
      return

def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
    msgList = msg.split(" ")
    senderID = msgList[0]
    instruction = msgList[1]
    details = " ".join(msgList[2:])
    if (details != ""):
      for cID in clientele:
        if cID != senderID:
          sendMsg = instruction + " " + senderID + " " + details + "\n"
          clientele[cID].send(sendMsg.encode())
    serverChannel.task_done()

clientele = dict()
playerNum = 0

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

mics = ["1", "2"]

while True:
  client, address = server.accept()
  # myID is the key to the client in the clientele dictionary
  myID = playerNum
  myMic = mics[playerNum]
  toRemove = []
  for cID in clientele:
    try:
      print (repr(cID), repr(playerNum))
      clientele[cID].send(("newPlayer %s\n" % myID).encode())
      client.send(("newPlayer %s\n" % cID).encode())
    except:
      toRemove.append(cID)
      continue
  for removal in toRemove:
    del clientele[removal]
  clientele[myID] = client
  client.send(("myIDis %s \n" % myID).encode())
  client.send(("myMicIs %s \n" % myMic).encode())
  print("connection recieved from %s" % myID + str(myMic))
  threading.Thread(target = handleClient, args = 
                        (client ,serverChannel, myID, clientele)).start()
  playerNum += 1