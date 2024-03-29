# from lib2to3.pgen2 import driver
import sys, os, json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Automat:
    def __init__(self):
        self.running = False
        if not os.path.exists(".secrets"):
            with open(".secrets", "w") as f:
                self.secrets = {}
        else:
            with open(".secrets") as f:
                self.secrets = json.load(f)
                # print(self.secrets)
        self.driver = None
        self.sequence = []
        self.checkpoint = 0
        self.focus = None
        self.commands = {
            "quit":self.quit,
            "start":self.start,
            "save":self.save,
            "secret":self.secret,
            "goto":self.goto,
            "grab":self.grab,
            "grab_x":self.grab_x,
            "clear":self.clear,
            "text":self.text,
            "text_s":self.text_s,
            "text_i":self.text_i,
            "select":self.select,
            "select_v":self.select_v,
            "select_t":self.select_t,
            "click":self.click,
            "click_x":self.click_x,
            "enter":self.enter,
            "tab":self.tab,
        }
        self.oos={
            "start",
            "save",
            "play",
            "quicksave",
            "restart",
            "reset",
            "secret",
            "quit",}
        with open("secrets.json", "a") as f:
            f.write("")
        with open("secrets.json", "r") as f:
            text = f.read()
            if len(text) > 0:
                self.secrets = json.loads(text)
    def find_element(self, find_by, identifier):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((find_by, identifier))
            )
            return element
        except:
            return None
    def start(self, url):
        self.sequence = self.sequence[self.checkpoint:]
        self.goto(url)
        # if len(self.sequence) == 0:
        #     self.sequence.append(f"goto {url}")
        # self.run_seq(self.sequence)
    def save(self, name):
        with open(f"sequences/{name}.mat", "w") as f:
            f.write("\n".join(self.sequence))
    def secret(self, arg:str):
        idx = arg.find(" ")
        name = arg[:idx]
        val = arg[idx+1:]
        self.secrets[name] = val
    def quit(self):
        self.running = False
        if self.driver != None:
            # quit isn't working God knows why
            self.driver.quit()
    def goto(self, url):
        self.driver.get(url)
    def grab(self, query: str):
        self.focus = self.driver.find_element(by=By.CSS_SELECTOR, value=query)
    def grab_x(self, xpath):
        self.focus = self.driver.find_element(by=By.XPATH, value=xpath)
    def text(self, txt):
        self.focus.clear()
    def text(self, txt):
        self.focus.send_keys(txt)
    def text_s(self, secret):
        self.focus.send_keys(self.secrets[secret])
    def text_i(self, msg):
        txt = input(msg)
        self.focus.send_keys(txt)
    def select(self, idx):
        idx = int(idx)
        sel = Select(self.focus)
        sel.select_by_index(idx)
    def select_v(self, value):
        sel = Select(self.focus)
        sel.select_by_value(value)
    def select_t(self, text):
        sel = Select(self.focus)
        sel.select_by_visible_text(text)
    def click(self, query):
        self.driver.find_element(by=By.CSS_SELECTOR, value=query).click()
    def click_x(self, xpath):
        self.driver.find_element(by=By.XPATH, value=xpath).click()
    def enter(self, _):
        self.focus.send_keys(Keys.ENTER)
    def tab(self, _):
        self.focus.send_keys(Keys.TAB)
    def __del__(self):
        # save secrets
        with open("secrets.json", "w") as f:
            json.dump(self.secrets, f)
        self.quit("")
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
            # o.add_argument("--headless")
            self.driver = webdriver.Firefox(options=o)
        for com in seq:
            self.exec(com)

    def exec(self, action:str):
        command = action.split(" ")
        # arg = ""
        # idx = action.find(" ")
        # if idx != -1:
        #     action = action[:idx]
        #     arg = action[idx+1:]
        # action = action.strip()
        # arg = arg.strip()
        action = command[0]
        arg = command[1] if len(command) > 1 else None 
        print(action, arg)
        if action in self.commands:
            # print(action, arg)
            self.commands[action](arg)
        else:
            print(f"command '{action} not recognized'")
        if action not in self.oos:
            self.sequence.append(command)

def main():
    args = sys.argv[1:]
    automat = Automat()
    if len(args) == 0:
        automat.session()
    else:
        with open(args[0]) as f:
            seq = f.read().splitlines()
            automat.run_seq(seq)

if __name__ == "__main__":
    main()