class Place:
    def __init__(self, name, description):
        self.name = name               # "a short description"
        self.description = description # "a sentence about the place"
        self.linked_places = list()    # [(Place, "how to get there")]
        self.items = dict()            # {'cheese':{'food':'yes', 'weapon':'dave', 'visible':'no'}}
        self.inhabitants = list()      # [Character]

    def link_place(self, place, route): # (Place, "route to get there")
        self.linked_places.append((place, route))

    def describe(self):
        print("\n\nLocation: {}.  {}".format(self.name, self.description))
        print("-" * 40)

        inhabitants = ["{}, {}".format(inhabitant.name, inhabitant.description) for inhabitant in self.inhabitants]
        print("Inhabitants:")
        for inhabitant in inhabitants:
            print(" {}".format(inhabitant))

        # for item, attr in self.items.items():
        #     print(item, attr)
        items = [item for item, attr in self.items.items() if attr.get('visible') != 'no']
        print("Items: {}".format(', '.join(items)))

        print("Places you can go from here:")
        for number, place in enumerate(self.linked_places, 1):
            place_name, place_description = place[0].name, place[1]
            print(" {}. {}: {}".format(number, place_name, place_description))
        print("")

