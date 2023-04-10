from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton
from PyQt5.QtMultimedia import QSound, QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from instances.Stack import Stack
import time

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome!')
        self.setFixedSize(1920, 1080)

        #set icon
        self.setWindowIcon(QIcon('../src/icon.png'))

        #set ./bg_images/bg.jpg as background
        self.bg = QLabel(self)
        self.bg.setPixmap(QPixmap('../src/bg.jpg'))
        self.bg.setGeometry(0, 0, 1920, 1080)
        self.bg.setScaledContents(True)

        # Add logo to the beginning page
        logo_width, logo_height = 400, 200
        x = (1800 - logo_width) // 2
        y = (400 - logo_height) // 2
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap('../card_images/logo.png'))
        self.logo.setGeometry(x, y, logo_width, logo_height)  # Replace x, y, width, and height with desired values
        self.logo.setScaledContents(True)

        # Create a new card game
        self.game = Stack()

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_game)
        #keep the button on the top and fixed, center it
        self.start_button.setFixedSize(200, 100)
        self.start_button.move(800, 500)
        self.start_button.setParent(self)

        #Add a How to Play button
        self.how_to_play_button = QPushButton('How to Play')
        self.how_to_play_button.clicked.connect(self.how_to_play)
        #keep the button on the top and fixed, center it
        self.how_to_play_button.setFixedSize(200, 100)
        self.how_to_play_button.move(800, 700)
        self.how_to_play_button.setParent(self)

        #set the font size of the button
        font = self.start_button.font()
        font.setPointSize(25)
        self.start_button.setFont(font)

        font = self.how_to_play_button.font()
        font.setPointSize(18)
        self.how_to_play_button.setFont(font)

        # Create hit button and hide it initially
        self.hit_button = QPushButton('Hit', self)
        self.hit_button.setFixedSize(200, 100)
        self.hit_button.move(760, 500)
        self.hit_button.setFont(font)
        self.hit_button.clicked.connect(self.hit)
        self.hit_button.hide()

        # Create stay button and hide it initially
        self.stay_button = QPushButton('Stay', self)
        self.stay_button.setFixedSize(200, 100)
        self.stay_button.move(1040, 500)
        self.stay_button.setFont(font)
        self.stay_button.clicked.connect(self.stay)
        self.stay_button.hide()

        #set ./bg_images/huanledoudizhu.mp3 as background music
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile('../src/huanledoudizhu.mp3')))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.play()

    def start_game(self):
        self.logo.hide()
        self.start_button.hide()
        self.hit_button.show()
        self.stay_button.show()

    def how_to_play(self):
        self.logo.hide()
        self.start_button.hide()
        self.how_to_play_button.hide()

        #write the rules of the game
        self.rules = QLabel(self)
        self.rules.setText('Game of the rules')
        self.rules.setAlignment(Qt.AlignCenter)
        #set the font size of the rules
        font = self.rules.font()
        font.setPointSize(30)
        #set the font color of the rules
        self.rules.setStyleSheet("color: black")
        self.rules.setFont(font)
        self.rules.setFixedSize(200, 100)
        self.rules.move(800, 500)
        self.rules.show()


    def hit(self):
        # Add your hit logic here
        pass

    def stay(self):
        # Add your stay logic here
        pass

if __name__ == '__main__':
    app = QApplication([])
    window = GameWindow()
    window.show()

    app.exec_()