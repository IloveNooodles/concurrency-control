class Action():
    def __init__(self, type:str, no:int, resource:str):
        # type = "R", "W", "C"
        self.type = type
        # no : transaction number (no)
        self.no = no
        # resource : resource name
        self.resource = resource