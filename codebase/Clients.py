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

def getName(client):
    return client['name']

def getResponses(client):
    return client['responses']

def getInitilized(client):
    return client['initilized']

def getClientList():
    return Clients

def makePostalCodes():
    allCodes = []
    for i in Clients:
        allCodes.append(i['postal code'])
    codes = list(dict.fromkeys(allCodes))
    return codes

def updateJSON():
    fileError = False

    while(not fileError):
        try:
            with open(FILE_PATH, "w") as f:
                json.dump(Clients, f, indent=3)
            #If program gets here, there was no issue with updating the client file
            fileError = True
        except Exception:
            print("error when updating JSON file")
            #do nothing - keeps loop going

def updateClientList():
    with open(FILE_PATH, "r") as f:
        Clients = json.load(f)
