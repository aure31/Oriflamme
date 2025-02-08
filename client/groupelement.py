class GroupElement:
    def __init__(self, name):
        self.name = name
        self.elements = {}

    def affiche(self,window):
        for element in self.elements.values():
            element.affiche(window)

