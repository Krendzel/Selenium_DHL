from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import xml.etree.ElementTree as ET
import sys, os, shutil, pathlib, fnmatch
from string import digits
from termcolor import colored, cprint
from configparser import ConfigParser

CONFIG = ConfigParser()
CONFIG.read("config.ini")
CONFIG_FILE = CONFIG['LOGIN_DATA']

path = "xmls/"
path_out = "xmls_fixed/"
path_out_old = "xmls_fixed/old/"

driver = webdriver.Firefox()

driver.maximize_window()

driver.get("https://dhl24.com.pl/DHL2/shipment.html")
driver.implicitly_wait(10)
time.sleep(2)

# Login
def Login_panel():
    # create a new Firefox session
    
    privacy_btn = driver.find_element_by_id("onetrust-accept-btn-handler")
    privacy_btn.click()
    time.sleep(2)

    login_input = driver.find_element_by_id("LoginForm_username")
    login_input.send_keys(CONFIG_FILE['LOGIN'])

    pass_input = driver.find_element_by_id("LoginForm_password")
    pass_input.send_keys(CONFIG_FILE['PASSWORD'])

    login_btn = driver.find_element_by_id("button-zaloguj")
    login_btn.click()

def fill_address(city, street, number ,refliv):
    
    time.sleep(2)
    postal_code = driver.find_element_by_id("ReceiverForm_postalCode")

    city_input = driver.find_element_by_id("ReceiverForm_city")
    city_input.clear()
    city_input.send_keys(city)
    # print(f"I Find city: {city_input.get_attribute('value')}")

    street_input = driver.find_element_by_id("ReceiverForm_street")
    street_input.clear()
    fixed_street = str.maketrans('','', digits)
    street_input.send_keys(street.strip().translate(fixed_street))
    time.sleep(2)
    street_input.send_keys(Keys.ENTER)
    # print(f"I Find street: {street_input.get_attribute('value')}")

    split_number = number.split("/")
    
    house_input = driver.find_element_by_id("ReceiverForm_number")
    house_input.clear()
    house_input.send_keys(split_number[0])
    time.sleep(5)
    # print(f"I Find number house: {house_input.get_attribute('value')}")
    house_input = driver.find_element_by_id("ReceiverForm_number")
    house_input.send_keys(Keys.ENTER)
    

    # apt_input = driver.find_element_by_id("ReceiverForm_apt")
    # apt_input.send_keys(split_number[1])
    # time.sleep(5)
    postal_code = driver.find_element_by_id("ReceiverForm_postalCode")
    new_postal_code = postal_code.get_attribute('value')
    print(f"New postal code: {'Not Found' if not new_postal_code else new_postal_code}")
    return new_postal_code


def move_old_xml():
    if not os.path.isdir(path_out_old):
        pathlib.Path(path_out_old).mkdir(parents=False, exist_ok=True)
    for file in fnmatch.filter(os.listdir(path_out), "*.xml"):
        shutil.move(os.path.join(path_out, file), os.path.join(path_out_old, file))

# move_old_xml()
Login_panel()
for file in os.listdir(path):
    tree = ET.parse(path+file)
    root = tree.getroot()
    city = root[6]
    street = root[1]
    house = root[2]
    refliv = root[11]
    postal_code_xml = root[5]
    # new_postal_code = "0"

    # print(f'REFLIV: {refliv.text} Street: {street.text}, House: {house.text}, City: {city.text} Postal code: {postal_code.text} New Postal Code: {new_postal_code.text}')
    print('\nStarting Parsing REFLIV: ' + refliv.text)

    test = fill_address(city.text, street.text, house.text, refliv.text)
    
    if not test:
        test = "xx-xxx"
        postal_code_xml.set('updated', 'no')
        tree.write(path_out+"no_x"+file, encoding="UTF-8")
        print(refliv.text + ": File not fixed :(")
    else:
        postal_code_xml.text = test
        postal_code_xml.set('updated', 'yes')
        tree.write(path_out+"x"+file, encoding="UTF-8")
        print(refliv.text + ": File fixed!\n")

    
