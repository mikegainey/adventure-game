from place import Place, Backpack
from character import Character, Enemy
from item import Item, Food, Container

# define places
kitchen = Place("Kitchen", "A dank and dirty room buzzing with flies.")
dining_hall = Place("Dining Hall", "A large room with ornate golden decorations on each wall.")
ballroom = Place("Ballroom", "A vast room with a shiny wooden floor.  Huge candlesticks guard the entrance. Stairs lead to a balcony overlooking the ballroom.")
balcony = Place("Balcony", "A balcony surrounding and overlooking the ballroom.  Stairs lead back down to the ballroom floor.")

# link places; parameters are (place to link, "how to get there")
kitchen.link_place(dining_hall, "south")
dining_hall.link_place(kitchen, "north")
dining_hall.link_place(ballroom, "west")
ballroom.link_place(dining_hall, "east")
ballroom.link_place(balcony, "up the stairs")
balcony.link_place(ballroom, "down the stairs")

# define items and their properties
cheese = Food("cheese")
cheese.add_properties("invisible") # because it's in the refrigerator

pizza = Food("pizza")
pizza.add_properties("invisible")  # because it's in the refrigerator

refrigerator = Container("refrigerator")
refrigerator.add_properties("too heavy")
refrigerator.add_contents(cheese, pizza)

kitchen.add_items(refrigerator, cheese, pizza)

book = Item("book")
dining_hall.add_items(book)

knife = Item("knife")
ballroom.add_items(knife)

# define characters and enemies
mike = Character("Mike", "a computer programmer")
mike.conversation = ["You never know when you could use some cheese.", "And you can't use cheese after you've eaten it."]
kitchen.inhabitants.add(mike)

dave = Enemy("Dave", "a smelly zombie")
dave.conversation = ["What's up, dude! I'm hungry.", "What do you call cheese that isn't yours?", "Nacho cheese!"]
dave.weakness = cheese
dining_hall.inhabitants.add(dave)

eddie = Enemy("Eddie", "another smelly zombie")
eddie.conversation = ["I'm not really hungry.", "Ok, I'm a zombie.  I'm always hungry.", "But for what?!"]
eddie.weakness = pizza
dining_hall.inhabitants.add(eddie)

tabitha = Enemy("Tabitha", "an enormous spider with countless eyes and furry legs.")
tabitha.conversation = ["Sssss....I'm so bored...", "Read any good books lately?"]
tabitha.weakness = book
ballroom.inhabitants.add(tabitha)


current_place = kitchen

backpack = Backpack()

result = None # the result of fighting enemies; a value of "you lose" ends the game

while result != "you lose":
    current_place.describe()

    # show contents of the backpack
    items = backpack.list_items()
    print("Your backpack contains: {}\n".format(", ".join(items)))

    # get a command from the user; assumes first word is the verb and last word is the object
    command = input("command: ").split()
    if len(command) == 0: # if the user just presses <Enter>
        continue
    cmd_verb, cmd_object = command[0], command[-1]
    print()

    # handle moving from place to place
    # If there are 3 linked places, choices will be ["1", "2", "3"]
    numberof_linked_places = len(current_place.linked_places)
    choices = [str(c + 1) for c in range(numberof_linked_places)]
    if command[0] in choices:
        place_index = int(command[0]) - 1
        current_place = current_place.linked_places[place_index][0]

    # handle talking to characters
    elif cmd_verb == "talk":
        if len(command) == 1:
            print("Specify who you want to talk to.")
        else:
            character = current_place.find_character(cmd_object)
            if character == "not here":
                print("{} is not here.".format(cmd_object))
            else:
                character.talk()

    # handle taking items (putting them in the backpack)
    elif cmd_verb == "take":
        if len(command) == 1:
            print("Specify what you want to take.")
        else:
            item = current_place.find_item(cmd_object)
            if item == "not here":
                print("I don't see a {}.".format(cmd_object))
            elif "too heavy" in item.properties:
                print("You can't take the {}.  It's too heavy.".format(cmd_object))
            else:
                print("You take the {}.".format(cmd_object))
                backpack.add_items(item)
                current_place.remove_item(item)

    # handle eating food (in your backpack)
    elif cmd_verb == "eat":
        if len(command) == 1:
            print("Specify what you want to eat.")
        else:
            # is the item in your backpack?
            food = backpack.find_item(cmd_object)
            if food == "not here":
                print("You don't have a {}.".format(cmd_object))
            # is the item food?
            elif not isinstance(food, Food):
                print("The {} is not food.".format(cmd_object))
            else:
                print("You eat the {}.".format(food.name))
                food.eat()
                # remove the food from your backpack
                backpack.remove_item(food)

    # handle opening items that are containers
    elif cmd_verb == "open":
        if len(command) == 1:
            print("Specify what you want to open.")
        else:
            # is the item in the current_place?
            container = current_place.find_item(cmd_object)
            if container == "not here":
                print("I don't see a {}.".format(cmd_object))
                # is the item a container?
            elif not isinstance(container, Container):
                print("The {} is not a container.".format(cmd_object))
            else:
                print("You open the {}.".format(container.name))
                for item in container.contents:
                    if "invisible" in item.properties:
                        item.properties.remove("invisible")

    # handle fighting Enemies
    elif cmd_verb == "fight":
        if len(command) == 1:
            print("Specify who you want to fight with.")
        else:
            # is the character present?
            character = current_place.find_character(cmd_object)
            if character == "not here":
                print("{} is not here.".format(cmd_object))
            elif not isinstance(character, Enemy):
                print("{} is not an enemy.".format(character.name))
            else:
                weapon_str = input("What will you fight with? ")
                weapon = backpack.find_item(weapon_str)
                if weapon == "not here":
                    print("\nYou don't have a {}.".format(weapon_str))
                else:
                    result = character.fight(weapon)
                    if result == "you win":
                        print("\nYou win the fight!")
                        current_place.remove_character(character)
                        backpack.remove_item(weapon)
                        # backpack.items.remove(weapon)
                    else:
                        print("\nYou lost the fight!")
                        # the while loop will end because result == "you loose"

    else:
        print("I don't understand.")

# the while loop terminated because you lost a fight
print("""\n{} says, "Game Over!".\n\n""".format(character.name))

# TODO:
# item properties to demonstrate: weapon, tool
# why isn't a container a Backpack?
# generate class docs with: python3 -m pydoc -w ./
