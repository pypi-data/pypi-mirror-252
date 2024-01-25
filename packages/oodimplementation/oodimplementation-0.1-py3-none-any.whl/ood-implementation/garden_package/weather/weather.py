"""
    This is weather module in the garden package
"""
class Weather:
    def __init__(self, condition):
        self.condition = condition

    def report(self):
        print(f"The weather is {self.condition}.")
