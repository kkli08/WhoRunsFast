import random
from .PokerCard import PokerCard
from .Stack import Stack

class WhoRunsFast:
    def __init__(self):
        self.stack = Stack()
        self.user = []
        self.bot = []
        self.prev_player = None
        self.current_player = None
        self.played_cards = []
        self.game_over = False
        self.winner = None

        # Shuffle the stack
        self.stack.shuffle()

        # Deal cards to players
        num_cards = min(len(self.stack.cards), 18)
        for i in range(num_cards):
            self.bot.append(self.stack.draw_card())
            self.user.append(self.stack.draw_card())
        self.bot.sort()
        self.user.sort()

        # Determine who goes first
        if PokerCard("Clubs", 3) in self.user:
            self.prev_player = "user"
            self.current_player = "bot"
        else:
            self.prev_player = "bot"
            self.current_player = "user"
            
    def play(self, card):
        if self.game_over:
            return

        if self.current_player == "user" and card not in self.user:
            return
        elif self.current_player == "bot" and card not in self.bot:
            return

        if not self.played_cards:
            # First card played in this round
            if card.value == 16:
                # Joker bomb
                self.played_cards.append(card)
                if self.current_player == "bot":
                    self.bot.remove(card)
                else:
                    self.user.remove(card)
                self.end_game()
            else:
                self.played_cards.append(card)
                if self.current_player == "bot":
                    self.bot.remove(card)
                else:
                    self.user.remove(card)
                self.prev_player = self.current_player
                self.current_player = "user" if self.current_player == "bot" else "bot"
        else:
            # Check if card is valid
            prev_card = self.played_cards[-1]
            if card.value > prev_card.value and len(self.played_cards) == 1:
                # Single card
                self.played_cards.append(card)
                if self.current_player == "bot":
                    self.bot.remove(card)
                else:
                    self.user.remove(card)
                self.prev_player = self.current_player
                self.current_player = "user" if self.current_player == "bot" else "bot"
            elif card.value == prev_card.value and len(self.played_cards) == 1:
                # Pair
                self.played_cards.append(card)
                if self.current_player == "bot":
                    self.bot.remove(card)
                else:
                    self.user.remove(card)
                self.prev_player = self.current_player
                self.current_player = "user" if self.current_player == "bot" else "bot"
            elif card.value == prev_card.value and len(self.played_cards) == 2:
                # Three of a kind
                self.played_cards.append(card)
                if self.current_player == "bot":
                    self.bot.remove(card)
                else:
                    self.user.remove(card)
                self.prev_player = self.current_player
                self.current_player = "user" if self.current_player == "bot" else "bot"
    
    def end_game(self):
        self.game_over = True
        self.winner = "bot" if self.current_player == "user" else "user"
            
    def pass_turn(self):
        if not self.played_cards:
            return
        self.prev_player = self.current_player
        self.current_player = "user" if self.current_player == "bot" else "bot"
        self.played_cards = []
            
    def play_bot(self):
        if self.current_player != "bot":
            return
        if not self.played_cards:
            # Bot plays lowest card in hand
            card = self.bot[0]
        else:
            # Bot plays the smallest card that can beat the previous one
            prev_card = self.played_cards[-1]
            for card in self.bot:
                if card.value > prev_card.value:
                    break
            else:
                card = None
        if card:
            self.play(card)
        else:
            self.pass_turn()
            
    def play_user(self, card_index):
        if self.current_player != "user":
            return
        if card_index >= len(self.user):
            return
        card = self.user[card_index]
        self.play(card)

    def print_game_status(self):
        print("Played cards:", self.played_cards)
        print("Bot hand:", ", ".join(str(card) for card in self.bot))
        print("User hand:", ", ".join(str(card) for card in self.user))
        print("Current player:", self.current_player)
        print("Previous player:", self.prev_player)

    def play_game(self):
        while not self.game_over:
            if self.current_player == "bot":
                self.play_bot()
            else:
                self.print_game_status()
                card_index = int(input("Enter index of card to play, or -1 to pass: "))
                if card_index == -1:
                    self.pass_turn()
                else:
                    self.play_user(card_index)
        print("Game over!")
        print("Winner:", self.winner)

    def continue_game(self):
        print("Do you want to play again?")
        answer = input("Enter Y to continue, or any other key to exit: ")
        if answer.upper() == "Y":
            self.reset_game()
            self.play_game()
        else:
            print("Thanks for playing!")

    def reset_game(self):
        self.stack = Stack()
        self.user = []
        self.bot = []
        self.prev_player = None
        self.current_player = None
        self.played_cards = []
        self.game_over = False
        self.winner = None

        # Add all cards to the stack
        for suit in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            for value in range(3, 16):
                card = PokerCard(suit, value)
                self.stack.add_card(card)
        card = PokerCard("Joker", 16)
        self.stack.add_card(card)
        card = PokerCard("Joker", 17)
        self.stack.add_card(card)

        # Shuffle the stack
        random.shuffle(self.stack.cards)

        # Deal cards to players
        for i in range(0, len(self.stack.cards), 3):
            self.bot.append(self.stack.cards[i])
            self.user.append(self.stack.cards[i+1])
        self.bot.sort()
        self.user.sort()

        # Determine who goes first
        if PokerCard("Clubs", 3) in self.user:
            self.prev_player = "user"
            self.current_player = "bot"
        else:
            self.prev_player = "bot"
            self.current_player = "user"

    def deal(self):
        for i in range(0, len(self.stack.cards), 3):
            self.bot.append(self.stack.cards[i])
            self.user.append(self.stack.cards[i+1])
        self.bot.sort()
        self.user.sort()

        # Determine who goes first
        if PokerCard("Clubs", 3) in self.user:
            self.prev_player = "user"
            self.current_player = "bot"
        else:
            self.prev_player = "bot"
            self.current_player = "user"
