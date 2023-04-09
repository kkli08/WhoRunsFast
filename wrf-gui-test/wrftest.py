import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from instances.WhoRunsFast import WhoRunsFast

class GameWindow(QWidget):
    def __init__(self, game):
        super().__init__()

        self.game = game

        # Initialize GUI elements
        self.played_cards_label = QLabel()
        self.bot_hand_label = QLabel()
        self.user_hand_label = QLabel()
        self.card_buttons_layout = QHBoxLayout()
        self.pass_button = QPushButton("Pass")
        self.reset_button = QPushButton("Reset")

        # Set up GUI layout
        layout = QVBoxLayout()
        layout.addWidget(self.played_cards_label)
        layout.addWidget(self.bot_hand_label)
        layout.addWidget(self.user_hand_label)
        layout.addLayout(self.card_buttons_layout)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.pass_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Connect button signals to game methods
        self.pass_button.clicked.connect(self.game.pass_turn)
        self.reset_button.clicked.connect(self.reset_game)

        # Start game loop
        self.update_gui()
    
    def update_gui(self):
        # Update played cards label
        # played_cards_pixmap = QPixmap("card_images/" + str(self.game.played_cards[-1]) + ".png")
        if self.game.played_cards:
            played_cards_pixmap = QPixmap("card_images/" + str(self.game.played_cards[-1]) + ".png")
            self.played_cards_label.setPixmap(played_cards_pixmap)

        # self.played_cards_label.setPixmap(played_cards_pixmap)

        # Update bot hand label
        bot_hand_pixmap = QPixmap("card_images/back.png")
        self.bot_hand_label.setPixmap(bot_hand_pixmap)

        # Update user hand label and card buttons
        user_hand_pixmap = QPixmap("card_images/back.png")
        self.user_hand_label.setPixmap(user_hand_pixmap)
        self.card_buttons_layout = QHBoxLayout()
        for i, card in enumerate(self.game.user):
            card_button = QPushButton()
            card_button.setFixedSize(71, 96)
            card_button.setIcon(QIcon("card_images/" + str(card) + ".png"))
            card_button.setIconSize(QSize(71, 96))
            card_button.clicked.connect(lambda _, i=i: self.game.play_user(i))
            self.card_buttons_layout.addWidget(card_button)
        self.card_buttons_layout.addStretch()
        self.layout().addLayout(self.card_buttons_layout)

        # Check if game is over and update GUI accordingly
        if self.game.game_over:
            winner_label = QLabel("Winner: " + self.game.winner)
            self.layout().addWidget(winner_label)
            self.pass_button.setDisabled(True)
            for card_button in self.card_buttons_layout.children():
                card_button.setDisabled(True)
        else:
            # Update current and previous player labels
            current_player_label = QLabel("Current player: " + self.game.current_player)
            prev_player_label = QLabel("Previous player: " + self.game.prev_player)
            self.layout().addWidget(current_player_label)
            self.layout().addWidget(prev_player_label)

            # Update card buttons and pass button enabled status
            if self.game.current_player == "user":
                self.pass_button.setDisabled(False)
                for card_button in self.card_buttons_layout.children():
                    card_button.setDisabled(False)
            else:
                self.pass_button.setDisabled(True)
                for card_button in self.card_buttons_layout.children():
                    card_button.setDisabled(True)
        
        # Update GUI
        self.update()

    def reset_game(self):
        self.game.reset_game()
        self.update_gui()

print("Starting application...")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WhoRunsFast()
    window = GameWindow(game)
    sys.exit(app.exec_())


