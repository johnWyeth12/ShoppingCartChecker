import TimeSlotChecker, FacebookInterface

if __name__ == "__main__":
    FacebookInterface.facebookLogin()
    TimeSlotChecker.openBrowsers()

    #gets to page for checking if there's a delivery option available
    TimeSlotChecker.CheckDelivery()