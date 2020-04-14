import json

FILE_PATH = "../ClientInfo.json"

def init():
    with open(FILE_PATH) as f:
        temp = json.load(f)
    return temp

#[Name, Postal Code, Active?]
Clients = init()

def getStatus(client):
    return client['active status']

def getPostalCode(client):
    return client['postal code']

def getClientList():
    return Clients

def makePostalCodes():
    codes = [Clients[0]['postal code']]
    for i in Clients:
        for x in codes:
            if(i['postal code'] != x):
                codes.append(i['postal code'])
    
    return codes

def updateJSON():
    with open(FILE_PATH, "w") as f:
        json.dump(Clients, f, indent=3)
