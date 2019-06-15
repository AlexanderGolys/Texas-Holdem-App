class Player:
    def __init__(self, cash, number):
        self.stack = cash
        self.hand = []
        self.number = number
        self.bet = 0
        self.fold = False

    def get_cards(self, hand):
        self.hand = hand
        self.fold = False

    def fold_(self):
        self.fold = True

    def raise_(self, bet):
        self.stack -= bet
        self.bet += bet
        print("player ", self.number, "raised ", bet)

    def earn(self, amount):
        self.stack += amount
