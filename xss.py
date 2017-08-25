import requests
import mechanize
import sys
from selenium import webdriver
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
import requests
from selenium.webdriver.chrome.options import Options


def getForms():
    url = sys.argv[1:]
    url = url[0]
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, "html.parser") 
    #soup = BeautifulSoup(requests.get(url).content)
    print "INPUT NAMES: "
    for name in soup.find_all('input'):
        print name.get('name')

    print "SUBMIT INPUT: "
    submitInput = soup.find_all('input', attrs={'type':re.compile("submit")})
    print submitInput
    if submitInput == []:
        print req.text
    onInput()


def findXss():
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                'Timed out waiting for PA creation ' +
                                'confirmation popup to appear.')
        alert = driver.switch_to_alert
        alert.accept()
        print "XSS Found:" + line
    except TimeoutException:
        print "No XSS " + line
        driver.quit()
        pass


def onInput():
    url = sys.argv[1:]
    url = url[0]
    inputName = raw_input("Select an input @name to write: ")
    inputValue = raw_input("Select a submit input @value: ")
    lst = open("xxsfilterbypass.lst", "r")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-xss-auditor')
    driver = webdriver.Chrome(desired_capabilities=options.to_capabilities())
    for line in lst:    
        try:
            driver.get(url)
            field = driver.find_element_by_name(inputName)
            submit = driver.find_element_by_xpath("//input[@value='"+ inputValue +"'][@type='submit']")
            field.send_keys(line)
            field.send_keys(Keys.RETURN)
            submit.click()
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')
                alert = driver.switch_to_alert()
                #alert.accept()
                print "XSS Found:" + line

            except TimeoutException:
                print "No XSS " + line
                pass
        except StaleElementReferenceException as e:
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')
                print "XSS Found: " + line
                break
            except TimeoutException:
                print "No XSS: " + line
                pass
        except UnexpectedAlertPresentException:
            print "XSS Found: " + line
            break
                
    print "This web is vulnerable to XSS"


def onUrl():
    lst = open("xxsfilterbypass.lst", "r")
    url = sys.argv[1:]
    url = url[0]
    driver = webdriver.Chrome()
    # chromedriver https://chromedriver.storage.googleapis.com/index.html?path=2.31/
    for line in lst:
        driver.get(url+line)
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')
            alert = driver.switch_to_alert()
            alert.Dismiss()
            print "XSS Found:"
            print line

        except TimeoutException:
            print "No XSS " + line
            pass


def main():
    if len (sys.argv) != 2:
        print "Enter the URL: python xss.py URL"
        sys.exit(1)
    
    selection = raw_input("On input[i] or on url[u]: " )
    if selection == "i":
        getForms()
    elif selection == "u":
        onUrl()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()