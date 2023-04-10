from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QMessageBox, QWidget
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5 import QtTest
from instances.Stack import Stack
import random
import webbrowser
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

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_game)
        #keep the button on the top and fixed, center it
        self.start_button.setFixedSize(200, 100)
        self.start_button.move(800, 500)
        self.start_button.setParent(self)
        self.start_button.setCursor(Qt.PointingHandCursor)

        #set a clickable image at the botton right corner
        self.github_icon = QLabel(self)
        self.github_icon.setPixmap(QPixmap('../src/GitHub.png'))
        self.github_icon.setGeometry(1800,950, 60, 60)
        self.github_icon.setScaledContents(True)
        #change the cursor to point when hover over the image
        self.github_icon.setCursor(Qt.PointingHandCursor)

        self.github_icon.mousePressEvent = self.open_github

        #set the font size of the button
        font = self.start_button.font()
        font.setPointSize(25)
        self.start_button.setFont(font)

        # Create hit button and hide it initially
        self.hit_button = QPushButton('Hit', self)
        self.hit_button.setFixedSize(200, 100)
        self.hit_button.move(760, 500)
        self.hit_button.setFont(font)
        self.hit_button.clicked.connect(self.hit)
        self.hit_button.hide()
        self.hit_button.setCursor(Qt.PointingHandCursor)

        # Create stay button and hide it initially
        self.stay_button = QPushButton('Stay', self)
        self.stay_button.setFixedSize(200, 100)
        self.stay_button.move(1040, 500)
        self.stay_button.setFont(font)
        self.stay_button.clicked.connect(self.stay)
        self.stay_button.hide()
        self.stay_button.setCursor(Qt.PointingHandCursor)

        #set ./bg_images/huanledoudizhu.mp3 as background music
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile('../src/huanledoudizhu.mp3')))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.play()

        ########################### Game Attribute
        # Create a new card game
        self.game = Stack()

        # Create a new player
        self.user = []
        self.bot = []

        self.user_score = 0
        self.bot_score = 0

        self.bust = False

        self.current_player = 'user'

    def start_game(self):
        self.logo.hide()
        self.start_button.hide()
        self.github_icon.hide()
        self.hit_button.show()
        self.stay_button.show()
        
        #Start game logic
        #Draw 1 card for player and 1 card for bot
        random.shuffle(self.game.cards)
        
        self.user.append(self.game.cards.pop())
        self.bot.append(self.game.cards.pop())

        #wait for 1 second to run the next line
        QtTest.QTest.qWait(100)
        self.display_face(self.user)
        self.display_bot_face(self.bot)
        self.display_score(self.user)

    def hit(self):
        #Action when hit button is clicked
        #Draw 1 card for player
        self.user.append(self.game.cards.pop())
        QtTest.QTest.qWait(100)
        self.display_face(self.user)
        self.display_score(self.user)
        if self.get_score(self.user) > 21:
            self.bust = True
            self.end()
            
    def stay(self):
        #Action when stay button is clicked
        #Pass and check the score
        score = self.get_score(self.user)
        if score > 21:
            self.bust = True
            self.end()
        else:
            self.current_player = 'bot'
            self.hit_button.hide()
            self.stay_button.hide()
            self.bot_turn()

    def bot_turn(self):
        #bot will keep hitting until the score is greater than 17,
        while self.get_score(self.bot) < 21:
            if self.get_score(self.bot) < 17:
                self.bot_hit()
            else:
                try_index = random.randint(1,10)
                if try_index <= 3 and self.get_score(self.bot) < 21:
                    self.bot_hit()
                else:
                    self.bot_stay()
                    break
            QtTest.QTest.qWait(1000)

        if self.get_score(self.bot) == 21:
            self.end()
        
    def bot_hit(self):
        #Draw 1 card for bot
        self.bot.append(self.game.cards.pop())
        self.display_bot_face(self.bot)
        if self.get_score(self.bot) > 21:
            self.bust = True
            self.end()

    def bot_stay(self):
        #Pass and check the score
        score = self.get_score(self.bot)
        if score > 21:
            self.bust = True
        #reveal the bot's cards
        self.end()

    #handle esc key to pop up the warning window, return to the main window if click 'yes'
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

        if event.key() == Qt.Key_H:
            #read the help.txt file
            with open('../src/howToPlay.txt', 'rb') as f:
                help_text = f.read()
            help_text = help_text.decode('utf-8')
            #open a message box
            QMessageBox.about(self, 'Help', help_text)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Tired so soon?', '这么快就累啦？快来试试我们的充值系统吧！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.No:
            event.accept()
        else:
            event.ignore()

    def open_github(self, event):
        webbrowser.open('https://github.com/kkli08/WhoRunsFast/blob/main/README.md')

    def display_face(self,player):
        #display the card at the position (x,y)
        for i in range(len(player)):
            card = QLabel(self)
            card.setPixmap(QPixmap('../card_images/'+str(player[i].value)+'_of_'+player[i].suit+'.png').scaled(200, 245, Qt.KeepAspectRatio))
            #resize the image to 100*150 and keep the card at the bottom of the window
            card.setGeometry(600 + i*50, 900, 200, 245)
            self.layout().addWidget(card)

    #function to check bot cards in order to debug
    def display_bot_face(self,player):
        #display the card at the position (x,y)
        for i in range(len(player)):
            card = QLabel(self)
            card.setPixmap(QPixmap('../card_images/'+str(player[i].value)+'_of_'+player[i].suit+'.png').scaled(200, 245, Qt.KeepAspectRatio))
            #resize the image to 100*150 and keep the card at the bottom of the window
            card.setGeometry(600 + i*50, 50, 200, 245)
            self.layout().addWidget(card)

    def display_back(self,player):
        #display the card at the position (x,y)
        #the card should be display as image in card_images/back2.png
        for i in range(len(player)):
            card = QLabel(self)
            card.setPixmap(QPixmap('../card_images/back2.png').scaled(200, 245, Qt.KeepAspectRatio))
            #shrink the whole image to 100*150
            card.setGeometry(600 + i*50, -50, 200, 245)
            self.layout().addWidget(card)

    def get_score(self, hand):
        score = 0
        for card in hand:
            if card.value > 10:
                score += 10
            elif card.value == 1:
                score += 11
            else:
                score += card.value
        
        # Handle aces
        num_aces = sum([1 for card in hand if card.value == 1])
        while score > 21 and num_aces > 0:
            score -= 10
            num_aces -= 1
        return score
    
    def display_score(self, hand):
        #remove the previous score, this one is not working as well, fuck it.
        for i in reversed(range(self.layout().count())):
            widgetToRemove = self.layout().itemAt(i).widget()
            if widgetToRemove.inherits("QLabel"):
                widgetToRemove.setParent(None)

        #display the score of the player
        score = self.get_score(hand)
        score_label = QLabel(self)
        score_label.setText(str(score))
        #set font color and size
        score_label.setStyleSheet("color: white; font-size: 30px")
        score_label.setGeometry(600, 800, 100, 100)
        self.layout().addWidget(score_label)
    
    def end(self):
        #Display the result as message box
        if self.bust and self.current_player == 'user':
            QMessageBox.about(self, 'Game Over', 'Bust!!!! You lose.\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))
        elif self.bust and self.current_player == 'bot':
            QMessageBox.about(self, 'Game Over', 'Congrat!!!! You win.\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot))+'(Busted)')
        elif self.get_score(self.user) == 21:
            QMessageBox.about(self, 'Game Over', 'Congrat!!!! You win.\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))
        elif self.get_score(self.bot) == 21:
            QMessageBox.about(self, 'Game Over', 'You lose this round, time to prepaid!\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))
        else:
            if self.get_score(self.user) > self.get_score(self.bot):
                QMessageBox.about(self, 'Game Over', 'Congrat!!!! You win.\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))
            else:
                QMessageBox.about(self, 'Game Over', 'You lose this round, time to prepaid!\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))

        #if tie
        if self.get_score(self.user) == self.get_score(self.bot):
            QMessageBox.about(self, 'Game Over', 'Tie!!!!\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))

        #reset the game
        self.user = []
        self.bot = []
        self.bust = False
        self.current_player = 'user'
        self.logo.show()
        self.start_button.show()
        self.github_icon.show()
        self.hit_button.hide()
        self.stay_button.hide()

        # clear all the cards, idk why the fuck is not working??????
        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)



if __name__ == '__main__':
    app = QApplication([])
    window = GameWindow()
    window.show()

    app.exec_()