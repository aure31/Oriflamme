class GroupElement:
    def __init__(self, name):
        self.name = name
        self.elements = {}
        self.menus = []
        self.show = None

    def affiche(self,window):
        for element in self.elements.values():
            element.affiche(window)
    
    def addElement(self,name,element):
        self.elements[name] = element
        element.addMenu(self)

    def addMenu(self,menu):
        self.menus.append(menu)
    
    def getElement(self,name):
        return self.elements[name]
    
    def isAffiche(self):
        if self.show is not None:
            return self.show
        for menu in self.menus:
            if menu.isAffiche():
                return True
        return False
    

class ListElement:
    def __init__(self):
        self.elements = []
        self.menus = []

    def addMenu(self,menu):
        self.menus.append(menu)

    def affiche(self,window):
        for element in self.elements:
            element.affiche(window)
    
    def addElement(self,element):
        self.elements.append(element)
        element.menus = self.menus

    def removeElement(self,element):
        self.elements.remove(element)


class DynamicTextList(ListElement):
    def __init__(self,start:tuple[int,int] = (0,0),threshold:int = 10,color:tuple[int,int,int] = (255,255,255)):
        super().__init__()
        self.start = start
        self.threshold = threshold
        self.color = color
    
    def setText(self,text:list[str]):
        from client.classes import Texte
        self.elements = []
        y = self.start[1]
        for txt in text:
            self.addElement(Texte(txt,self.start[0],y,self.color))
            y += self.threshold


