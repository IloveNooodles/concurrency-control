from typing import List

# class Resource():
#     def __init__(self, name: str):
#         self.name = name

class Action():
    def __init__(self, type:str, no:int, resource:str):
        # type = "R", "W", "C"
        self.type = type
        # no : transaction number
        self.no = no
        # resource : resource name
        self.resource = resource

class Transaction():
    def __init__(self, no: int):
        # no : transaction number
        self.no = no
        self.start_time = 0
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

    def start(self):
        pass
        
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
    