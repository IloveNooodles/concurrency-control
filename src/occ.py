from typing import List
import time
from copy import deepcopy
from src.lib.action import Action
from src.lib.occ_transaction import Transaction

SLEEP_TIME = 0.00000000000001

class OCC():
    """Optimistic Concurrency Control Algorithm"""
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
        """Get the transaction object from the list of transaction by given action object"""
        for transaction in self.list_transaction:
            if action.no == transaction.transaction_no:
                return transaction
    
    def validate(self, action, current_transaction):
        """Validation before commit"""
        valid = True
        conflict_action = Action("-",0,"")
        for to_be_checked_transaction in self.list_transaction:
            if (to_be_checked_transaction.validate_time != 0 
                and to_be_checked_transaction.validate_time < current_transaction.validate_time):
                if (to_be_checked_transaction.finish_time != 0 and 
                 to_be_checked_transaction.finish_time < current_transaction.start_time):
                    continue
                elif (to_be_checked_transaction.finish_time != 0 and 
                      current_transaction.start_time < to_be_checked_transaction.finish_time and
                      to_be_checked_transaction.finish_time < current_transaction.validate_time):
                      for written_resource in to_be_checked_transaction.written_resources:
                        if written_resource in current_transaction.read_resources:
                            valid = False
                            conflict_action = Action("W", to_be_checked_transaction.transaction_no, written_resource)
                            break
                else:
                    valid = False
                    break
        return valid, conflict_action
    
    def print_result(self):
        """Print the result of OCC"""
        for action in self.log:
            if action.type == "A" or action.type == "C":
                print(f"{action.type}{action.no}", end=" ")
            else:
                print(f"{action.type}{action.no}({action.resource})", end=" ")
            

    def run(self):
        idx = 0
        while(idx < len(self.action_list)):
            action = self.action_list[idx]
            current_transaction = self.get_transaction(action)

            # initialize start time
            if (current_transaction.start_time == 0):
                current_transaction.start_time = time.time()

            # if action is commit
            if action.type == "C":
                current_transaction.validate_time = time.time()
                valid, conflict_action = self.validate(action, current_transaction)
                if (valid):
                    current_transaction.commit()
                    current_transaction.finish_time = time.time()
                    time.sleep(SLEEP_TIME)
                    self.log.append(action)                    
                else:
                    # NOT VALID, ROLLBACK
                    print("Transaction " + str(current_transaction.transaction_no) + " is not committed, " + "conflict with " + conflict_action.type  + str(conflict_action.no)  + "(" + conflict_action.resource +")")
                    print("Transaction " + str(current_transaction.transaction_no) + " is aborted")
                    self.log.append(Action("A", current_transaction.transaction_no, ""))
                    current_transaction.start_time = time.time()
                    time.sleep(SLEEP_TIME)
                    temp_action_list = deepcopy(self.action_list[:idx+1])
                    for action in current_transaction.action_log:
                        temp_action_list.append(action)
                    temp_action_list.append(Action("C", current_transaction.transaction_no, ""))
                    rest_action_list = deepcopy(self.action_list[idx+1:])
                    for action in rest_action_list:
                        temp_action_list.append(action)
                    self.action_list = temp_action_list

            # if action is read
            elif action.type == "R":
                current_transaction.read(action)
                time.sleep(SLEEP_TIME)
                self.log.append(action)

            # if action is write
            elif action.type == "W":
                current_transaction.write(action)
                time.sleep(SLEEP_TIME)
                self.log.append(action)
            idx+=1

        print("\nFINAL SCHEDULE:")
        self.print_result()
        print("\n")