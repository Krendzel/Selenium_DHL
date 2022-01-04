import os, sys
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
from termcolor import colored, cprint
from selenium import webdriver
import time


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
        cprint("Initializing app...", 'green')
        try:
            self.check_dirs()
        except KeyboardInterrupt:
            cprint("Exiting...", 'red')

    def check_dirs(self):
        if not os.path.exists(self.SRC_PATH):
            create_dir(self.SRC_PATH)

        if not os.path.exists(self.OUT_PATH):
            create_dir(self.OUT_PATH)

        if not os.path.exists(self.OUT_OLD_PATH):
            create_dir(self.OUT_OLD_PATH)

        if not os.path.exists(self.ERROR_PATH):
            create_dir(self.ERROR_PATH)

        else:
            cprint("Checking directories...", 'green')

    def init_driver(self):
        cprint("Initializing driver...", 'green')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome('C:/web_drivers/chromedriver.exe', options=options)
        driver.get("https://sandbox.dhl24.com.pl/pl/uzytkownik/zaloguj.html", )
        driver.implicitly_wait(1)

        return driver

    def login_panel(self, driver):
        try:
            privacy_btn = driver.find_element_by_class_name("save-preference-btn-handler")
            privacy_btn.click()
        except NoSuchElementException:
            cprint("No privacy button found", 'red')

        # TODO: find better way to find elements
        login_input = driver.find_element_by_css_selector("[id^='LoginForm_'][type='text']")
        login_input.send_keys(self.DHL_LOGIN)

        pass_input = driver.find_element_by_css_selector("[id^='LoginForm_'][type='password']")
        pass_input.send_keys(self.DHL_PASSWORD)

        login_btn = driver.find_element_by_id("button-zaloguj")
        login_btn.click()


app = ParseApp()
chrome = app.init_driver()
app.login_panel(chrome)
