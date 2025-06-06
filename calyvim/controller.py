class CalyController:
    def __init__(self):
        self.context = {}

    def assign(self, key, value):
        self.context[key] = value
