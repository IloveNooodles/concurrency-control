class Resource():
    def __init__(self, name: str):
        self.value = 0
        self.name = name
    
    def update(self, value: int):
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return f"Name:\t{self.name}\nValue:\t{self.value}"