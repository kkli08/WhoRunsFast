import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from instances.BlackJack import BlackJack

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Blackjack")

        self.init_ui()

    def init_ui(self):
        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(10, 10, 100, 30)
        self.start_button.clicked.connect(self.start_game)

        self.hit_button = QPushButton("Hit", self)
        self.hit_button.setGeometry(120, 10, 100, 30)
        self.hit_button.clicked.connect(self.hit)
        self.hit_button.setDisabled(True)

        self.stay_button = QPushButton("Stay", self)
        self.stay_button.setGeometry(230, 10, 100, 30)
        self.stay_button.clicked.connect(self.stay)
        self.stay_button.setDisabled(True)

        self.user_cards_label = QLabel("Your cards:", self)
        self.user_cards_label.setGeometry(10, 50, 100, 30)

        self.bot_cards_label = QLabel("Bot cards:", self)
        self.bot_cards_label.setGeometry(10, 250, 100, 30)

        self.cards_scene = QGraphicsScene()
        self.cards_view = QGraphicsView(self.cards_scene, self)
        self.cards_view.setGeometry(10, 80, 800, 400)
        self.cards_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.cards_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def start_game(self):
        self.game = BlackJack()
        self.game.start()

        self.start_button.setDisabled(True)
        self.hit_button.setDisabled(False)
        self.stay_button.setDisabled(False)

        # Display cards using the card_images folder and back1.png for hidden cards

    def hit(self):
        # Handle hit action
        pass

    def stay(self):
        # Handle stay action
        pass

    def update_ui(self):
        # Update UI after each action (hit or stay)
        pass

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
