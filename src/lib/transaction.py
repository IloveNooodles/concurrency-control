from lib.resource import Resource


class Transaction():
    def __init__(self, name: str):
        self.name = name
        self.resource = []
        self.action = []

    def add_resource(self, resource: Resource):
        self.resource.append(resource)

    def add_action(self, action):
        pass
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        return f"Transaction:\t{self.transaction}"