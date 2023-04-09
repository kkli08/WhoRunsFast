from random import shuffle
from .Stack import Stack

class Game:
    def __init__(self):
        self.stack = Stack()
        self.user = []
        self.bot = []
        self.turn = 0
        self.playing = True
        
    def start(self):
        shuffle(self.stack.cards)
        for i in range(2):
            self.user.append(self.stack.cards.pop())
            self.bot.append(self.stack.cards.pop())
            
        while self.playing:
            if self.turn == 0:
                self.user_turn()
            else:
                self.bot_turn()
                
            if len(self.user) == 0 or len(self.bot) == 0:
                self.playing = False
                
        self.end()
            
    def user_turn(self):
        print("Your turn!")
        print("Your cards:", [str(card.value) + " of " + card.suit for card in self.user])
        print("Bot's card:", str(self.bot[0].value) + " of " + self.bot[0].suit)
        print("Enter 'hit' to draw a card, or 'stay' to end your turn.")
        
        action = input().lower()
        while action not in ["hit", "stay"]:
            print("Invalid input! Enter 'hit' or 'stay'.")
            action = input().lower()
            
        if action == "hit":
            card = self.stack.cards.pop()
            self.user.append(card)
            print("You drew the", str(card.value) + " of " + card.suit)
            
            if self.get_score(self.user) > 21:
                print("Bust! You lose.")
                self.playing = False
        else:
            print("You end your turn with", self.get_score(self.user))
            self.turn = 1
            
    def bot_turn(self):
        print("Bot's turn!")
        print("Bot's cards:", [str(card.value) + " of " + card.suit for card in self.bot])
        
        while self.get_score(self.bot) < 17:
            card = self.stack.cards.pop()
            self.bot.append(card)
            print("Bot drew the", str(card.value) + " of " + card.suit)
            
            if self.get_score(self.bot) > 21:
                print("Bot busts! You win.")
                self.playing = False
                return
        
        print("Bot ends its turn with", self.get_score(self.bot))
        self.turn = 0
        
    def get_score(self, hand):
        score = 0
        for card in hand:
            if card.value > 10:
                score += 10
            elif card.value == 1:
                score += 11
            else:
                score += card.value
        
        # Handle aces
        num_aces = sum([1 for card in hand if card.value == 1])
        while score > 21 and num_aces > 0:
            score -= 10
            num_aces -= 1
            
        return score
    
    def end(self):
        user_score = self.get_score(self.user)
        bot_score = self.get_score(self.bot)
        
        if user_score > bot_score:
            print("You win!")
        elif user_score < bot_score:
            print("You lose!")
        else:
            print("It's a tie!")
