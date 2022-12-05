from src.lib.action import Action

class Transaction():
    def __init__(self, transaction_no: int):
        self.transaction_no = transaction_no
        self.start_time = 0
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
