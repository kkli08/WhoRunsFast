from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from instances.Stack import Stack

class BlackJackWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Blackjack')
        self.setFixedSize(1920, 1080)

        #set ./bg_images/bg.jpg as background
        self.bg = QLabel(self)
        self.bg.setPixmap(QPixmap('../bg_images/bg.jpg'))
        self.bg.setGeometry(0, 0, 1920, 1080)
        self.bg.setScaledContents(True)

        # Add logo to the beginning page
        logo_width, logo_height = 400, 200
        x = (1800 - logo_width) // 2
        y = 20
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

        #set the font size of the button
        font = start_button.font()
        font.setPointSize(30)
        start_button.setFont(font)

        #set ./bg_images/huanledoudizhu.mp3 as background music, loop forever
        self.bg_music = QMediaPlayer()
        self.bg_music.setMedia(QMediaContent(QUrl.fromLocalFile('../bg_images/huanledoudizhu.mp3')))
        self.bg_music.setVolume(50)
        self.bg_music.play()

        # Set up the GUI
        # self.initUI()

    def start_game(self):
        pass
if __name__ == '__main__':
    app = QApplication([])
    window = BlackJackWindow()
    window.show()

    app.exec_()