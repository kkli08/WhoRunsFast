from instances.BlackJack import BlackJack
from instances.WhoRunsFast import WhoRunsFast
# while True:
#     print("Welcome to Blackjack!")
#     game = BlackJack()
#     game.start()

#     print("Do you want to play again? (y/n)")
#     answer = input().lower()
#     while answer not in ["y", "n"]:
#         print("Invalid input! Enter 'y' or 'n'.")
#         answer = input().lower()

#     if answer == "n":
#         break

# print("Thanks for playing!")

def main():
    game = WhoRunsFast()

    while True:
        print("Welcome to WhoRunsFast!")
        game.play_game()
        game.continue_game()

main()