"""
    This is flower module in the garden package
"""
class Flower:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def bloom(self):
        print(f"The {self.color} {self.name} is blooming.")
