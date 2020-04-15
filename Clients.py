import json

FILE_PATH = "../ClientInfo.json"

def init():
    with open(FILE_PATH) as f:
        temp = json.load(f)
    return temp

#[Name, Postal Code, Active?]
Clients = init()

def updateJSON():
    with open(FILE_PATH, "w") as f:
        json.dump(Clients, f, indent=3)

def getStatus(client):
    return Clients[client]['active status']

def getClientList():
    return Clients

def makePostalCodes():
    allCodes = []
    for i in Clients:
        allCodes.append(i['postal code'])
    codes = list(dict.fromkeys(allCodes))
    return codes

