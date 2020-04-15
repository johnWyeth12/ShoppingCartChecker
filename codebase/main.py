import TimeSlotChecker, FacebookInterface, Clients

if __name__ == "__main__":
    Clients.init()
    FacebookInterface.initAllClients()
    TimeSlotChecker.openBrowsers()

    #gets to page ready for checking if there's a delivery option available
    TimeSlotChecker.CheckDelivery()
