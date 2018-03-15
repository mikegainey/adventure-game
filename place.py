from backpack import Backpack

class Place:
    def __init__(self, name, description):
        self.name = name               # "a short description"
        self.description = description # "a sentence about the place"
        self.linked_places = list()    # [(Place, "how to get there")]
        self.items = Backpack()
        self.inhabitants = set()       # {Character}

    def link_place(self, place, route): # (Place, "route to get there")
        self.linked_places.append((place, route))

    # find a character in the Place
    def find_character(self, cmd_object):
        for character in self.inhabitants:
            if character.name.lower() == cmd_object.lower():
                return character
        return "not here"

    def describe(self):
        input("\nPress <Enter> to continue ")
        print("\n\nLocation: {}.  {}".format(self.name, self.description))
        print("-" * 40)

        print("Inhabitants:")
        for inhabitant in self.inhabitants:
            print(" {}, {}".format(inhabitant.name, inhabitant.description))

        visible_items = self.items.list_visible_items()
        print("\nItems: {}".format(', '.join(visible_items)))

        print("\nPlaces you can go from here:")
        for number, place in enumerate(self.linked_places, 1):
            place_name, place_description = place[0].name, place[1]
            print(" {}. {}: {}".format(number, place_name, place_description))
        print("-" * 40)
        print("")
