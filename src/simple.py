from typing import List, boolea

from lib.resource import Resource
from lib.transaction import Transaction


class Simple():
    def __init__(self, action_list: List = []):
        self.action_list = action_list
        self.running_transaction = None
        self.running_action = None
        self.queue = []
        self.transaction_completed = []
        self.locks = {}
        self.resource = {}
        self.completed_action = []

    def set_action_list(self, action_list: List = []):
        self.action_list = action_list
    
    def get_result(self):
        for action in self.completed_action:
            print(action, end="; ")
    
    def run(self):
        print("====================================================================================")
        print("Starting simple locking protocol")
        for action in self.action_list:
            self.parse(action)
        
        print("====================================================================================")
        print("All transaction have been completed")
        print("Here are the result")
        self.get_result()
        print("====================================================================================")
        

    def validate_transaction(self, action: str, resource: str, transaction_number: int) -> bool:
        # Check if transaction is already commit
        if transaction_number in self.transaction_completed:
            return False
        
        # if the action is commit then must be valid
        if action == 'C':
            return True
        
        locks_key = self.locks.keys()
        locks_value = None
        
        if resource not in locks_key:
            return True
        
        # Check if transaction want to read or write but still have lock
        locks_value = self.locks[resource]

        # if requested transaction holds the lock then ok
        if (action == 'R' or action == 'W') and locks_value == transaction_number:
            return True

        return False

    def commit(self, transaction_number: int):
        is_transaction_valid = self.validate_transaction('C', None, transaction_number)
        pass
  
    def write(self, resource: str, transaction_number: int):
        is_transaction_valid = self.validate_transaction('W', resource, transaction_number)

    def read(self, resource: str, transaction_number: int):
        is_transaction_valid = self.validate_transaction('R', resource, transaction_number)
        to_add = f"R{transaction_number}({resource})"
        if is_transaction_valid:
            self.lock()
            self.resource[resource] = 0
            self.completed_action.append(to_add)
            print(f"{self.running_transaction} is reading resource {resource}")
            return

        transaction_holding_locks = self.locks[resource]
        print(f"Resource {resource} is being locked by T{transaction_holding_locks}")
        print(f"Putting {self.running_action} in the queue")
        self.queue.append(self.running_action)
        # put the transaction in the queue

    def lock(self, resource: str, transaction_number: int):
        self.locks[resource] = transaction_number
        to_add = f"XL{transaction_number}({resource})"
        self.completed_action.append(to_add)
        print(f"{self.running_transaction} is locking resource {resource}")

    def unlock(self, resource: str, transaction_number: int):
        try:
            self.locks.pop(resource)
            to_add = f"UL{transaction_number}({resource})"
            self.completed_action.append(to_add)
            print(f"{self.running_transaction} unlocks resource {resource}")
        except KeyError:
            print("No resource found")
  
    def parse(self, transaction: str):
        trans = transaction[0]
        transaction_number = None
        resource = None
        self.running_action = transaction
        if trans == 'R':
            transaction_number = int(transaction[1])
            resource = transaction[3]
            self.running_transaction = f"T{transaction_number}"
            self.read(resource, transaction_number)
        elif trans == 'W':
            transaction_number = int(transaction[1])
            resource = transaction[3]
            self.running_transaction = f"T{transaction_number}"
            self.write(resource, transaction_number)
        elif trans == 'C':
            transaction_number = int(transaction[1])
            self.running_transaction = f"T{transaction_number}"
            self.commit(transaction, transaction_number)
        else:
            print(f"{transaction} is invalid")
            print("Please input correct test case, program exiting")
            exit(1)
