import sys, os, json

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
    def __del__(self):
        # save secrets
        pass
    def session(self):
        pass

    def run_seq(self, seq):
        pass

    def exec(self, action):
        pass

def main():
    args = sys.argv[1:]
    automat = Automat()
    if len(args) == 0:
        automat.session()

if __name__ == "__main__":
    main()