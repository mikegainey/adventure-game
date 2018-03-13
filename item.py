class Item:
    def __init__(self, name):
        self.name = name
        self.properties = set()

    def add_property(self, property):
        self.properties.add(property)

class Food(Item):
    pass

class Container(Item):
    def __init__(self, name):
        super().__init__(name)
        self.contents = set()

    def add_contents(self, *items):
        for item in items:
            self.contents.add(item)

