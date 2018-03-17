class Item:
    def __init__(self, name):
        self.name = name
        self.properties = set()

    def add_properties(self, *properties):
        for property in properties:
            self.properties.add(property)

class Food(Item):
    def eat(self):
        print("nom nom nom ...")

class Container(Item):
    def __init__(self, name):
        super().__init__(name)
        self.contents = set()
        self.key = None

    def add_contents(self, *items):
        for item in items:
            self.contents.add(item)

