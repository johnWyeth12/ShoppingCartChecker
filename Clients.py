#[Name, Postal Code, Active?]
Clients = [["John Wyeth", "L6H5Z7", 1], 
           ["Lynn Wyeth (Rossouw)", "L6H5Z7", 1]]

def getStatus(client):
    return Clients[client][2]

def getClientList():
    return Clients

def getPostalCodes():
    codes = [Clients[0][1]]
    for i in Clients:
        for x in codes:
            if(i[1] != x):
                codes.append(i[1])
    
    return codes
