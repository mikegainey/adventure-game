from place import Place
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
cheese.add_property("invisible") # because it's in the refrigerator

pizza = Food("pizza")
pizza.add_property("invisible")  # because it's in the refrigerator

refrigerator = Container('refrigerator')
refrigerator.add_contents(cheese, pizza)
refrigerator.add_property("too heavy")

kitchen.add_items(refrigerator, cheese, pizza)

book = Item("book")
knife = Item("knife")

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
dining_hall.items.add(book)

tabitha = Enemy("Tabitha", "an enormous spider with countless eyes and furry legs.")
tabitha.conversation = ["Sssss....I'm so bored...", "Read any good books lately?"]
tabitha.weakness = book
ballroom.inhabitants.add(tabitha)
ballroom.items.add(knife)


current_place = kitchen

backpack = set()

result = None # the result of fighting enemies; a value of 'you lose' ends the game

while result != 'you lose':
    current_place.describe()

    # show contents of the backpack
    items = [item.name for item in backpack]
    print("Your backpack contains: {}\n".format(', '.join(items)))

    # get a command from the user; assumes first word is the verb and last word is the object
    command = input("command: ").split()
    if len(command) == 0:
        continue
    cmd_verb, cmd_object = command[0], command[-1]
    print("") # Trinket will print the () unless the quotes are present

    # handle moving from place to place
    # If there are 3 linked places, choices will be ['1', '2', '3']
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
            if character == 'not here':
                print("{} is not here.".format(cmd_object))
            else:
                character.talk()

    # handle taking items (putting them in the backpack)
    elif cmd_verb == 'take':
        if len(command) == 1:
            print("What will you take?")
        else:
            item = current_place.find_item(cmd_object)
            if item == 'not here':
                print("I don't see a {}.".format(cmd_object))
            elif 'too heavy' in item.properties:
                print("You can't take the {}.  It's too heavy.".format(cmd_object))
            else:
                print("You take the {}.".format(cmd_object))
                backpack.add(item)
                current_place.items.remove(item)

    # # handle eating food (in your backpack)
    # elif cmd_verb == 'eat':
    #     fooditems = [item for item, attr in backpack.items() if attr.get('food') == 'yes']
    #     # is the item in your backpack?
    #     if cmd_object not in backpack:
    #         print("You don't have a {}.".format(cmd_object))
    #     else:
    #         # is the item food?
    #         if cmd_object not in fooditems:
    #             print("The {} is not food.".format(cmd_object))
    #         else:
    #             print("You eat the {}.".format(cmd_object))
    #             # remove the food from your backpack
    #             del backpack[cmd_object]

    # # handle opening items that are containers
    # elif cmd_verb == 'open':
    #     items = [item for item, attr in current_place.items.items() if attr.get('visible') != 'no']
    #     containers = [item for item, attr in current_place.items.items() if attr.get('container') == 'yes']
    #     # is the item in the current_place?
    #     if cmd_object not in items:
    #         print("I don't see a {}.".format(cmd_object))
    #     else:
    #         # is the item a container?
    #         if cmd_object not in containers:
    #             print("The {} is not a container.".format(cmd_object))
    #         else:
    #             print("You open the {}.".format(cmd_object))
    #             # make the container's contents visible
    #             contents = current_place.items.get(cmd_object).get('contains')
    #             for item in contents:
    #                 current_place.items.get(item)['visible'] = 'yes'

    # # handle fighting Enemies
    # elif cmd_verb == 'fight':
    #     if len(command) == 1:
    #         # if the command string is only 1 word, the opponent hasn't been specified
    #         print("Who will you fight with?")
    #     else:
    #         # is the character present?
    #         character = [character for character in current_place.inhabitants
    #                     if character.name.lower() == cmd_object.lower()]
    #         if len(character) == 0:
    #             print("{} is not here.".format(cmd_object))
    #         else:
    #             character = character[0]
    #             weapon = input("What will you fight with? ")
    #             if weapon not in backpack:
    #                 print("\nYou don't have a {}.".format(weapon))
    #             else:
    #                 result = character.fight(weapon)
    #                 if result == 'you win':
    #                     print("\nYou win the fight!")
    #                     # remove the Enemy and weapon
    #                     current_place.inhabitants.remove(character)
    #                     del backpack[weapon]
    #                 elif result == 'not an enemy':
    #                     pass # nothing will happen
    #                 else:
    #                     print("\nYou lost the fight!")
    #                     # the while loop will end because result == 'you loose'

    else:
        print("I don't understand.")

# the while loop terminated because you lost a fight
print("""\n{} says, "Game Over!".\n\n""".format(character.name))

# TODO:
# item properties to demonstrate: weapon, tool
