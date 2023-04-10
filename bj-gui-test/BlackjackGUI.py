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

        start_button = QPushButton('Start')
        start_button.clicked.connect(self.start_game)
        #keep the button on the top and fixed, center it
        start_button.setFixedSize(200, 100)
        start_button.move(800, 500)
        start_button.setParent(self)

        #Add a How to Play button
        how_to_play_button = QPushButton('How to Play')
        how_to_play_button.clicked.connect(self.how_to_play)
        #keep the button on the top and fixed, center it
        how_to_play_button.setFixedSize(200, 100)
        how_to_play_button.move(800, 700)
        how_to_play_button.setParent(self)

        #set the font size of the button
        font = start_button.font()
        font.setPointSize(30)
        start_button.setFont(font)

        #set ./bg_images/huanledoudizhu.mp3 as background music
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile('../src/huanledoudizhu.mp3')))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.play()

    def start_game(self):
        self.logo.hide()

    def how_to_play(self):
        self.logo.hide()



if __name__ == '__main__':
    app = QApplication([])
    window = GameWindow()
    window.show()

    app.exec_()