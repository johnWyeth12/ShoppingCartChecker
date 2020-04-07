from selenium import webdriver
import time, secrets

WAIT_PERIOD = 120 #2 minutes

LOGIN_PAGE = "https://delivery.realcanadiansuperstore.ca/"
POSTAL_CODE = "L6H5Z7"

POSTAL_CODE_XPATH = "//*[@id='signup-zipcode']"
POSTAL_CODE_START_SHOPPING_XPATH = "//*[@id='signup-widget']/div/div[1]/form/button"
POSTAL_CODE_CONFIRM_BUTTON_XPATH = "//*[@id='signup-widget']/div/div[1]/form/a"

USER_EMAIL_FIELD_XPATH = "//*[@id='email']"
USER_PASS_FIELD_XPATH = "//*[@id='password']"
SIGN_IN_XPATH = "//*[@id='login']/fieldset/button"

DELIVERY_BUTTON_XPATH = "//*[@id='header']/div/div/div[4]/div[2]/div[2]/span/a"

def PostalCodeEnter():
    postalCode_Element = browser.find_element_by_xpath(POSTAL_CODE_XPATH)
    postalCode_Element.send_keys(POSTAL_CODE)
    time.sleep(2)
    postalCode_Button = browser.find_element_by_xpath(POSTAL_CODE_START_SHOPPING_XPATH).click()
    time.sleep(5)
    confirmButton = browser.find_element_by_xpath(POSTAL_CODE_CONFIRM_BUTTON_XPATH).click()
    time.sleep(2)

def EnterCredentials():
    usernameField = browser.find_element_by_xpath(USER_EMAIL_FIELD_XPATH)
    usernameField.send_keys(secrets.USER_EMAIL)

    browser.refresh()
    #give user time to enter their password
    time.sleep(60)
    
def CheckDelivery():
    button = browser.find_element_by_xpath(DELIVERY_BUTTON_XPATH).click()
    
    while(1):
        time.sleep(WAIT_PERIOD)
        try:
            text = browser.find_element_by_xpath("//*[@id='react-tabs-3']/div/div/div/div/div/div/h1").text
            if(text != "No delivery times available"):
                sendWhatsAppMessage()
        except:
            sendWhatsAppMessage()


def sendWhatsAppMessage():
    print("Sending WhatsApp Reminder")


browser = webdriver.Chrome("C:/bin/chromedriver.exe")
browser.get(LOGIN_PAGE)
PostalCodeEnter()
EnterCredentials()

#gets to page for checking if there's a delivery option available
CheckDelivery()


