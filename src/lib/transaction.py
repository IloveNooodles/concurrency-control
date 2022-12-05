class Transaction():
    def __init__(self, name: str):
        self.name = name
        self.resource = []
    
    def __str__(self):
        print(f"Transaction:\t{self.transaction}")