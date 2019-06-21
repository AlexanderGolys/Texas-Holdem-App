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

    def __lt__(self, other):
        if self.value < other.value:
            return True
        return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        return False

    def v_to_sign(self):
        if self.value < 9:
            return str(self.value + 1)
        elif self.value == 9:
            return '10'
        elif self.value == 10:
            return 'Jack'
        elif self.value == 11:
            return 'Queen'
        elif self.value == 12:
            return 'King'
        elif self.value == 13:
            return 'Ace'
