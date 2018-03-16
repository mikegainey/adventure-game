class Character:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.conversation = None # ["saying 1", "saying 2", "saying 3"]
        self.conversation_x = 0

    def talk(self):
        if self.conversation is None:
            print("{} doesn't want to talk with you.".format(self.name))
        else:
            print("[{} says]: {}".format(self.name, self.conversation[self.conversation_x]))
            self.conversation_x = (self.conversation_x + 1) % len(self.conversation)

    def fight(self, weapon):
        return "not an enemy"


class Enemy(Character):
    def fight(self, weapon):
        if weapon == self.weakness:
            return "you win"
        else:
            return "you lose"
