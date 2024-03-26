import json, random, time, os
from Player import Player
from Enemy import Enemy

def save_game(player, enemies):
    save_dir = "data"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "savegame.json")
    
    with open(save_path, "w") as file:
        save_data = {
            "player": player.to_dict(),
            "enemies": [enemy.to_dict() for enemy in enemies]
        }
        json.dump(save_data, file, indent=4)
    print("Game saved!")
    
def load_game():
    save_path = "data/savegame.json"
    
    try:
        with open(save_path, "r") as file:
            save_data = json.load(file)
            player = Player.from_dict(save_data["player"])
            enemies = []
            if 'enemies' in save_data:
                enemies = [Enemy.from_dict(enemy_data) for enemy_data in save_data["enemies"]]
        print("Game loaded!")
        return player, enemies
    except FileNotFoundError:
        print("No save game found.")
        return None, None
    
def create_character():
    print("Create Your Character")
    name = input("Enter character name: ")
    health = int(input("Enter health points: "))
    mana = int(input("Enter mana points: "))
    return Player(name, health, mana)
    
def get_random_enemies(num_enemies):
    with open("data/enemies.json", "r") as file:
        enemy_data = json.load(file)
        enemies_data = random.sample(enemy_data["enemies"], num_enemies)
        return enemies_data

def display_status(player, enemies):
    print("\n" + "=" * 20 + " Status " + "=" * 20)
    print(f"{player.name} (Level {player.level}): Health: {player.health}/{player.max_health}, Mana: {player.mana}/{player.max_mana}, Experience: {player.experience}/{player.level * 100}")
    print("Inventory:")
    for item, quantity in player.inventory.items():
        print(f"{item}: {quantity}")
    print("Enemies:")
    for enemy in enemies:
        print(f"{enemy.name} (Level {enemy.level}): Health: {enemy.health}/{enemy.max_health}")
    print("=" * 48 + "\n")
    
def start_new_game():
    player1 = create_character()
    num_enemies = random.randint(1, 5)
    enemies_data = get_random_enemies(num_enemies)
    enemies = [Enemy(enemy["name"], enemy["health"], enemy["mana"], enemy["damage"], enemy["defense"], enemy["level"]) for enemy in enemies_data]
    start_new_round(player1, enemies)
    
def start_new_round(player1, enemies):
    num_enemies = random.randint(1, 5)
    enemies_data = get_random_enemies(num_enemies)
    enemies = [Enemy(enemy["name"], enemy["health"], enemy["mana"], enemy["damage"], enemy["defense"], enemy["level"]) for enemy in enemies_data]
    
    while player1.health > 0 and any(enemy.health > 0 for enemy in enemies):
        display_status(player1, enemies)
        time.sleep(1)
        # Player's turn
        print("\n" + "=" * 20 + " Player's Turn " + "=" * 20)
        print("Choose your action:")
        print("1: Attack")
        print("2: Cast Spell")
        print("3: Use Item")
        choice = input("Enter your choice: ")
        if choice == "1":
            target = random.choice(enemies)
            player1.attack(target)
            if target.health <= 0:
                print(f"{target.name} has been defeated!")
                enemies.remove(target)
                player1.gain_experience(50)
        elif choice == "2":
            print("Choose a spell:")
            for i, spell in enumerate(player1.spells.keys(), 1):
                print(f"{i}: {spell}")
            spell_choice = input("Enter your choice: ")
            if spell_choice.isdigit() and 1 <= int(spell_choice) <= len(player1.spells):
                spell_name = list(player1.spells.keys())[int(spell_choice) - 1]
                target = random.choice(enemies)
                player1.cast_spell(target, spell_name)
                if target.health <= 0:
                    print(f"{target.name} has been defeated!")
                    enemies.remove(target)
                    player1.gain_experience(50)
            else:
                print("Invalid choice.")
        elif choice == "3":
            print("Choose an item:")
            for i, item in enumerate(player1.inventory.keys(), 1):
                print(f"{i}: {item}")
            item_choice = input("Enter your choice: ")
            if item_choice.isdigit() and 1 <= int(item_choice) <= len(player1.inventory):
                item_name = list(player1.inventory.keys())[int(item_choice) - 1]
                player1.use_item(item_name, player1)
            else:
                print("Invalid choice!")
        else:
            print("Invalid choice!")

        if not enemies:
            print("You have defeated all the enemies!")
            break

        # Enemies' turn
        print("\n" + "=" * 20 + " Enemies' Turn " + "=" * 20)
        for enemy in enemies:
            enemy.attack(player1)
            if player1.health <= 0:
                print(f"{player1.name} has been defeated!")
                break
                        
    print("\n" + "=" * 20 + " Round Over " + "=" * 20)
    print("Round ended.")
    choice = input("Do you want to start another round? (yes/no): ")
    if choice.lower() == "yes":
        start_new_round(player1, get_random_enemies(random.randint(1, 5)))
    else:
        print("\n" + "=" * 20 + " Game Over " + "=" * 20)
        print("Thanks for playing!")
        save_game(player1, enemies)