from typing import List
import time
from copy import deepcopy
from src.lib.action import Action
from src.lib.occ_transaction import Transaction

SLEEP_TIME = 0.00000000000001

class OCC():
    def __init__(self, arr: List[str]):
        self.action_list = []
        num_of_transaction = 0
        for action_str in arr:
            type = action_str[0]
            no = int(action_str[1])
            if no > num_of_transaction:
                num_of_transaction = no
            resource = None
            if (type != "C"):
                resource = action_str[3]
            self.action_list.append(Action(type, no, resource))
        self.list_transaction = [Transaction(i) for i in range(1, num_of_transaction + 1)]
        self.log = []
    
    def get_transaction(self, action: Action):
        for transaction in self.list_transaction:
            if action.no == transaction.transaction_no:
                return transaction
    
    def validate(self, action, current_transaction):
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

    def run(self):
        idx = 0
        while(idx < len(self.action_list)):
            #find the transaction
            action = self.action_list[idx]
            current_transaction = self.get_transaction(action)

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
                    print("Transaction " + str(current_transaction.transaction_no) + " is not committed, aborting")
                    current_transaction.start_time = time.time()
                    temp_action_list = deepcopy(self.action_list[:idx+1])
                    for action in current_transaction.action_log:
                        temp_action_list.append(action)
                    temp_action_list.append(Action("C", current_transaction.transaction_no, ""))
                    rest_action_list = deepcopy(self.action_list[idx+1:])
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