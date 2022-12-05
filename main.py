import argparse

from src.occ import OCC
from src.simple import Simple


class Main():
    def __init__(self):
        parser = argparse.ArgumentParser(
          description="Concurrency Control Protocol Implementation"
        )

        parser.add_argument(
            "concurrency_control",
            choices=["simple", "optimistic"],
            help="choose concurrency control protocol, s[imple] for simple and o[ptimistic] for optimistic",
        )

        parser.add_argument(
            "schedule_input",
            metavar="[pathfile]",
            type=str,
            help="path file for the testcase or input",
        )

        args = parser.parse_args()
        self.options = getattr(args, "concurrency_control")
        self.filepath = getattr(args, "schedule_input")
        self.schedule = None
    
    def read_files(self):
        try:
            file = open(self.filepath, "r")
            arr = file.read()
            arr = arr.split(";")
            arr = [x.strip() for x in arr]
            self.schedule = arr
        except:
            print("File not found, exiting...")
            exit(1)
    
    def start(self):
        self.read_files()
        protocol = None
        if self.options == 'simple':
            protocol = Simple(self.schedule)
            protocol.run()
        elif self.options == 'optimistic':
            pass
          


if __name__ == "__main__":
    main = Main()
    main.start()