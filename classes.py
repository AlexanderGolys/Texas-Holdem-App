class Player:
    def __init__(self, cash, number):
        self.stack = cash
        self.hand = []
        self.number = number
        self.bet = 0
        self.fold = False
        self.allin = False

    def get_cards(self, hand):
        self.hand = hand
        self.fold = False

    def fold_(self):
        self.fold = True

    def raise_(self, bet):
        if bet < self.stack:
            self.stack -= bet
            self.bet += bet
            print("player ", self.number, "raised ", bet)
        else:
            self.bet += self.stack
            self.stack = 0
            print("player ", self.number, "is all-in")

    def earn(self, amount):
        self.stack += amount

    def give_to_the_pot(self):
        self.bet = 0


class Card:
    def __init__(self, value, color):
        self.value = value
        self. color = color
