class Player:
    def __init__(self, cash, number):
        self.stack = cash
        self.hand = []
        self.number = number

    def get_cards(self, hand):
        self.hand = hand

    def pas(self):
        self.hand = []

