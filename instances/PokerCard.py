import random
from random import shuffle

class PokerCard:
    def __init__(self, suit: str, value: int):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
class Stack:
    def __init__(self):
        self.cards = []
        for suit in ["hearts", "diamonds", "clubs", "spades"]:
            for value in range(1, 14):
                card = PokerCard(suit, value)
                self.cards.append(card)

    def __repr__(self):
        return f"Stack of {len(self.cards)} cards"
    
    def shuffle(self):
        random.shuffle(self.cards)