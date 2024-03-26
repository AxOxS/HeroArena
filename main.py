#Main failas, atsakingas už žaidimo pradžios ekraną, kuris leidžia žaidėjui pasirinkti ar jis nori pradėti naują žaidimą, ar tęsti jau pradėtą seniau.

#Importuojamos reikalingos funkcijos iš functions.py failo
from functions import start_new_game, start_new_round, load_game


#Kodo blokas, kuris pradeda vykdyti programą tik tada, kai ji yra paleidžiama tiesiogiai, o ne importuojama į kitus failus/scriptus.
if __name__ == "__main__":
    print("Welcome to the RPG Game!")
    
    #Input'o validacija, užtikrinanti, kad parenkamas teisingas variantas
    while True:
        print("1. New Game")
        print("2. Load Game")
        choice = input("Enter your choice: ")
        
        if choice in ("1", "2"):
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    #Pradedamas naujas žaidimas
    if choice == "1":
        start_new_game()
    
    #Tęsiamas senas žaidimas, jeigu toks yra. Jeigu žaidėjo arba priešų duomenys neegzistuoja, pradedamas naujas žaidimas.
    elif choice == "2":
        player1, enemies = load_game()
        if player1 is None or enemies is None:
            print("Starting new game instead.")
            start_new_game()
        else:
            start_new_round(player1, enemies)

