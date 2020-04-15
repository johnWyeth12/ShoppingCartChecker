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
            #reset the actice status for the user so they aren't bombarded with messages
            user['active status'] = 0

def sendMessengerMessage(message, name):
    sent = fbClient.send(Message(text = message), thread_id = name.uid)

def getLastRecievedMessgae(messageThread, user):
    array = []
    for i in messageThread:
        if i.author == user.uid:
            array.append(i.text)
    return array

def setActiveStatus(user, message):
    message = message.lower()
    clientList = Clients.getClientList()
    if message == START_MESSAGE:
        #set status to 1 for user when they specify it
        for i in clientList:
            if(i['name'] == user.name and i['active status'] != 1):
                i['active status'] = 1
                sendMessengerMessage(CHANGED_TO_ACTIVE_MESSAGE, user)
                return
    else:
        #send message explaining what they entered wasn't recognized
        sendMessengerMessage(UNRECOGNIZED_INPUT_MESSAGE, user)

def facebookHeartbeat():
    messagesRecieved = []
    clientList = Clients.getClientList()

    for user in clientList:
        name = fbClient.searchForUsers(user['name'])
        name = name[0]
        totalThread = fbClient.fetchThreadMessages(thread_id = name.uid, limit = 100) #TODO get logic to know how many messages to get per user
        lastMessagesRecieved = getLastRecievedMessgae(totalThread, name)
        if (lastMessagesRecieved != None):
            #see if there are any new messages from clients
            if(len(lastMessagesRecieved) > user['responses']):        
                setActiveStatus(name, lastMessagesRecieved[0])
                user['responses'] = user['responses'] + 1
    
    Clients.updateJSON()

