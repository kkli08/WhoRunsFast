import random
from random import shuffle

class PokerCard:
    def __init__(self, suit: str, value: int):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
    def __lt__(self, other):
        return self.value < other.value