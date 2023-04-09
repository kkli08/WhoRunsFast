import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
# import WhoRunsFast in the instances folder
from instances.WhoRunsFast import WhoRunsFast

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a new card game
        self.game = WhoRunsFast()

        # Set up the GUI
        self.initUI()

    def initUI(self):
        # Set the window title
        self.setWindowTitle('Card Game')

        # Create labels to display the played cards, user's hand, and bot's hand
        self.played_cards_label = QLabel('Played Cards')
        self.user_hand_label = QLabel('Your Hand')
        self.bot_hand_label = QLabel('Bot\'s Hand')
        self.played_cards = QHBoxLayout()
        self.user_hand = QHBoxLayout()
        self.bot_hand = QHBoxLayout()

        # Add the labels to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.played_cards_label)
        main_layout.addLayout(self.played_cards)
        main_layout.addWidget(self.user_hand_label)
        main_layout.addLayout(self.user_hand)
        main_layout.addWidget(self.bot_hand_label)
        main_layout.addLayout(self.bot_hand)

        # Add a button for the user to play their turn
        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.play_turn)
        main_layout.addWidget(self.play_button)

        # Add a button for the user to pass their turn
        self.pass_button = QPushButton('Pass')
        self.pass_button.clicked.connect(self.pass_turn)
        main_layout.addWidget(self.pass_button)

        # Set the main layout
        self.setLayout(main_layout)

        # Update the GUI with the initial game state
        self.update_gui()

    def update_gui(self):
        # Update the played cards label
        played_cards_text = 'Played Cards: ' + ', '.join(str(card) for card in self.game.played_cards)
        self.played_cards_label.setText(played_cards_text)

        # Update the user's hand
        self.update_hand(self.game.user, self.user_hand)

        # Update the bot's hand
        self.update_hand(self.game.bot, self.bot_hand)

        # Enable/disable the play button depending on whose turn it is
        self.play_button.setEnabled(self.game.current_player == 'user')

    def update_hand(self, hand, layout):
        # Clear the current hand layout
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        # Add a label for each card in the hand
        for card in hand:
            card_label = QLabel(str(card))
            card_label.setPixmap(QPixmap('card_images/' + str(card) + '.png'))
            layout.addWidget(card_label)

    def play_turn(self):
        # Play a card from the user's hand
        card_index = self.get_selected_card_index()
        if card_index is not None:
            self.game.play_user(card_index)
            self.update_gui()

    def pass_turn(self):
        # Pass the user's turn
        self.game.pass_turn()
        self.update_gui()

    def get_selected_card_index(self):
        # Get the index of the selected card in the user's hand
        for i in range(len(self.game.user)):
            card_label = self.user_hand.itemAt(i).widget()
            if card_label.hasFocus():
                return i
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_window = GameWindow()
    game_window.show()
    app.exec_()


