import json

#[Name, Postal Code, Active?]
Clients = []

def init():
    f = open("ClientInfo.json", "r")
    Clients = json.load(f)

def updateJSON():


def getStatus(client):
    return Clients[client]['active status']

def getClientList():
    return Clients

def getPostalCodes():
    codes = [Clients[0]['postal code']]
    for i in Clients:
        for x in codes:
            if(i[1] != x):
                codes.append(i['postal code'])
    
    return codes
init()
print(Clients)