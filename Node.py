

class Node:

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value
    
    def setValue(self, newvalue):
        self.value = newvalue

    def __repr__(self): 
        return str(self.value)