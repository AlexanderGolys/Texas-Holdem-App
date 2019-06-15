class Player:
    def __init__(self, cash):
        self.stack = cash
        self.hand = []

    def get_cards(self, hand):
        self.hand = hand

    def pas(self):
        self.hand = []

