from typing import List, boolea

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

    def valid_transaction(self, action: str, resource: str, transaction_number: int) -> bool:
        # Check if transaction is already commit
        if transaction_number in self.completed:
            return False
        
        # Check if transaction want to read or write but still have lock
        locks_key = self.locks.keys()
        locks_value = None
        
        if resource in locks_key:
            locks_value = self.locks[resource]
        
        # if requested transaction holds the lock then ok
        if (action == 'C' or action == 'R') and locks_value == transaction_number:
            return True
        
        return False

    def commit(self, transaction: str):
        pass
  
    def write(self):
        pass

    def read(self, resource: str, transaction_number: int):
        pass
  
    def lock(self):
        pass
    
    def unlock(self):
        pass
    
    def parse(self, transaction: str):
        trans = transaction[0]
        transaction_number = None
        resource = None
        if trans == 'R':
            transaction_number = transaction[1]
            resource = transaction[3]
            self.read(resource, transaction_number)
        elif trans == 'W':
            transaction_number = transaction[1]
            resource = transaction[3]
            self.write(resource, transaction_number)
        elif trans == 'C':
            transaction_number = transaction[1]
            self.commit(transaction, transaction_number)
        else:
            print(f"{transaction} is invalid")
            print("Please input correct test case, program exiting")
            exit(1)
