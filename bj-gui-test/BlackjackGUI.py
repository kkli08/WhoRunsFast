import tkinter as tk
from instances.BlackJack import BlackJack
import tkinter.messagebox as messagebox

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        self.game = BlackJack()
        self.user_cards = []
        
        self.title_label = tk.Label(master, text="Welcome to Blackjack!")
        self.title_label.pack()
        
        self.user_cards_label = tk.Label(master, text="Your cards:")
        self.user_cards_label.pack()
        
        self.bot_card_label = tk.Label(master, text="Bot's card: [hidden]")
        self.bot_card_label.pack()
        
        self.hit_button = tk.Button(master, text="Hit", command=self.hit)
        self.hit_button.pack(side=tk.LEFT)
        
        self.stay_button = tk.Button(master, text="Stay", command=self.stay)
        self.stay_button.pack(side=tk.RIGHT)
        
        self.status_label = tk.Label(master, text="")
        self.status_label.pack()
        
    def hit(self):
        card = self.game.stack.cards.pop()
        self.user_cards.append(card)
        
        card_str = str(card.value) + " of " + card.suit
        self.user_cards_label.configure(text="Your cards: " + ", ".join([card_str for card in self.user_cards]))
        
        score = self.game.get_score(self.user_cards)
        if score > 21:
            self.end_game("Bust! You lose.")
        elif score == 21:
            self.end_game("Blackjack! You win.")
            
    def stay(self):
        while self.game.get_score(self.game.bot) < 17:
            card = self.game.stack.cards.pop()
            self.game.bot.append(card)
            self.bot_card_label.configure(text="Bot's card: " + str(card.value) + " of " + card.suit)
            
            if self.game.get_score(self.game.bot) > 21:
                self.end_game("Bot busts! You win.")
                return
        
        user_score = self.game.get_score(self.user_cards)
        bot_score = self.game.get_score(self.game.bot)
        
        if user_score > bot_score:
            self.end_game("You win!")
        elif user_score < bot_score:
            self.end_game("You lose!")
        else:
            self.end_game("It's a tie!")
            
    def end_game(self, message):
        self.hit_button.configure(state=tk.DISABLED)
        self.stay_button.configure(state=tk.DISABLED)
        self.status_label.configure(text=message)
        
        # Prompt user to play again
        answer = messagebox.askyesno("Play again?", "Do you want to play again?")
        if answer:
            # Reset game state and GUI
            self.game = BlackJack()
            self.user_cards = []
            self.user_cards_label.configure(text="Your cards:")
            self.bot_card_label.configure(text="Bot's card: [hidden]")
            self.hit_button.configure(state=tk.NORMAL)
            self.stay_button.configure(state=tk.NORMAL)
            self.status_label.configure(text="")
        else:
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = BlackjackGUI(root)
    root.mainloop()
