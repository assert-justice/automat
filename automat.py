import sys, os, json, time
# I don't know if this is enough imports, I think we could use a couple more
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Automat:
    def __init__(self):
        self.running = False
        self.secrets = {}
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
    def quit(self, _):
        self.running = False
        if self.driver != None:
            # quit isn't working God knows why
            self.driver.quit()
    def goto(self, url):
        self.driver.get(url)
        if self.find_element(By.CSS_SELECTOR, "html"):
            pass
        else:
            print("url timeout")
    def grab(self, query):
        self.focus = self.find_element(By.CSS_SELECTOR, query)
    def grab_x(self, xpath):
        self.focus = self.find_element(By.XPATH, xpath)
    def clear(self, _):
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
        self.find_element(By.CSS_SELECTOR, query).click()
    def click_x(self, xpath):
        self.find_element(By.XPATH, xpath).click()
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
            #o.add_argument("--headless")
            self.driver = webdriver.Firefox(options=o)
        for action in seq:
            self.exec(action)

    def exec(self, action:str):
        command = action
        arg = ""
        idx = action.find(" ")
        if idx != -1:
            action = command[:idx]
            arg = command[idx+1:]
        action = action.strip()
        arg = arg.strip()
        if action in self.commands:
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