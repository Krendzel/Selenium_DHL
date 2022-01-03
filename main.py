import os, sys
from dotenv import load_dotenv
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


app = ParseApp()

