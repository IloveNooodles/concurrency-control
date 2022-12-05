from typing import List

from lib.resource import Resource
from lib.transaction import Transaction


class Simple():

    def __init__(self, action: List = []):
        self.action = action
        self.queue = []
        self.completed = []
        self.running = []
        self.locks = {}
        self.resource = {}

    def set_action(self, action: List = []):
        self.action = action

    def start(self):
        pass

    def commit(self, transaction: str):
        pass
  
    def write(self):
        pass

    def read(self):
        pass
  
    def lock(self):
        pass
    
    def unlock(self):
        pass
    
    def parse(self, transaction: str):
        trans = transaction[0]
        trans_number = None
        resource = None
        if trans == 'R':
            trans_number = transaction[1]
            resource = transaction[3]
            self.read(resource, trans_number)
        elif trans == 'W':
            trans_number = transaction[1]
            resource = transaction[3]
            self.write(resource, trans_number)
        elif trans == 'C':
            trans_number = transaction[1]
            self.commit(transaction, trans_number)
        else:
            print(f"{transaction} is invalid")
            print("Please input correct test case, program exiting")
