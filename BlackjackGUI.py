from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from instances.Stack import Stack

class BlackJackWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set the window size and title
        self.setWindowTitle('Blackjack')
        self.setGeometry(100, 100, 800, 600)
        
        # Create a new game
        self.stack = Stack()
        
        self.user = []
        self.bot = []

        self.user_score = 0
        self.bot_score = 0

        self.playing = True
        self.bust = False

        # Start the game
        self.start()
        
        # Show the window
        self.show()

    def start(self):
        # Shuffle the deck
        self.stack.shuffle()
        
        # Draw 1 card for the user and bot
        self.user.append(self.stack.cards.pop())
        self.user.append(self.stack.cards.pop())
        self.user.append(self.stack.cards.pop())
        self.user.append(self.stack.cards.pop())
        
        # Display the cards
        self.display_cards()

    def display_cards(self):
        # Display the user's cards
        for i, card in enumerate(self.user):
            card_label = QLabel(self)
            card_label.setPixmap(QPixmap('card_images/{}_of_{}.png'.format(card.value, card.suit)))

            # Move the card to the correct position
            card_label.move(100 + (i * 100), 100)
            card_label.show()



if __name__ == '__main__':
    app = QApplication([])
    window = BlackJackWindow()
    app.exec_()