from typing import List

from lib.resource import Resource
from lib.transaction import Transaction


class Simple():

    def __init__(self, action: List = []):
        self.action = List
        self.queue = []
        self.completed = []
        self.running = []
        self.locks = {}

    def set_action(self, action: List = []):
        self.action = action

    def start(self):
        pass

    def commit(self, transaction: Transaction):
        pass
  
    def write():
        pass

    def read():
        pass
  
    def lock():
        pass
    
    def unlock():
        pass