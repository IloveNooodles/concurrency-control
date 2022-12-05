from time import sleep, time
from typing import List


class Simple():
    def __init__(self, action_list: List = []):
        self.action_list = action_list
        self.running_transaction = None
        self.running_action = None
        self.queue = []
        self.transactions_in_queue = {}
        self.transaction_and_schedule = {}
        self.order_transaction = {}
        self.locks = {}
        self.completed_action = []
        self.is_deadlocked_prevention = False

    def set_action_list(self, action_list: List = []):
        self.action_list = action_list

    def get_result(self):
        for action in self.completed_action:
            print(action, end="; ")

    def run(self):
        print("====================================================================================")
        print(">> Starting simple locking protocol")
        choice = input(">> Do you want to activate deadlock prevention? (y/n) ")
        while (not choice in ['y', 'n']):
            print("Please input correct format")
            choice = input(">> Do you want to activate deadlock prevention? (y/n) ")
        
        if choice == 'y':
            self.is_deadlocked_prevention = True
        
        while self.action_list:
            action = self.action_list.pop(0)
            self.parse(action)
        
        # print(self.order_transaction)
        # print(self.transaction_and_schedule)
        # sleep(5)
        while self.queue:
            transaction = self.queue.pop(0)
            self.parse(transaction)

        print("====================================================================================")
        print(">> All transaction have been completed")
        print(">> Here are the schedule: ", end="")
        self.get_result()
        print("\n====================================================================================")
        

    def validate_transaction(self, action: str, resource: str, transaction_number: int) -> bool:
        # Check if transaction is already commit
        
        # if the action is commit then check if the transaction is still running
        if action == 'C':
            # check queue if there are still 
            if self.running_transaction not in self.transactions_in_queue.values():
                return True

            return False
        
        locks_key = self.locks.keys()
        locks_value = None
        
        if not action == 'C' and resource not in locks_key:
            self.lock(resource, transaction_number)
            return True
        
        # Check if transaction want to read or write but still have lock
        locks_value = self.locks[resource]

        # if requested transaction holds the lock then ok
        if (action == 'R' or action == 'W') and locks_value == transaction_number:
            return True

        return False

    def commit(self, transaction_number: int):
        if self.running_transaction not in self.order_transaction.keys():
            self.order_transaction[self.running_transaction] = time()
        is_transaction_valid = self.validate_transaction('C', None, transaction_number)
        if is_transaction_valid:
            # unlocks all the the locks within the same transaction number
            print(f">> {self.running_transaction} commited")
            self.unlock(transaction_number)
            self.completed_action.append(self.running_action)
            self.run_queue()
        else:
            print(f">> Putting {self.running_action} in the queue")
            self.queue.append(self.running_action)
            print(f">> Queue now: {self.queue}")
            if self.running_transaction not in self.transactions_in_queue.keys():
                self.transactions_in_queue[self.running_action] = self.running_transaction

        if self.running_transaction not in self.transaction_and_schedule.keys():
            self.transaction_and_schedule[self.running_transaction] = [self.running_action]
        else:
            if self.running_action not in self.transaction_and_schedule[self.running_transaction]:
                self.transaction_and_schedule[self.running_transaction].append(self.running_action)

    def write(self, resource: str, transaction_number: int):
        if self.running_transaction not in self.order_transaction.keys():
            self.order_transaction[self.running_transaction] = time()
        is_transaction_valid = self.validate_transaction('W', resource, transaction_number)
        if is_transaction_valid:
            self.completed_action.append(self.running_action)
            print(f">> {self.running_transaction} is writing resource {resource}")

        else:
            transaction_holding_locks = f"T{self.locks[resource]}"
            print(f">> Resource {resource} is being locked by {transaction_holding_locks}")
            if self.is_deadlocked_prevention:
                if self.order_transaction[self.running_transaction] < self.order_transaction[transaction_holding_locks]:
                    self.abort(transaction_holding_locks)
                    self.completed_action.append(self.running_action)
                    self.lock(resource, transaction_number)
                    print(f">> {self.running_transaction} is writing resource {resource}")
            else:
                print(f">> Putting {self.running_action} in the queue")
                self.queue.append(self.running_action)
                print(f">> Queue now: {self.queue}")
                if self.running_transaction not in self.transactions_in_queue.keys():
                    self.transactions_in_queue[self.running_action] = self.running_transaction

        if self.running_transaction not in self.transaction_and_schedule.keys():
            self.transaction_and_schedule[self.running_transaction] = [self.running_action]
        else:
            if self.running_action not in self.transaction_and_schedule[self.running_transaction]:
                self.transaction_and_schedule[self.running_transaction].append(self.running_action)

    def read(self, resource: str, transaction_number: int):
        if self.running_transaction not in self.order_transaction.keys():
            self.order_transaction[self.running_transaction] = time()

        is_transaction_valid = self.validate_transaction('R', resource, transaction_number)
        if is_transaction_valid:
            self.completed_action.append(self.running_action)
            print(f">> {self.running_transaction} is reading resource {resource}")
        else:
            transaction_holding_locks = f"T{self.locks[resource]}"
            print(f">> Resource {resource} is being locked by {transaction_holding_locks}")
            print(f">> Putting {self.running_action} in the queue")
            
            if self.is_deadlocked_prevention:
              if self.order_transaction[self.running_transaction] < self.order_transaction[transaction_holding_locks]:
                  self.abort(transaction_holding_locks)
                  self.completed_action.append(self.running_action)
                  self.lock(resource, transaction_number)
                  print(f">> {self.running_transaction} is reading resource {resource}")
            
            else: 
                self.queue.append(self.running_action)
                print(f">> Queue now: {self.queue}")
                if self.running_transaction not in self.transactions_in_queue.keys():
                    self.transactions_in_queue[self.running_action] = self.running_transaction

        if self.running_transaction not in self.transaction_and_schedule.keys():
          self.transaction_and_schedule[self.running_transaction] = [self.running_action]
        else:
            if self.running_action not in self.transaction_and_schedule[self.running_transaction]:
                self.transaction_and_schedule[self.running_transaction].append(self.running_action)

    def abort(self, transaction: str):
        transaction_number = transaction[1]
        action = f"A{transaction_number}"
        self.completed_action.append(action)
        print(f">> Aborting transaction T{transaction_number}")

        self.unlock(transaction_number)
        queue = self.transaction_and_schedule.pop(transaction)
        self.action_list = queue + self.action_list

    def lock(self, resource: str, transaction_number: int):
        self.locks[resource] = transaction_number
        to_add = f"XL{transaction_number}({resource})"
        self.completed_action.append(to_add)
        print(f">> {self.running_transaction} is locking resource {resource}")

    def unlock(self, transaction_number: int):
        try:
            locks_key = self.locks.keys()
            unlocked_locks = [x for x in locks_key if self.locks[x] == int(transaction_number)]
            for lock in unlocked_locks:
                self.locks.pop(lock)
                to_add = f"UL{transaction_number}({lock})"
                self.completed_action.append(to_add)
                print(f">> T{transaction_number} unlocks resource {lock}")
        except KeyError:
            print(">> No resource found")

    def run_queue(self):
        length_queue = len(self.queue)
        
        if length_queue <= 0:
            return 
        print(">> Running schedule in the queue")      
        for i in range(length_queue):
            transaction = self.queue.pop(0)
            self.transactions_in_queue.pop(transaction)
            self.parse(transaction)

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
            self.commit(transaction_number)
        else:
            print(f">> {transaction} is invalid")
            print(">> Please input correct test case, program exiting")
            exit(1)

if __name__ == "__main__":
    # s = Simple(['R5(X)', 'R2(Y)', 'R1(Y)', 'W3(Y)', 'W3(Z)', 'R5(Z)', 'R1(X)', 'R4(W)', 'W3(W)', 'W5(Y)', 'W5(Z)', 'C1', 'C2', 'C3', 'C4', 'C5'])
    s = Simple(['R1(X)', 'R2(Y)', 'R1(Y)', 'C1', 'C2'])
    # s = Simple(['R1(a)', 'R2(b)', 'W1(b)', 'W2(a)', 'C1', 'C2'])
    s.run()
