class Inventory:
    def __init__(self):
        self.items = set()

    def add_items(self, *items):
        for item in items:
            self.items.add(item)

    def list_items(self):
        return [item.name for item in self.items]

    def list_visible_items(self):
        visible_items = list()
        for item in self.items:
            if hasattr(item, 'properties'):
                if 'invisible' in item.properties:
                    continue
            visible_items.append(item.name)
        return visible_items
