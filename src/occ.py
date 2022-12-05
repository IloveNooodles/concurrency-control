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
        for transaction in self.list_transaction:
            if action.timestamp == transaction.start_time:
                current_transaction = transaction
        # start validate
        for to_be_checked_transaction in self.list_transaction:
            pass
    def start(self):
        idx = 0
        for action in self.action_list:
            if action.type == "C":
                if (idx == 0):
                    self.commit(action.timestamp)
            elif action.type == "R":
                if (idx == 0):
                    self.read(action.timestamp, action.resource)
            elif action.type == "W":
                if (idx == 0):
                    self.write(action.timestamp, action.resource)
                else:
                    self.validate(self, action)
        
if __name__ == "__main__":
    filename = "test/tc1.txt"
    file = open(filename, "r")
    arr = file.read()
    arr = arr.split(";")
    arr = [x.strip() for x in arr]
    action_list = []
    transaction_count = 0
    for action_str in arr:
        print(action_str)
        type = action_str[0]
        no = None
        resource = None
        if (type != "C"):
            no = int(action_str[1])
            if no > transaction_count:
                transaction_count = no
            resource = action_str[3]
        action_list.append(Action(type, no, resource))
    OCC(transaction_count, action_list)
    