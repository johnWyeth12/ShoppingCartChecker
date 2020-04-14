import json

#[Name, Postal Code, Active?]
Clients = [{'name':"John Wyeth", 'postal code':"L6H5Z7", 'active status':1}]

def init():
    f = open("ClientInfo.json", "w")
    clientData = []
    for i in Clients:
        clientData.append(i)
    
    json.dump(clientData, f, indent = 2)

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
