from item import Food

class Backpack:
    def __init__(self):
        self.items = set()

    def add_items(self, *items):
        for item in items:
            self.items.add(item)

    def remove_item(self, item):
        self.items.remove(item)

    def list_items(self):
        return [item.name for item in self.items]

    def list_byproperty(self, property):
        return [item.name for item in self.items if property in item.properties]

    def list_visible_items(self):
        visible_items = list()
        for item in self.items:
            if 'invisible' in item.properties:
                continue
            visible_items.append(item.name)
        return visible_items

    def list_food(self):
        return [item.name for item in self.items if isinstance(item, Food)]

    def find_item(self, cmd_object):
        for item in self.items:
            if item.name.lower() == cmd_object.lower():
                return item
        return "not here"


if __name__ == '__main__':
   pass 
