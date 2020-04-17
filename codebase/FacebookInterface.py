import secrets, time, Clients, os
from fbchat import Client
from fbchat.models import *
from getpass import getpass

START_MESSAGE = "start"
STOP_MESSAGE = "stop"
WELCOME_MESSAGE = "Welcome! This is an automated message to start off this grocery ordering notification system\nSend me 'start' to begin receiving notifications"
NOTIFY_MESSAGE = "Delivery Time Slot Available! https://delivery.realcanadiansuperstore.ca/ \n\n Notifications have automatically been turned OFF. To receive notifications again, please send me 'start'"
UNRECOGNIZED_INPUT_MESSAGE = "I'm sorry I don't recognize what you typed.\nSend me 'start' to recieve delivery time notifications."
CHANGED_TO_ACTIVE_MESSAGE = "Ok! You'll receive notifications about open delivery times.\nSend me 'stop' to NOT receive notifications anymore."
CHANGED_TO_INACTIVE_MESSAGE = "Ok! You won't receive any notifications about open delivery times anymore.\nSend me 'start' to receive notifications again."

fbClient = Client(secrets.FB_EMAIL, getpass())

def initAllClients():
    clientList = Clients.getClientList()
    for i in clientList:
        if(Clients.getInitilized(i) == 0):
            name = fbClient.searchForUsers(i['name'])[0]
            sendMessengerMessage(WELCOME_MESSAGE, name)
            i['initilized'] = 1

def sendFBNotifications(activatedPostalCode):
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    
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
    messageArray = []
    for i in messageThread:
        if i.author == user.uid:
            messageArray.append(i.text)
    return messageArray

def setActiveStatus(user, message):
    message = message.lower()
    clientList = Clients.getClientList()
    if message == START_MESSAGE:
        #set status to 1 for user when they specify it
        for i in clientList:
            if(Clients.getName(i) == user.name and Clients.getStatus(i) != 1):
                i['active status'] = 1
                sendMessengerMessage(CHANGED_TO_ACTIVE_MESSAGE, user)
                return
    elif message == STOP_MESSAGE:
        #set status to 1 for user when they specify it
        for i in clientList:
            if(Clients.getName(i) == user.name and Clients.getStatus(i) != 0):
                i['active status'] = 0
                sendMessengerMessage(CHANGED_TO_INACTIVE_MESSAGE, user)
                return
    else:
        #send message explaining what they entered wasn't recognized
        sendMessengerMessage(UNRECOGNIZED_INPUT_MESSAGE, user)

def facebookHeartbeat():
    initAllClients()
    clientList = Clients.getClientList()

    for user in clientList:
        name = fbClient.searchForUsers(Clients.getName(user))
        name = name[0]
        totalThread = fbClient.fetchThreadMessages(thread_id = name.uid, limit = 100) #TODO get logic to know how many messages to get per user
        lastMessagesRecieved = getLastRecievedMessgae(totalThread, name)
        if (lastMessagesRecieved != None):
            #see if there are any new messages from clients
            if(len(lastMessagesRecieved) > Clients.getResponses(user)):        
                setActiveStatus(name, lastMessagesRecieved[0])
                user['responses'] = user['responses'] + 1
    
    #Clients.updateClientList()
    Clients.updateJSON()
    os.system('cls')

