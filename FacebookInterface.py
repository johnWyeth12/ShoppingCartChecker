import secrets, time, Clients
from fbchat import Client
from fbchat.models import *
from getpass import getpass

def facebookLogin():
    fbClient = Client(secrets.FB_EMAIL, getpass())

def sendFBMessage():
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print("Sending Facebook Message | " + currentTime)
    
    clientList = secrets.getClientList()
    for i in clientList:
        #Only send to client if active
        if(Clients.getStatus(i)):
            name = fbClient.searchForUsers(i)
            name = name[0]
            sent = fbClient.send(Message(text= "Delivery Time Slot Available! https://delivery.realcanadiansuperstore.ca/"), thread_id=name.uid)

def facebookHeartbeat():
    #check for messages to disable/enable clients
    x = 0 #placeholder

