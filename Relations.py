
class Relation:

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def getRelationName(self): return self.name

    def setRelationName(self, newname): self.name = newname

    def getRelationNumber(self): return self.number

    def setRelationNumber(self, newnumber): self.number = newnumber

    