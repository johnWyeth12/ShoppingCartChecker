from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, secrets
from fbchat import Client
from fbchat.models import *
from getpass import getpass

WAIT_PERIOD = 60 #1 minute
WAIT_STANDARD = 5

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
    time.sleep(WAIT_STANDARD)
    postalCode_Button = browser.find_element_by_xpath(POSTAL_CODE_START_SHOPPING_XPATH).click()
    time.sleep(WAIT_STANDARD)
    confirmButton = browser.find_element_by_xpath(POSTAL_CODE_CONFIRM_BUTTON_XPATH).click()
    time.sleep(WAIT_STANDARD)

def EnterCredentials():
    usernameField = browser.find_element_by_xpath(USER_EMAIL_FIELD_XPATH)
    usernameField.send_keys(secrets.USER_EMAIL)

    browser.refresh()
    #give user time to enter their password
    time.sleep(WAIT_PERIOD)
    
def CheckDelivery():
    button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, DELIVERY_BUTTON_XPATH)))
    button.click()

    while(1):
        
        try:
            time.sleep(WAIT_PERIOD)
            text = browser.find_element_by_xpath("//*[@id='react-tabs-1']/div/div/div/div/div/div/img")
        except Exception:
            sendFBMessage()

        time.sleep(WAIT_STANDARD)
        browser.refresh()


def sendFBMessage():
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)
    print("Sending WhatsApp Reminder | " + currentTime)
    
    clientList = secrets.getClientList()
    for i in clientList:
        name = fbClient.searchForUsers(i)
        name = name[0]
        sent = fbClient.send(Message(text= "Delivery Time Slot Available! https://delivery.realcanadiansuperstore.ca/"), thread_id=name.uid)


fbClient = Client(secrets.FB_EMAIL, getpass())

browser = webdriver.Chrome("C:/bin/chromedriver.exe")
browser.get(LOGIN_PAGE)
PostalCodeEnter()
EnterCredentials()

#gets to page for checking if there's a delivery option available
CheckDelivery()


