#Failas, skirtas pagalbinėm funkcijom, neįeinančiom į klases, kaip metodai.

#Importuojami reikalingi moduliai
import json, random, os
from Player import Player
from Enemy import Enemy
from util import *

#Funkcija, skirta išsaugoti žaidimą. Funkcija priima žaidėjo ir priešų sąrašus, išsaugo juos JSON faile. Dabartinėje žaidimo stadijoje, arba veikėjas įveikia visus round'o priešus ir išsaugant žaidimą, priešų
#sąrašas bus tuščias, paruoštas naujiems priešams, arba žaidėjas pralaimi ir savegame yra ištrinamas. Ateityje galima padaryti, kad būtų galima išsaugoti žaidimą midstate, kad žaidėjas
#galėtų tęsti žaidimą iš tos vietos, kur sustojo vidury round'o. Tada enemies išsaugojimas bus naudingas. Dabar iš jo naudos nėra.
def save_game(player, enemies):
    #Folderis, kuriame bus saugomi json failai
    save_dir = "data"
    #Sukuriamas, nurodytas folderis, jeigu jis neegzistuoja. Jeigu failas jau egzistuoja - nebus jokio error'o, nes yra nurodytas exist_ok=True argumentas.
    os.makedirs(save_dir, exist_ok=True)
    #Sukuriamas išsaugojimo path (kelias iki išsaugojimo failo/directory, nurodomas json failo pavadinimas)
    save_path = os.path.join(save_dir, "savegame.json")
    
    #Standartinė rašymo į failą procedūra, nurodant kokį failą atidaryti rašymo režime.
    #Sukuriamas save_data dictionary, kuriame yra žaidėjo ir priešų sąrašų duomenys, paversti į dictionary formatą, kad būtų galima išsaugoti JSON faile.
    #Žaidėjas vienas, todėl jis yra tiesiog paverčiamas į dictionary su to_dict metodu. Priešai yra sąrašas, todėl jie yra paverčiami į dictionary sąrašą,
    #naudojant for ciklą.
    with open(save_path, "w") as file:
        save_data = {
            "player": player.to_dict(),
            "enemies": [enemy.to_dict() for enemy in enemies]
        }
        #naudojama json dump() funkcija, kuri išsaugo dictionary į JSON failą, nurodant failą ir indent argumentus. Šiuo atveju, kiekviena indentacija bus 4 tarpų dydžio
        json.dump(save_data, file, indent=4)
    print("Game saved!")
 

#Funkcija, skirta užkrauti išsaugoto žaidėjo profilio informaciją, kad žaidimas galėtų būti tęsiamas.
#Nurodomas skaitomo failo path ir bandoma atidaryti nurodytą failą skaitymo režime. Jeigu failas neegzistuoja - išvedamas pranešimas, kad save game nerastas.
#Neradus save game - grąžinami None, None. Funkcija aptikusi, kad veikėjas arba priešai yra None - inicijuoja naujo žaidimo pradžią. 
def load_game():
    save_path = "data/savegame.json"
    
    try:
        with open(save_path, "r") as file:
            #Naudojant json load funkciją, nuskaitomas JSON failas ir paverčiamas į dictionary formatą, kad būtų galima naudoti žaidimo duomenys tinkamu formatu.
            save_data = json.load(file)
            #Naudojant from_dict metodą, iš grąžintos savegame informacijos sukuriamas žaidėjo objektas.
            player = Player.from_dict(save_data["player"])
            #Kadangi round'e priešų būna ne vienas - juos saugosime sąraše.
            #Kad populatinti sąrašą priešų klasės objektais - naudosime for ciklą visiems priešams iš savegame gauti.
            enemies = []
            if 'enemies' in save_data:
                enemies = [Enemy.from_dict(enemy_data) for enemy_data in save_data["enemies"]]
        print("Game loaded!")
        return player, enemies
    except FileNotFoundError:
        print("No save game found.")
        return None, None

#Standartinė informacijos surinkimo funkcija, naudojanti input validation, kad būtų galima sukurti veikėją su tinkamais atributais.
#Funkcija nepraleis netinkamos informacijos ir lauks, kol tinkami duomenys bus įvesti.   
def create_character():
    print("Create Your Character")
    
    while True:
        name = input("Enter character name: ")
        if name.strip():
            break
        else:
            print("Name cannot be empty.")
    
    while True:
        try:
            health = int(input("Enter health points: "))
            if health > 0:
                break
            else:
                print("Health points must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    
    while True:
        try:
            mana = int(input("Enter mana points: "))
            if mana > 0:
                break
            else:
                print("Mana points must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    
    #Praėjus input validation sėkmingai - sukuriamas naujas Player objektas, naudojant įvestus duomenis.
    return Player(name, health, mana)

#Kadangi, kiekvienas naujas round'as turės naujus priešus - reikia sukurti funkciją, kuri sugeneruotų atsitiktinį priešų sąrašą iš JSON failo.
#Funkcija priima vieną argumentą - num_enemies, kuris nurodo kiek priešų bus sugeneruota.
#Funkcija atidaro JSON failą, nuskaito priešų duomenis ir iš jų sugeneruoja num_enemies atsitiktinių priešų sąrašą.    
def get_random_enemies(num_enemies):
    with open("data/enemies.json", "r") as file:
        enemy_data = json.load(file)
        #.sample() - funkcija iš random modulio, kuri sugeneruoja atsitiktinį sąrašą iš duoto sąrašo, nurodytu kiekiu.
        enemies_data = random.sample(enemy_data["enemies"], num_enemies)
        return enemies_data

#Tęsinys iš get_random_enemies funkcijos. Funkcija parenka atsitiktinai priešų skaičių nuo 1 iki 5 ir juos parenka su get_random_enemies funkcija.
def create_enemies():
    num_enemies = random.randint(1, 5)
    enemies_data = get_random_enemies(num_enemies)
    #Naudojant for ciklą (list comprehension) - iteratinama per kiekvieną enemy dictionary iš enemies_data.
    #Kiekvienas enemy dictionary yra paverčiamas į Enemy objektą ir grąžinamas bendrame sąraše.
    return [Enemy(enemy["name"], enemy["health"], enemy["mana"], enemy["damage"], enemy["defense"], enemy["level"]) for enemy in enemies_data]

#Funkcija, kuri nubraižo ir pavaizduoja pagrindinę žaidimo informaciją. Žaidėjo informaciją, žaidėjo daiktus ir priešų informaciją.
def display_status(player, enemies):
    print("\n" + "=" * 35 + " Status " + "=" * 35)
    print(f"\n{player.name} (Level {player.level}): Health: {player.health}/{player.max_health}, Mana: {player.mana}/{player.max_mana}, Experience: {player.get_experience()}/{player.level * 100}\n")
    print("Inventory:")
    for item, quantity in player.inventory.items():
        print(f"{item}: {quantity}")
    print("\nEnemies:")
    for enemy in enemies:
        print(f"{enemy.name} (Level {enemy.level}): Health: {enemy.health}/{enemy.max_health}")
    print("\n" + "=" * 78 + "\n")
    
def start_new_game():
    player1 = create_character()
    enemies = create_enemies()
    start_new_round(player1, enemies)


def start_new_round(player1, enemies):
    enemies = create_enemies()
    
    #Ciklas vykdomas tol, kol žaidėjas arba bent vienas priešas yra gyvi.
    while player1.health > 0 and any(enemy.health > 0 for enemy in enemies):
        #Kiekvieno ciklo pradžioje - išvalomas ekranas, kad būtų galima matyti tik dabartinę informaciją.
        os.system('cls' if os.name == 'nt' else 'clear')
        display_status(player1, enemies)
        
        #Veikėjo eilės meniu. Kiekvienas input praeina validation, kad būtų išvengiama errorų ir parenkama tiksli informacija.
        print("\n" + "=" * 20 + " Player's Turn " + "=" * 20)
        print("Choose your action:")
        print("1: Attack")
        print("2: Cast Spell")
        print("3: Use Item")
        
        while True:
            choice = input("Enter your choice: ")
            if choice in ["1", "2", "3"]:
                break
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")
        
        #Atakuojant - parenkamas atsitiktinis priešas iš priešų sąrašo. Jeigu priešas yra negyvas - jis yra ištrinamas iš sąrašo ir žaidėjas gauna 50 xp.        
        if choice == "1":
            target = random.choice(enemies)
            player1.attack(target)
            if target.health <= 0:
                #print_running_info(f"{target.name} has been defeated!")
                enemies.remove(target)
                player1.gain_experience(50)
        elif choice == "2":
            print("Choose a spell:")
            #iteratinam per spells dictionary keys iš key ir value porų, iš žaidėjo objekto ir išvedam kiekvieną spell pavadinimą su jo numeriu.
            for i, spell in enumerate(player1.spells.keys(), 1):
                print(f"{i}: {spell}")
            #Input validation, kad būtų išvengta errorų ir parenkama tiksli informacija.
            while True:
                spell_choice = input("Enter your choice: ")
                if spell_choice.isdigit() and 1 <= int(spell_choice) <= len(player1.spells):
                    break
                else:
                    print("Invalid choice! Please enter a valid spell number.")
            
            #1. player1.spells.keys() - ištraukiamas "view objektas" keys iš spells dictionary žaidėjo objekte.
            #2. list() - paverčia keys view objektą į sąrašą, kad būtų galima pasiekti keys pagal indeksą.
            #3. [int(spell_choice) - 1] - parenkamas konkretus spell pagal indeksą, atitinkantį žaidėjo įvestį (-1 nes indeksuojama nuo 0)       
            spell_name = list(player1.spells.keys())[int(spell_choice) - 1]
            #Veikėjas panaudoja burtą, parenkant atsitiktinį priešą iš priešų sąrašo.
            target = random.choice(enemies)
            player1.cast_spell(target, spell_name)
            if target.health <= 0:
                #print_running_info(f"{target.name} has been defeated!")
                enemies.remove(target)
                player1.gain_experience(50)
        elif choice == "3":
            print("Choose an item:")
            #iteratinam per item dictionary keys iš key ir value porų, iš žaidėjo objekto ir išvedam kiekvieną item pavadinimą su jo numeriu.
            for i, item in enumerate(player1.inventory.keys(), 1):
                print(f"{i}: {item}")
            
            #Input validation, kad būtų išvengta errorų ir parenkama tiksli informacija.    
            while True: 
                item_choice = input("Enter your choice: ")
                if item_choice.isdigit() and 1 <= int(item_choice) <= len(player1.inventory):
                    break
                else:
                    print("Invalid choice! Please enter a valid item number.")
            #1. player1.inventory.keys() - ištraukiamas "view objektas" keys iš inventory dictionary žaidėjo objekte.
            #2. list() - paverčia keys view objektą į sąrašą, kad būtų galima pasiekti keys pagal indeksą.
            #3. [int(item_choice) - 1] - parenkamas konkretus spell pagal indeksą, atitinkantį žaidėjo įvestį (-1 nes indeksuojama nuo 0)           
            item_name = list(player1.inventory.keys())[int(item_choice) - 1]
            player1.use_item(item_name)
        
        #Įveikus visus priešus - išvedamas pranešimas ir break'inama iš ciklo.
        if not enemies:
            print_running_info("You have defeated all the enemies!")
            break

        #Priešų eilė. Pradžioje - išvalomas ekranas, kad būtų galima matyti tik dabartinę informaciją.
        os.system('cls' if os.name == 'nt' else 'clear')
        display_status(player1, enemies)
        print("\n" + "=" * 20 + " Enemies' Turn " + "=" * 20)
        #Kiekvienas priešas atakuoja žaidėją ir po kiekvienos atakos tikrinama ar žaidėjas dar gyvas.
        for enemy in enemies:
            enemy.attack(player1)
            if player1.health <= 0:
                print_running_info(f"{player1.name} has been defeated!")
                break
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 20 + " Round Over " + "=" * 20)
    #Jeigu žaidėjas pralaimi - išvedamas pranešimas ir ištrinamas savegame. Kadangi žaidimo principas toks, jog turi vieną gyvybę. Miršti - turi pradėti iš naujo.
    if player1.health <= 0:
        print_running_info("You have been defeated!")
        save_path = "data/savegame.json"
        if os.path.exists(save_path):
            os.remove(save_path)
            print_running_info("Save game deleted.")
    else:
        print("Round ended.")
        #Jeigu žaidėjas gyvas - leidžiama pasirinkti ar jis nori pradėti naują round'ą ar baigti žaidimą šiam kartui.
        while True:
            choice = input("Do you want to start another round? (yes/no): ")
            if choice in ["yes", "no"]:
                break
            else:
                print("Invalid choice! Please enter 'yes' or 'no'.")
        
        #Pagal pasirinkimą arba pradedamas naujas roundas su naujais priešais, arba išsaugojamas žaidimas ir programa baigia darbą.       
        if choice == "yes":
            start_new_round(player1, get_random_enemies(random.randint(1, 5)))
        else:
            print("\n" + "=" * 20 + " Game Over " + "=" * 20)
            print("Thanks for playing!")
            save_game(player1, enemies)
