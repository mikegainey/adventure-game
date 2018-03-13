class Place:
    def __init__(self, name, description):
        self.name = name               # "a short description"
        self.description = description # "a sentence about the place"
        self.linked_places = list()    # [(Place, "how to get there")]
        self.items = set()             # items are Items (includes Food, Container, ...)
        self.inhabitants = set()       # {Character}

    def link_place(self, place, route): # (Place, "route to get there")
        self.linked_places.append((place, route))

    def add_items(self, *items):
        for item in items:
            self.items.add(item)

    def describe(self):
        print("\n\nLocation: {}.  {}".format(self.name, self.description))
        print("-" * 40)

        print("Inhabitants:")
        for inhabitant in self.inhabitants:
            print(" {}, {}".format(inhabitant.name, inhabitant.description))

        visible_items = list()
        for item in self.items:
            if 'invisible' in item.properties:
                continue
            visible_items.append(item.name)
        print("\nItems: {}".format(', '.join(visible_items)))

        print("\nPlaces you can go from here:")
        for number, place in enumerate(self.linked_places, 1):
            place_name, place_description = place[0].name, place[1]
            print(" {}. {}: {}".format(number, place_name, place_description))
        print("")

