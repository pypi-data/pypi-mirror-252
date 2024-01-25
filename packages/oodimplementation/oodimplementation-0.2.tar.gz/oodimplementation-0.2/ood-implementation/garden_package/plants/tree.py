"""
    This is tree module in the garden package
"""
class Tree:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def grow(self):
        print(f"The {self.name} tree is growing to a height of {self.height} meters.")
