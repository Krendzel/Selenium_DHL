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

        pass

    def init_app(self):
        cprint("Initializing app...", 'green')
        self.check_dirs()
        pass

    def check_dirs(self):
        if not os.path.exists(self.SRC_PATH):
            cprint("Source directory does not exist, creating...", 'yellow')
            create_dir(self.SRC_PATH)

        if not os.path.exists(self.OUT_PATH):
            cprint(f"Destination directory ({self.OUT_PATH}) does not exist", 'red')
            create_dir(self.OUT_PATH)

        if not os.path.exists(self.OUT_OLD_PATH):
            cprint(f"Destination archive directory ({self.OUT_OLD_PATH}) does not exist", 'red')
            create_dir(self.OUT_OLD_PATH)

        if not os.path.exists(self.ERROR_PATH):
            cprint(f"Destination directory does not exist {self.ERROR_PATH}", 'red')
            create_dir(self.ERROR_PATH)

        else:
            cprint("Checking directories...", 'green')


app = ParseApp()
app.init_app()
