from random import shuffle
from .Stack import Stack
import random

class BlackJack:
    def __init__(self):
        self.stack = Stack()
        
        self.user = []
        self.bot = []

        self.user_score = 0
        self.bot_score = 0

        self.playing = True
        self.bust = False
        
    def start(self):
        shuffle(self.stack.cards)

        self.user_turn()
        
        #if user busts, the game ends
        if self.bust == False:
            self.bot_turn()
            #if bot busts, the game ends
            if self.bust == False:
                self.end()
            
    def user_turn(self):

        #Draw 1 card
        self.user.append(self.stack.cards.pop())
        print("\nYour turn!\n")
        print("Your cards:", [str(card.value) + " of " + card.suit for card in self.user])
        # print("Bot's card:", str(self.bot[0].value) + " of " + self.bot[0].suit)
        print("Bot card: [hidden]\n")
        print("Enter 'hit' to draw a card, or 'stay' to end your turn.")
        
        action = input().lower()
        while action not in ["hit", "stay"]:
            print("Invalid input! Enter 'hit' or 'stay'.")
            action = input().lower()

        while action == "hit":
            card = self.stack.cards.pop()
            self.user.append(card)
            print("You drew the", str(card.value) + " of " + card.suit)
            print("Your cards:", [str(card.value) + " of " + card.suit for card in self.user])
            
            if self.get_score(self.user) > 21:
                print("Bust! You lose, Your score:", self.get_score(self.user))
                self.playing = False
                self.bust = True
                return
            
            action = input("Enter 'hit' to draw a card, or 'stay' to end your turn.\n").lower()

            if action == "stay":
                self.user_score = self.get_score(self.user)
                print("You end your turn with", self.user_score)
            
    def bot_turn(self):
        #Draw 1 card
        self.bot.append(self.stack.cards.pop())

        print("Bot's turn!\n")
        print("Bot's cards: [hidden]\n")
        
        #when bot has 17 or more, it will have a 30% chance to hit
        while self.get_score(self.bot) < 21:
            if self.get_score(self.bot) < 17:
                card = self.stack.cards.pop()
                self.bot.append(card)
                print("Bot drew the [hidden]"'\n')
            
            else:
                try_index = random.randint(1,10)
                if try_index <= 3 and self.get_score(self.bot) < 21:
                    card = self.stack.cards.pop()
                    self.bot.append(card)
                    print("Bot drew the [hidden]"'\n')

                    self.bot_score = self.get_score(self.bot)
                    print("Bot ends its turn with", self.bot_score)
                    
                elif try_index > 3 and self.get_score(self.bot) < 21:
                    self.bot_score = self.get_score(self.bot)
                    print("Bot ends its turn with", self.bot_score)
                    break
        
        #if bot busts, the game ends
        if self.get_score(self.bot) > 21:
            print("Bot busts! You win.")
            print("Bot's cards:", [str(card.value) + " of " + card.suit for card in self.bot])

            self.playing = False
            self.bust = True
            return
        
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
        print("\nYour cards:", [str(card.value) + " of " + card.suit for card in self.user])
        print("Bot's cards:", [str(card.value) + " of " + card.suit for card in self.bot])

        if self.user_score > self.bot_score:
            print("\nYou win!")
        elif self.user_score < self.bot_score:
            print("\nYou lose!")
        else:
            print("\nIt's a tie!")

        #clear the hand cards
        self.user = []
        self.bot = []
