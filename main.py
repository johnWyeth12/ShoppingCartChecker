import TimeSlotChecker, FacebookInterface

if __name__ == "__main__":
    Clients.init()
    FacebookInterface.facebookLogin()
    TimeSlotChecker.openBrowsers()

    #gets to page ready for checking if there's a delivery option available
    TimeSlotChecker.CheckDelivery()