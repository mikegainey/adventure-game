from string import punctuation

class Character:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.conversation = None # ["saying 1", "saying 2", "saying 3"]
        self.conversation_x = 0
        self.QA = None # ({a set of key question words}, "answer (hint)")

    def talk(self):
        if self.conversation is None:
            print("{} doesn't want to talk with you.".format(self.name))
        else:
            print("[{} says]: {}".format(self.name, self.conversation[self.conversation_x]))
            self.conversation_x = (self.conversation_x + 1) % len(self.conversation)

    def ask(self):
        """If self.QA = ({"what", "weakness"}, "My weakness is cheese")
           If the quesion is "What is your weakness?" (or anything else containing the words "what" and "weakness"),
           then the answer would be printed: "My weakness is cheese."
        """
        if self.QA is None:
            print(f"{self.name} doesn't have any answers for you.")
        else:
            question = input("What is your question? ")
            if self.QA[0].issubset(set(question.lower().strip(punctuation).split())):
                print(f'''{self.name} says, "{self.QA[1]}."''')
            else:
                print(f'''{self.name} says, "meh."''')


class Enemy(Character):
    def fight(self, weapon):
        if weapon == self.weakness:
            return "you win"
        else:
            return "you lose"
