from typing import List

# class Resource():
#     def __init__(self, name: str):
#         self.name = name

class Action():
    def __init__(self, type:str, timestamp:int, resource:str):
        # type = "R", "W", "C"
        self.type = type
        # no : transaction number (timestamp)
        self.timestamp = timestamp
        # resource : resource name
        self.resource = resource

class Transaction():
    def __init__(self, timestamp: int):
        self.start_time = timestamp
        self.validate_time = 0
        self.finish_time = 0
        self.written_resources = []
        self.read_resources = []
        self.isCommitted = False
    
    def commit(self):
        self.isCommitted = True
    
    def read(self, resource: str):
        self.read_resources.append(resource)

    def write(self, resource: str):
        self.written_resources.append(resource)

class OCC():
    def __init__(self, num_of_transaction : int, action_list: List[Action]):
        self.list_transaction = [Transaction(i) for i in range(1, num_of_transaction + 1)]
        self.action_list = action_list
    
    def validate(self, action):
        # check if the transaction is valid
        # if valid, commit
        # else abort

        #find the transaction
        for transaction in self.list_transaction:
            if action.timestamp == transaction.start_time:
                current_transaction = transaction

        current_transaction.validate_time = current_transaction.start_time
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
        if not valid:
            raise Exception("INVALID TRANSACTION")
        return valid

    def start(self):
        idx = 0
        for action in self.action_list:
            if action.type == "C":
                #find the transaction
                for transaction in self.list_transaction:
                    if action.timestamp == transaction.start_time:
                        current_transaction = transaction
                current_transaction.commit()
                print("Transaction " + str(current_transaction.start_time) + " is committed")
            elif action.type == "R":
                #find the transaction
                for transaction in self.list_transaction:
                    if action.timestamp == transaction.start_time:
                        current_transaction = transaction

                current_transaction.read(action.resource)
                print("Transaction " + str(action.timestamp) + " is read " + action.resource)
            elif action.type == "W":
                if (self.validate(action)):
                    current_transaction.write(action.resource)
                    print("Transaction " + str(action.timestamp) + " is write " + action.resource)

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
        print(action_str)
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
    