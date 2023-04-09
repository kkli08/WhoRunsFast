import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QButtonGroup
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
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
        self.setWindowTitle('Who Runs Fast?')
        # self.setFixedSize(800, 600)

        # Create labels to display the played cards, user's hand, and bot's hand
        self.played_cards_label = QLabel('Played Cards')
        self.user_hand_label = QLabel('Your Hand')
        self.bot_hand_label = QLabel('Bot\'s Hand')
        self.played_cards = QHBoxLayout()
        self.user_hand = QHBoxLayout()
        self.bot_hand = QHBoxLayout()

        # Create a button group to hold the user's hand of cards
        self.user_hand_group = QButtonGroup(self)
        self.user_hand_group.buttonClicked[int].connect(self.play_turn)
        
        # Add a button for each card in the user's hand
        for i, card in enumerate(self.game.user):
            card_button = QPushButton()
            card_button.setFixedSize(100, 150)  # Set a fixed size for the card button
            card_button.setIconSize(QSize(100, 150))  # Set the size of the card icon
            card_button.setIcon(QIcon('card_images/{}_of_{}.png'.format(card.value, card.suit)))
            self.user_hand.addWidget(card_button)
            self.user_hand_group.addButton(card_button, i)  # Add the card button to the button group
        
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
        if self.game.played_cards:
            played_cards_pixmap = QPixmap("card_images/" + str(self.game.played_cards[-1]) + ".png")
            self.played_cards_label.setPixmap(played_cards_pixmap)
        else:
            self.played_cards_label.setText('Played Cards')

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
            # card_label.setPixmap(QPixmap('card_images/' + str(card) + '.png'))
            card_label.setPixmap(QPixmap('card_images/{}_of_{}.png'.format(card.value, card.suit)).scaled(100, 145, Qt.KeepAspectRatio))
            card_label.setAlignment(Qt.AlignCenter)
            
            layout.addWidget(card_label)

    # def play_turn(self):
    #     # Play a card from the user's hand
    #     card_index = self.get_selected_card_index()
    #     if card_index is not None:
    #         self.game.play_user(card_index)
    #         self.update_gui()
    #     else:
    #         print('No card selected')
    def play_turn(self):
        # Play a card from the user's hand
        selected_button = self.user_hand_group.checkedButton()
        if selected_button:
            card_index = self.get_selected_card_index(self.user_hand_group.id(selected_button))
            self.game.play_user(card_index)
            self.update_gui()
        else:
            print('No card selected')


    def pass_turn(self):
        # Pass the user's turn
        self.game.pass_turn()
        self.update_gui()

    # def get_selected_card_index(self):
    #     # Get the index of the selected card in the user's hand
    #     for i in range(len(self.game.user)):
    #         card_label = self.user_hand.itemAt(i).widget()
    #         if card_label.hasFocus():
    #             return i
    #     return None
    def get_selected_card_index(self):
        # Get the index of the selected card in the user's hand
        selected_button = self.user_hand_group.checkedButton()
        if selected_button is not None:
            return self.user_hand_group.id(selected_button)
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_window = GameWindow()
    game_window.show()
    
    # Start the game loop
    while not game_window.game.game_over:
        if game_window.game.current_player == 'bot':
            game_window.game.play_bot()
            game_window.update_gui()
        else:
            app.processEvents()
    
    # Display the winner
    winner_label = QLabel('Winner: ' + game_window.game.winner)
    winner_label.setAlignment(Qt.AlignCenter)
    winner_label.show()
    
    # Wait for the user to close the window
    sys.exit(app.exec_())

