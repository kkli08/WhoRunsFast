from instances.BlackJack import BlackJack
from instances.WhoRunsFast import WhoRunsFast

def main():
    print("Welcome!")
    GameNumber = int(input("Enter 1 for Blackjack, or 2 for WhoRunsFast: "))
    while GameNumber not in [1, 2]:
        print("Invalid input! Enter 1 or 2.")
        GameNumber = int(input("Enter 1 for Blackjack, or 2 for WhoRunsFast: "))
    if GameNumber == 1:
        while True:
            print("Welcome to Blackjack!")
            game = BlackJack()
            game.start()

            print("Do you want to play again? (y/n)")
            answer = input().lower()
            while answer not in ["y", "n"]:
                print("Invalid input! Enter 'y' or 'n'.")
                answer = input().lower()

            if answer == "n":
                break
        print("Thanks for playing!")
    else:
        game = WhoRunsFast()

        while True:
            print("Welcome to WhoRunsFast!")
            game.play_game()
            game.continue_game()

main()