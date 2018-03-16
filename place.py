import textwrap
import time
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
        return [item.name for item in self.items if 'invisible' not in item.properties]

    def list_food(self):
        return [item.name for item in self.items if isinstance(item, Food)]

    def find_item(self, cmd_object):
        for item in self.items:
            if item.name.lower() == cmd_object.lower():
                return item
        return "not here"


class Place(Backpack):
    def __init__(self, name, description):
        self.name = name               # "a short description"
        self.description = description # "a sentence about the place"
        self.linked_places = list()    # [(Place, "how to get there")]
        self.items = set()             # {Item}
        self.inhabitants = set()       # {Character}

    def link_place(self, place, route): # (Place, "route to get there")
        self.linked_places.append((place, route))

    # find a character in the Place
    def find_character(self, cmd_object):
        for character in self.inhabitants:
            if character.name.lower() == cmd_object.lower():
                return character
        return "not here"

    def remove_character(self, character):
        self.inhabitants.remove(character)

    def describe(self):
        tw = textwrap.TextWrapper(width=70, replace_whitespace=False, subsequent_indent='          ')
        # time.sleep(1)
        print("\n\n")
        print("-" * 70)
        print(tw.fill("Location: {}.  {}".format(self.name, self.description)))
        print("-" * 70)

        print("Inhabitants:")
        for inhabitant in self.inhabitants:
            print(" {}, {}".format(inhabitant.name, inhabitant.description))

        visible_items = self.list_visible_items()
        print("\nItems: {}".format(', '.join(visible_items)))

        print("\nPlaces you can go from here:")
        for number, place in enumerate(self.linked_places, 1):
            place_name, place_description = place[0].name, place[1]
            print(" {}. {}: {}".format(number, place_name, place_description))
        print("-" * 70)
        print("")
