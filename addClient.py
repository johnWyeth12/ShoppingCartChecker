import json
FILE_PATH = "ClientInfo.json"

def getCurrentClientList():
    clients = []
    with open(FILE_PATH, "r") as f:
        clients = json.load(f)
    return clients

def loadToFile(name, postalcode, active, responses, initilized, currentList):
    currentList.append({"name": name, "postal code": postalcode, "active status": active, "responses": responses, "initilized": initilized})
    with open(FILE_PATH, "w") as f:
        json.dump(currentList, f, indent=3)
    return True

def getName():
    name = input("Enter facebook name: ")
    return name

def getPostalCode():
    code = input("Enter postal code: ")
    return code

if __name__ == "__main__":
    currentList = getCurrentClientList()
    newName = getName()
    newPostalCode = getPostalCode()

    status = loadToFile(newName, newPostalCode, 0, 0, 0, currentList)
    if status:
        print("Addition successful")
    else:
        print("Addition failed")



