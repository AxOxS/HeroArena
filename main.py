from functions import start_new_game, start_new_round, load_game

if __name__ == "__main__":
    print("Welcome to the RPG Game!")
    print("1. New Game")
    print("2. Load Game")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        start_new_game()
    elif choice == "2":
        player1, enemies = load_game()
        if player1 is None or enemies is None:
            print("Starting new game instead.")
            start_new_game()
        else:
            start_new_round(player1, enemies)
    else:
        print("Invalid choice.")

