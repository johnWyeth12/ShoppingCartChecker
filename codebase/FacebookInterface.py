import secrets, time, Clients
from fbchat import Client
from fbchat.models import *
from getpass import getpass

START_MESSAGE = "start"
STOP_MESSAGE = "stop"
NOTIFY_MESSAGE = "Delivery Time Slot Available! https://delivery.realcanadiansuperstore.ca/"
UNRECOGNIZED_INPUT_MESSAGE = "I'm sorry I don't recognize what you typed.\nSend me 'start' to recieve delivery time notifications.\nSend me 'stop' to NOT recieve notifications."
CHANGED_TO_ACTIVE_MESSAGE = "Ok! You'll recieve notifications about open delivery times.\nSend me 'stop' to NOT recieve notifications anymore."
CHANGED_TO_INACTIVE_MESSAGE = "Ok! You won't recieve any notifications about open delivery times anymore.\nSend me 'start' to recieve notifications again."

fbClient = Client(secrets.FB_EMAIL, getpass())

def sendFBNotifications(activatedPostalCode):
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print("Sending Facebook Message | " + currentTime)
    
    clientList = Clients.getClientList()
    for user in clientList:
        #Only send to client if active
        if(Clients.getPostalCode(user) == activatedPostalCode and Clients.getStatus(user)):
            name = fbClient.searchForUsers(user['name'])
            name = name[0]
            sendMessengerMessage(NOTIFY_MESSAGE, name)

def sendMessengerMessage(message, name):
    sent = fbClient.send(Message(text = message), thread_id = name.uid)

def getLastRecievedMessgae(messageThread, user):
    for i in messageThread:
        if i.author == user.uid:
            return i.text

def setActiveStatus(user, message):
    message = message.lower()
    clientList = Clients.getClientList()
    if message == START_MESSAGE:
        #set status to 1 for user
        for i in clientList:
            if(i['name'] == user.name and i['active status'] != 1):
                i[2] = 1
                sendMessengerMessage(CHANGED_TO_ACTIVE_MESSAGE, user)
                return
    elif message == STOP_MESSAGE:
        #set status to 0 for user
        for i in clientList:
            if(i['name'] == user.name and i['active status'] != 0):
                i[2] = 0
                sendMessengerMessage(CHANGED_TO_INACTIVE_MESSAGE, user)
                return
    else:
        #send message explaining what they entered wasn't recognized
        sendMessengerMessage(UNRECOGNIZED_INPUT_MESSAGE, user)

def facebookHeartbeat():
    messagesRecieved = []
    clientList = Clients.getClientList()

    for user in clientList:
        #see if there are any new messages from clients
        name = fbClient.searchForUsers(user['name'])
        name = name[0]
        totalThread = fbClient.fetchThreadMessages(thread_id = name.uid, limit = 10) #TODO get logic to know how many messages to get per user
        lastMessageRecieved = getLastRecievedMessgae(totalThread, name)

        setActiveStatus(name, lastMessageRecieved)
        Clients.updateJSON()

