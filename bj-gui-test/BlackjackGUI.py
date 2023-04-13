from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QMessageBox, QWidget
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5 import QtTest
from instances.Stack import Stack
import random
import webbrowser
import time
import os, sys


#current is able to run through "python ./bj-gui-test/BlackjackGUI.py" & "python BlackjackGUI.py"
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#get the abs path of src/ and card_images/
src_path = os.path.join(path, 'src')
card_images_path = os.path.join(path, 'card_images')

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome!')
        self.setFixedSize(1920, 1080)

        #set icon
        self.setWindowIcon(QIcon(src_path+'/icon.png'))

        #set ./bg_images/bg.jpg as background
        self.bg = QLabel(self)
        self.bg.setPixmap(QPixmap(src_path+'/bg.jpg'))
        self.bg.setGeometry(0, 0, 1920, 1080)
        self.bg.setScaledContents(True)

        # Add logo to the beginning page
        logo_width, logo_height = 500, 250
        x = (1800 - logo_width) // 2
        y = (400 - logo_height) // 2
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(card_images_path+'/logo.png'))
        self.logo.setGeometry(x, y, logo_width, logo_height)  # Replace x, y, width, and height with desired values
        self.logo.setScaledContents(True)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_game)
        #keep the button on the top and fixed, center it
        self.start_button.setFixedSize(200, 100)
        self.start_button.move(800, 500)
        self.start_button.setParent(self)
        self.start_button.setCursor(Qt.PointingHandCursor)
        #set hover effect
        # self.start_button.setStyleSheet("QPushButton {background-color: initial;background-image: linear-gradient(-180deg, #00D775, #00BD68);border-radius: 5px;color: #FFFFFF;font-family: Inter,-apple-system,system-ui,Roboto,'Helvetica Neue',Arial,sans-serif;height: 44px;line-height: 44px;outline: 0;padding: 0 20px;position: relative;text-align: center;vertical-align: top;white-space: nowrap;width: 100%;border: 0;}")
        self.start_button.setStyleSheet("QPushButton:hover {color: #FFFFFF;background-color: #00BD68;}")

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

        #set ./src/huanledoudizhu.mp3 as background music
        # background music
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile('../src/huanledoudizhu.mp3')))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        # user victory sound
        self.playlist_victory = QMediaPlaylist()
        self.playlist_victory.addMedia(QMediaContent(QUrl.fromLocalFile('../src/victory.mp3')))
        self.playlist_victory.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)

        # user defeat sound
        self.playlist_lose = QMediaPlaylist()
        self.playlist_lose.addMedia(QMediaContent(QUrl.fromLocalFile('../src/defeat.mp3')))
        self.playlist_lose.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)

        
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.play()
        

        #this mediaplayer is for playing the shuffle sound
        self.player2 = QMediaPlayer()

        ########################### Game Attribute
        # Create a new card game
        self.game = Stack()

        # score for hand cards
        self.score_label = QLabel(self)
        self.score_label.setStyleSheet("color: white; font-size: 30px")
        self.score_label.setGeometry(600, 800, 100, 100)
        self.layout().addWidget(self.score_label)

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

    def closeEvent(self, event):
            reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Quit the application
                # QApplication.instance().quit()
                event.accept()  # accept the event
                os._exit(0)
            else:
                # Ignore the close event and keep the application running
                event.ignore()

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
            # if self.get_score(self.bot) < 17:
            #     self.bot_hit()
            # else:
            #     try_index = random.randint(1,10)
            #     if try_index <= 3 and self.get_score(self.bot) < 21:
            #         self.bot_hit()
            #     else:
            #         self.bot_stay()
            #         break

            # some changes to the bot strategy
            if self.get_score(self.bot) < 11:
                self.bot_hit()
            elif self.get_score(self.bot) < 17:
                if self.get_score(self.user) >= 14:
                    self.bot_hit()
                else:
                    self.bot_stay()
                    break
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
            os._exit(0)

        if event.key() == Qt.Key_H:
            #read the help.txt file
            with open(src_path+'/howToPlay.txt', 'rb') as f:
                help_text = f.read()
            help_text = help_text.decode('utf-8')
            #open a message box
            QMessageBox.about(self, 'Help', help_text)
        
        if event.key() == Qt.Key_B:
            #read the botStrategy.txt file
            with open(src_path+'/botStrategy.txt', 'rb') as f:
                help_text = f.read()
            help_text = help_text.decode('utf-8')
            
            #open a message box
            QMessageBox.about(self, 'Help', help_text)
  

    
    def display_face(self,player):
        #display the card at the position (x,y)
        for i in range(len(player)):
            card = QLabel(self)
            card.setPixmap(QPixmap(card_images_path+'/'+str(player[i].value)+'_of_'+player[i].suit+'.png').scaled(200, 245, Qt.KeepAspectRatio))
            #resize the image to 100*150 and keep the card at the bottom of the window
            card.setGeometry(600 + i*50, 900, 200, 245)
            self.layout().addWidget(card)

    def clear_face(self):
        #clear the card at the position (x,y)
        for i in range(len(self.user)):
            card = QLabel(self)
            card.setPixmap(QPixmap(card_images_path+'/back2.png').scaled(200, 245, Qt.KeepAspectRatio))
            #resize the image to 100*150 and keep the card at the bottom of the window
            card.setGeometry(600 + i*50, 900, 200, 245)
            self.layout().addWidget(card)
    
    #function to check bot cards in order to debug
    def display_bot_face(self,player):
        #display the card at the position (x,y)
        for i in range(len(player)):
            card = QLabel(self)
            card.setPixmap(QPixmap(card_images_path+'/'+str(player[i].value)+'_of_'+player[i].suit+'.png').scaled(200, 245, Qt.KeepAspectRatio))
            #resize the image to 100*150 and keep the card at the bottom of the window
            card.setGeometry(600 + i*50, 50, 200, 245)
            self.layout().addWidget(card)

    def clear_bot_face(self):
        #clear the card at the position (x,y)
        for i in range(len(self.bot)):
            card = QLabel(self)
            card.setPixmap(QPixmap(card_images_path+'/back2.png').scaled(200, 245, Qt.KeepAspectRatio))
            #resize the image to 100*150 and keep the card at the bottom of the window
            card.setGeometry(600 + i*50, 50, 200, 245)
            self.layout().addWidget(card)

    def display_back(self,player):
        #display the card at the position (x,y)
        #the card should be display as image in card_images/back2.png
        for i in range(len(player)):
            card = QLabel(self)
            card.setPixmap(QPixmap(card_images_path+'/back2.png').scaled(200, 245, Qt.KeepAspectRatio))
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
        # Calculate the score of the player
        score = self.get_score(hand)
        # Update the text of the score_label
        self.score_label.setText(str(score))

    

    def play_shuffle_music(self):
        """
        This is not working as well
        """
        media_content = QMediaContent(QUrl.fromLocalFile(src_path+'/shuffle.mp3'))

        self.player2.setMedia(media_content)
        #speed up the media
        self.player2.playbackRate = 2
        self.player2.setVolume(100)

        self.player.play()

    def play_victory_music(self):
        # set the media content and url for the victory music file
        path = '../src/victory.mp3'
        print(path)
        media_content = QMediaContent(QUrl.fromLocalFile(path))
        # set the media content to the media player
        self.player.setMedia(media_content)
        # play the victory music
        self.player.play()

    def play_defeat_music(self):
        path = '../src/defeat.mp3'
        print(path)
        # set the media content and url for the victory music file
        media_content = QMediaContent(QUrl.fromLocalFile(path))
        # set the media content to the media player
        self.player.setMedia(media_content)
        # play the victory music
        self.player.play()

    
    def end(self):
        #pause the current background music
        self.player.pause()
        #Display the result as message box
        if self.bust and self.current_player == 'user':
            # play the defeat music
            self.player.setPlaylist(self.playlist_lose)
            self.player.play()
            # self.play_defeat_music()
            QMessageBox.about(self, 'Game Over', 'Bust!!!! You lose.\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))
        elif self.bust and self.current_player == 'bot':
            # play the victory music
            self.player.setPlaylist(self.playlist_victory)
            self.player.play()
            # self.play_victory_music()
            QMessageBox.about(self, 'Game Over', 'Congrat!!!! You win.\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot))+'(Busted)')
        elif self.get_score(self.user) == 21:
            # play the victory music
            self.player.setPlaylist(self.playlist_victory)
            self.player.play()
            # self.play_victory_music()
            QMessageBox.about(self, 'Game Over', 'Congrat!!!! You win.\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))
        elif self.get_score(self.bot) == 21:
            # play the defeat music
            self.player.setPlaylist(self.playlist_lose)
            self.player.play()
            # self.play_defeat_music()
            QMessageBox.about(self, 'Game Over', 'You lose this round, bot wins!\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))
        else:
            if self.get_score(self.user) > self.get_score(self.bot):
                # play the victory music
                self.player.setPlaylist(self.playlist_victory)
                self.player.play()
                # self.play_victory_music()
                QMessageBox.about(self, 'Game Over', 'Congrat!!!! You win.\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))
            else:
                # self.play_defeat_music()
                self.player.setPlaylist(self.playlist_lose)
                self.player.play()
                QMessageBox.about(self, 'Game Over', 'You lose this round, bot wins!\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))

        #if tie
        if self.get_score(self.user) == self.get_score(self.bot):
            # play the victory music
            self.player.setPlaylist(self.playlist_victory)
            self.player.play()
            QMessageBox.about(self, 'Game Over', 'Tie!!!!\nYour score:'+str(self.get_score(self.user))+'\nBot\'s score:'+str(self.get_score(self.bot)))


        # ask the user if they want to play again
        reply = QMessageBox.question(self, 'Message', 'Do you want to play again?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            #reset the game (This part is messed up)
            # bgm restart
            self.player.setPlaylist(self.playlist)
            self.player.play()
            # clear the cards
            self.clear_bot_face()
            self.clear_face()

            # Create a new card game
            self.game = Stack()

            # Create a new player
            self.user = []
            self.bot = []

            self.user_score = 0
            self.bot_score = 0

            self.bust = False

            self.current_player = 'user'

            self.start_game()
        else:
            #close the game
            os._exit(0)



if __name__ == '__main__':
    app = QApplication([])
    window = GameWindow()
    window.show()

    sys.exit(app.exec_())
    
