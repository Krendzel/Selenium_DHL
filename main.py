import fnmatch
import os
import shutil
import sys
import time
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from termcolor import colored, cprint


def create_dir(dir_name):
    while not os.path.exists(dir_name):
        answer = input(colored("Directory {} does not exist. Create it? [y/n]\n".format(dir_name), 'yellow'))
        if answer == 'y':
            os.makedirs(dir_name)
        else:
            cprint("Exiting...", 'red')
            exit()


class ParseApp:
    def __init__(self):
        load_dotenv()
        self.DHL_LOGIN = os.getenv('DHL_LOGIN')
        self.DHL_PASSWORD = os.getenv('DHL_PASSWORD')
        self.SRC_PATH = os.getenv('SRC_PATH')
        self.OUT_PATH = os.getenv('DEST_PATH')
        self.OUT_OLD_PATH = os.getenv('DEST_OLD_PATH')
        self.ERROR_PATH = os.getenv('ERROR_PATH')
        if len(os.listdir(self.SRC_PATH)) == 0:
            cprint("❌ No XML files to process, exiting...", 'red')
            sys.exit()
        cprint("🔥 Initializing app...", 'green')
        try:
            self.check_dirs()
        except KeyboardInterrupt:
            cprint("Exiting...", 'red')

    def check_dirs(self):
        cprint("🔥 Checking directories...", 'green')
        if not os.path.exists(self.SRC_PATH):
            create_dir(self.SRC_PATH)

        if not os.path.exists(self.OUT_PATH):
            create_dir(self.OUT_PATH)

        if not os.path.exists(self.OUT_OLD_PATH):
            create_dir(self.OUT_OLD_PATH)

        if not os.path.exists(self.ERROR_PATH):
            create_dir(self.ERROR_PATH)

    def archive_processed_files(self):
        counter = 0
        for file in fnmatch.filter(os.listdir(self.OUT_PATH), "*.*"):
            counter += 1
            shutil.move(self.OUT_PATH + file, self.OUT_OLD_PATH + file)
        cprint(f"🔥 Archived {counter} files", 'yellow')

    def init_driver(self):
        cprint("🔥 Initializing driver...", 'green')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('C:/web_drivers/chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://dhl24.com.pl/pl/DHL2/shipment.html", )
        driver.implicitly_wait(1)

        return driver

    def login_process(self, driver):
        cprint("🔥 Logging in...", 'green')
        try:
            privacy_btn = driver.find_element(By.CLASS_NAME, "save-preference-btn-handler")
            privacy_btn.click()
        except NoSuchElementException:
            cprint("❌ No privacy button found", 'red')
            chrome.quit()

        # TODO: find better way to find elements
        login_input = driver.find_element(By.CSS_SELECTOR, "[id^='LoginForm_'][type='text']")
        login_input.send_keys(self.DHL_LOGIN)

        pass_input = driver.find_element(By.CSS_SELECTOR, "[id^='LoginForm_'][type='password']")
        pass_input.send_keys(self.DHL_PASSWORD)

        login_btn = driver.find_element(By.ID, "button-zaloguj")
        login_btn.click()

        try:
            error_msg = driver.find_element(By.CLASS_NAME, "errorSummary")
            cprint(f"❌ {error_msg.text}", 'red')
            driver.quit()
            sys.exit()
        except NoSuchElementException:
            cprint("✅ Login successful", 'green')

    def fill_address(self, driver, city_input, street_input):
        city = driver.find_element(By.ID,"ReceiverForm_city")
        city.clear()
        city.send_keys(city_input)

        street = driver.find_element(By.ID, "ReceiverForm_street")
        street.clear()
        street.send_keys(street_input)

    def process_xml(self, driver, dir_name):

        cprint("🔥 Reading XML files...", 'green')
        for file in os.listdir(dir_name):
            xml = ET.parse(dir_name + '/' + file)
            root = xml.getroot()
            order_id = root.find('SHIPMENT_REF_1').text
            city = root.find('RECIPIENT_CITY').text
            street = root.find('RECIPIENT_ADDRESS_1').text
            postal_code_old = root.find('RECIPIENT_POSTAL_CODE')
            print(f"Checking {order_id}")
            app.fill_address(chrome, city, street)
            time.sleep(2)  # need to be adjusted to avoid blank input value
            postal_code = driver.find_element(By.ID, "ReceiverForm_postalCode").get_property('value')
            print(f"{postal_code_old.text} -> {postal_code}")
            postal_code_old.text = postal_code
            xml.write(self.OUT_PATH + file, encoding="UTF-8")
            cprint(f"✅ {order_id} processed and moved to {self.OUT_PATH}", 'green')
            shutil.move(self.SRC_PATH + file, self.OUT_PATH + file)


app = ParseApp()
chrome = app.init_driver()
app.login_process(chrome)
app.process_xml(chrome, app.SRC_PATH)
chrome.quit()
