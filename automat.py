import sys, os, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

class Automat:
    def __init__(self):
        self.running = False
        if not os.path.exists(".secrets"):
            with open(".secrets", "w") as f:
                self.secrets = {}
        else:
            with open(".secrets") as f:
                self.secrets = json.load(f)
                print(self.secrets)
        self.driver = None
        self.sequence = []
        self.commands = {
            "quit":self.quit
        }
    def quit(self, _):
        self.running = False
    def start(self, url):
        self.driver.get(url)
    def __del__(self):
        # save secrets
        pass
    def session(self):
        self.driver = webdriver.Firefox()
        self.running = True
        print("Automat version 0.1.0 interactive session")
        while self.running:
            action = input()
            self.exec(action)

    def run_seq(self, seq):
        if not self.driver:
            o = Options()
            o.add_argument("--headless")
            self.driver = webdriver.Firefox(options=o)

    def exec(self, action:str):
        arg = ""
        idx = action.find(" ")
        if idx != -1:
            action = action[:idx]
            arg = action[idx+1:]
        if action in self.commands:
            self.commands[action](arg)
        else:
            print(f"command '{action} not recognized'")

def main():
    args = sys.argv[1:]
    automat = Automat()
    if len(args) == 0:
        automat.session()
    else:
        with open(args[1]) as f:
            seq = f.read().splitlines()
            automat.run_seq(seq)

if __name__ == "__main__":
    main()