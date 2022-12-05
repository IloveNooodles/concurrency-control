from typing import List
import time
from copy import deepcopy
# class Resource():
#     def __init__(self, name: str):
#         self.name = name

SLEEP_TIME = 0.00000000000001

class Action():
    def __init__(self, type:str, no:int, resource:str):
        # type = "R", "W", "C"
        self.type = type
        # no : transaction number (no)
        self.no = no
        # resource : resource name
        self.resource = resource

class Transaction():
    def __init__(self, no: int):
        self.transaction_no = no
        self.start_time = no
        self.validate_time = 0
        self.finish_time = 0
        self.written_resources = []
        self.read_resources = []
        self.isCommitted = False
        self.action_log = []
    
    def commit(self):
        self.isCommitted = True
    
    def read(self, action: Action):
        self.read_resources.append(action.resource)
        self.action_log.append(action)

    def write(self, action: Action):
        self.written_resources.append(action.resource)
        self.action_log.append(action)

class OCC():
    def __init__(self, num_of_transaction : int, action_list: List[Action]):
        self.list_transaction = [Transaction(i) for i in range(1, num_of_transaction + 1)]
        self.action_list = action_list
        self.log = []
    
    def validate(self, action, current_transaction):
        # check if the transaction is valid
        # if valid, commit
        # else abort

        # start validate
        valid = True
        for to_be_checked_transaction in self.list_transaction:
            if (to_be_checked_transaction.validate_time != 0 
                and to_be_checked_transaction.validate_time < current_transaction.validate_time):
                if to_be_checked_transaction.finish_time < current_transaction.finish_time:
                    continue
                elif (current_transaction.start_time < to_be_checked_transaction.finish_time and
                      to_be_checked_transaction.finish_time < current_transaction.validate_time):
                      for written_resource in to_be_checked_transaction.written_resources:
                        if written_resource in current_transaction.read_resources:
                            valid = False
                            break

        return valid

    def start(self):
        idx = 0
        while(idx < len(self.action_list)):
            #find the transaction
            action = self.action_list[idx]
            # print("action list len=",len(self.action_list))
            # print(action.no, action.resource)
            for transaction in self.list_transaction:
                if action.no == transaction.transaction_no:
                    current_transaction = transaction
            #start time
            if (current_transaction.start_time == 0):
                current_transaction.start_time = time.time()

            if action.type == "C":
                current_transaction.validate_time = time.time()
                if (self.validate(action, current_transaction)):
                    current_transaction.commit()
                    current_transaction.finish_time = time.time()
                    print("Transaction " + str(current_transaction.transaction_no) + " is committed")
                    time.sleep(SLEEP_TIME)
                    self.log.append(action)                    
                else:
                    #rollback
                    time.sleep(SLEEP_TIME)
                    print("Transaction " + str(current_transaction.start_time) + " is not committed, aborting")
                    current_transaction.start_time = time.time()
                    temp_action_list = deepcopy(self.action_list[:idx+1])
                    # print("len ca =",len(current_transaction.action_log))
                    for action in current_transaction.action_log:
                        temp_action_list.append(action)
                    temp_action_list.append(Action("C", current_transaction.transaction_no, ""))
                    rest_action_list = deepcopy(self.action_list[idx+1:])
                    # print("len ral =",len(rest_action_list))
                    for action in rest_action_list:
                        temp_action_list.append(action)
                    self.action_list = temp_action_list

            elif action.type == "R":
                #find the transaction
                current_transaction.read(action)
                print("Transaction " + str(current_transaction.transaction_no) + " is read " + action.resource)
                time.sleep(SLEEP_TIME)
                self.log.append(action)
            elif action.type == "W":
                current_transaction.write(action)
                print("Transaction " + str(current_transaction.transaction_no) + " is write " + action.resource)
                time.sleep(SLEEP_TIME)
                self.log.append(action)
            idx+=1
        
if __name__ == "__main__":
    filename = "test/tc2.txt"
    file = open(filename, "r")
    arr = file.read()
    arr = arr.split(";")
    arr = [x.strip() for x in arr]
    action_list = []
    transaction_count = 0
    for action_str in arr:
        # print(action_str)
        type = action_str[0]
        no = int(action_str[1])
        if no > transaction_count:
            transaction_count = no
        resource = None
        if (type != "C"):
            resource = action_str[3]
        action_list.append(Action(type, no, resource))

    print("------PROGRAM START------")
    occ = OCC(transaction_count, action_list)
    occ.start()
    