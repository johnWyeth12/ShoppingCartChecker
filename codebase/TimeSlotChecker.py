from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import secrets, FacebookInterface, time, Clients

WAIT_PERIOD = 60 #1 minute
WAIT_STANDARD = 5

LOGIN_PAGE = "https://delivery.realcanadiansuperstore.ca/"
POSTAL_CODES = Clients.makePostalCodes()
print(POSTAL_CODES)
BROWSERS = [None] * len(POSTAL_CODES)
ROTATIONS = len(BROWSERS)

POSTAL_CODE_XPATH = "//*[@id='signup-zipcode']"
POSTAL_CODE_START_SHOPPING_XPATH = "//*[@id='signup-widget']/div/div[1]/form/button"
POSTAL_CODE_CONFIRM_BUTTON_XPATH = "//*[@id='signup-widget']/div/div[1]/form/a"

USER_EMAIL_FIELD_XPATH = "//*[@id='email']"
USER_PASS_FIELD_XPATH = "//*[@id='password']"
SIGN_IN_XPATH = "//*[@id='login']/fieldset/button"

DELIVERY_BUTTON_XPATH = "//*[@id='header']/div/div/div[4]/div[2]/div[2]/span/a"

def PostalCodeEnter():
    for i in range(ROTATIONS):
        BROWSERS[i] = webdriver.Chrome("C:/bin/chromedriver.exe")
        BROWSERS[i].get(LOGIN_PAGE)

        postalCode_Element = BROWSERS[i].find_element_by_xpath(POSTAL_CODE_XPATH)
        postalCode_Element.send_keys(POSTAL_CODES[i])
        time.sleep(WAIT_STANDARD)

        postalCode_Button = BROWSERS[i].find_element_by_xpath(POSTAL_CODE_START_SHOPPING_XPATH).click()
        time.sleep(WAIT_STANDARD)

        confirmButton = BROWSERS[i].find_element_by_xpath(POSTAL_CODE_CONFIRM_BUTTON_XPATH).click()
        time.sleep(WAIT_STANDARD)

def EnterCredentials():
    for i in range(ROTATIONS):
        usernameField = BROWSERS[i].find_element_by_xpath(USER_EMAIL_FIELD_XPATH)
        usernameField.send_keys(secrets.USER_EMAIL)

        BROWSERS[i].refresh()
        #give user time to enter their password
        input("Press Enter... "+ str(i + 1))
        time.sleep(WAIT_STANDARD)
    
def CheckDelivery():
    for i in range(ROTATIONS):
        button = WebDriverWait(BROWSERS[i], 20).until(EC.element_to_be_clickable((By.XPATH, DELIVERY_BUTTON_XPATH)))
        button.click()
        time.sleep(WAIT_STANDARD)

    #The program remains in here
    while(1):
        time.sleep(WAIT_PERIOD)
        FacebookInterface.facebookHeartbeat()
        for i in range(ROTATIONS):
            try:
                text = BROWSERS[i].find_element_by_xpath("//*[@id='react-tabs-1']/div/div/div/div/div/div/img")
            except Exception:
                FacebookInterface.sendFBNotifications(POSTAL_CODES[i])

        time.sleep(WAIT_STANDARD)
        for i in range(ROTATIONS):
            BROWSERS[i].refresh()

def openBrowsers():
    PostalCodeEnter()
    EnterCredentials()


