# import random
# import time

# class Character:
#     def __init__(self, name, health, level=1):
#         self.name = name
#         self.health = health
#         self.level = level
#         self.status_effects = []

#     def attack(self, target):
#         damage = random.randint(1, 1000) * self.level
#         print(f"{self.name} attacks {target.name} for {damage} damage!")
#         target.take_damage(damage)

#     def take_damage(self, damage):
#         self.health -= damage
#         print(f"{self.name} takes {damage} damage. {self.name}'s health: {self.health}")
#         if self.health <= 0:
#             print(f"{self.name} has been defeated!")
#             del self

#     def apply_status_effect(self, effect):
#         self.status_effects.append(effect)
#         print(f"{self.name} is now affected by {effect}!")

#     def remove_status_effect(self, effect):
#         if effect in self.status_effects:
#             self.status_effects.remove(effect)
#             print(f"{self.name} is no longer affected by {effect}.")

#     def level_up(self):
#         self.level += 1
#         self.health += 10
#         print(f"{self.name} leveled up to level {self.level}!")


# class Player(Character):
#     def __init__(self, name, health, mana, level=1):
#         super().__init__(name, health, level)
#         self.mana = mana
#         self.experience = 0
#         self.spells = {"Fireball": {"damage": (10, 20), "mana_cost": 10},
#                        "Heal": {"heal_amount": (10, 20), "mana_cost": 10}}

#     def cast_spell(self, target, spell_name):
#         if spell_name in self.spells:
#             spell = self.spells[spell_name]
#             if self.mana >= spell["mana_cost"]:
#                 self.mana -= spell["mana_cost"]
#                 if "damage" in spell:
#                     damage = random.randint(*spell["damage"]) * self.level
#                     print(f"{self.name} casts {spell_name} on {target.name} for {damage} damage!")
#                     target.take_damage(damage)
#                 elif "heal_amount" in spell:
#                     heal_amount = random.randint(*spell["heal_amount"])
#                     print(f"{self.name} casts {spell_name} on themselves, healing {heal_amount} HP!")
#                     self.health = min(self.health + heal_amount, 100)  # Ensure health does not exceed 100
#             else:
#                 print("Not enough mana to cast this spell!")
#         else:
#             print("Invalid spell!")

#     def gain_experience(self, exp):
#         self.experience += exp
#         print(f"{self.name} gained {exp} experience points!")
#         if self.experience >= self.level * 100:
#             self.level_up()


# class Enemy(Character):
#     def __init__(self, name, health, damage, level=1):
#         super().__init__(name, health, level)
#         self.damage = damage

#     def attack(self, target):
#         damage = random.randint(1, 10) * self.level
#         print(f"{self.name} attacks {target.name} for {damage} damage!")
#         target.take_damage(damage)
#         if random.random() < 0.2:  # 20% chance to apply a status effect
#             self.apply_status_effect("Poison")
#             target.remove_status_effect("Poison")  # Demonstration purpose: remove the effect immediately


# class Item:
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description

#     def use(self, target):
#         pass  # Placeholder for item usage


# # User Interface
# def display_status(player, enemies):
#     print("\n" + "=" * 20 + " Status " + "=" * 20)
#     print(f"{player.name} (Level {player.level}): Health: {player.health}, Mana: {player.mana}, Experience: {player.experience}/{player.level * 100}")
#     print("Enemies:")
#     for enemy in enemies:
#         print(f"{enemy.name} (Level {enemy.level}): Health: {enemy.health}")
#     print("=" * 48 + "\n")


# # Instantiate player and enemy objects
# player1 = Player("Hero", 100, 50)
# enemies = [Enemy("Goblin", 50, 8), Enemy("Skeleton", 70, 12)]

# # Gameplay loop
# while player1.health > 0 and any(enemy.health > 0 for enemy in enemies):
#     display_status(player1, enemies)
#     time.sleep(1)  # Introducing a slight delay for better readability

#     # Player's turn
#     print("\n" + "=" * 20 + " Player's Turn " + "=" * 20)
#     print("Choose your action:")
#     print("1: Attack")
#     print("2: Cast Spell")
#     choice = input("Enter your choice: ")
#     if choice == "1":
#         target = random.choice(enemies)
#         player1.attack(target)
#         if target.health <= 0:
#             print(f"{target.name} has been defeated!")
#             enemies.remove(target)
#             player1.gain_experience(50)
#     elif choice == "2":
#         print("Choose a spell:")
#         for i, spell in enumerate(player1.spells.keys(), 1):
#             print(f"{i}: {spell}")
#         spell_choice = input("Enter your choice: ")
#         if spell_choice.isdigit() and 1 <= int(spell_choice) <= len(player1.spells):
#             spell_name = list(player1.spells.keys())[int(spell_choice) - 1]
#             target = random.choice(enemies)
#             player1.cast_spell(target, spell_name)
#             if target.health <= 0:
#                 print(f"{target.name} has been defeated!")
#                 enemies.remove(target)
#                 player1.gain_experience(50)
#         else:
#             print("Invalid choice!")
#     else:
#         print("Invalid choice! You wasted your turn.")

#     if not enemies:
#         print("All enemies have been defeated!")
#         break

#     # Enemies' turn
#     print("\n" + "=" * 20 + " Enemies' Turn " + "=" * 20)
#     for enemy in enemies:
#         enemy.attack(player1)
#         if player1.health <= 0:
#             print(f"{player1.name} has been defeated!")
#             break

# # Game over
# print("\n" + "=" * 20 + " Game Over " + "=" * 20)
# print("Thanks for playing!")

import random
import time

class Character:
    def __init__(self, name, health, mana, level=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.level = level
        self.status_effects = []
        self.damage = 10
        self.defense = 5

    def attack(self, target):
        damage = max(0, random.randint(self.damage - 3, self.damage + 3) - target.defense)
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} takes {damage} damage. {self.name}'s health: {self.health}/{self.max_health}")
        if self.health <= 0:
            print(f"{self.name} has been defeated!")
            del self

    def apply_status_effect(self, effect):
        if effect not in self.status_effects:
            self.status_effects.append(effect)
            print(f"{self.name} is now affected by {effect}!")
            if effect == "Poison":
                print(f"{self.name} takes damage from poison!")
                self.take_damage(random.randint(5, 10))

    def remove_status_effect(self, effect):
        if effect in self.status_effects:
            self.status_effects.remove(effect)
            print(f"{self.name} is no longer affected by {effect}.")

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.max_mana += 5
        self.mana = self.max_mana
        self.damage += 2
        self.defense += 1
        print(f"{self.name} leveled up to level {self.level}!")


class Player(Character):
    def __init__(self, name, health, mana, level=1):
        super().__init__(name, health, mana, level)
        self.experience = 0
        self.spells = {"Fireball": {"damage": (15, 25), "mana_cost": 15, "cooldown": 3},
                       "Heal": {"heal_amount": (15, 25), "mana_cost": 15, "cooldown": 3}}
        self.inventory = {"Health Potion": 3, "Mana Potion": 3}

    def cast_spell(self, target, spell_name):
        if spell_name in self.spells:
            spell = self.spells[spell_name]
            if self.mana >= spell["mana_cost"]:
                if spell_name not in self.status_effects:
                    self.mana -= spell["mana_cost"]
                    if "damage" in spell:
                        damage = max(0, random.randint(*spell["damage"]) - target.defense)
                        print(f"{self.name} casts {spell_name} on {target.name} for {damage} damage!")
                        target.take_damage(damage)
                    elif "heal_amount" in spell:
                        heal_amount = random.randint(*spell["heal_amount"])
                        print(f"{self.name} casts {spell_name} on themselves, healing {heal_amount} HP!")
                        self.health = min(self.health + heal_amount, self.max_health)
                    self.apply_status_effect(spell_name)
                    print(f"{self.name}'s {spell_name} is on cooldown for {spell['cooldown']} turns.")
                else:
                    print(f"{self.name}'s {spell_name} is still on cooldown!")
            else:
                print("Not enough mana to cast this spell!")
        else:
            print("Invalid spell!")

    def use_item(self, item_name, target):
        if item_name in self.inventory:
            if self.inventory[item_name] > 0:
                if item_name == "Health Potion":
                    heal_amount = random.randint(20, 30)
                    print(f"{self.name} uses {item_name}, healing {heal_amount} HP!")
                    self.health = min(self.health + heal_amount, self.max_health)
                elif item_name == "Mana Potion":
                    restore_amount = random.randint(20, 30)
                    print(f"{self.name} uses {item_name}, restoring {restore_amount} mana!")
                    self.mana = min(self.mana + restore_amount, self.max_mana)
                self.inventory[item_name] -= 1
            else:
                print("You don't have any more of that item!")
        else:
            print("Invalid item!")

    def gain_experience(self, exp):
        self.experience += exp
        print(f"{self.name} gained {exp} experience points!")
        if self.experience >= self.level * 100:
            self.level_up()


class Enemy(Character):
    def __init__(self, name, health, mana, damage, defense, level=1):
        super().__init__(name, health, mana, level)
        self.damage = damage
        self.defense = defense

    def attack(self, target):
        damage = max(0, random.randint(self.damage - 3, self.damage + 3) - target.defense)
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)
        if random.random() < 0.2:  # 20% chance to apply a status effect
            self.apply_status_effect("Poison")
            target.remove_status_effect("Poison")  # Demonstration purpose: remove the effect immediately


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, target):
        pass  # Placeholder for item usage


# User Interface
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


# Instantiate player and enemy objects
player1 = Player("Hero", 100, 50)
enemies = [Enemy("Goblin", 50, 30, 8, 3), Enemy("Skeleton", 70, 20, 12, 5)]

# Gameplay loop
while player1.health > 0 and any(enemy.health > 0 for enemy in enemies):
    display_status(player1, enemies)
    time.sleep(1)  # Introducing a slight delay for better readability

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
            print("Invalid choice!")
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
        print("Invalid choice! You wasted your turn.")

    if not enemies:
        print("All enemies have been defeated!")
        break

    # Enemies' turn
    print("\n" + "=" * 20 + " Enemies' Turn " + "=" * 20)
    for enemy in enemies:
        enemy.attack(player1)
        if player1.health <= 0:
            print(f"{player1.name} has been defeated!")
            break

# Game over
print("\n" + "=" * 20 + " Game Over " + "=" * 20)#Lunos darbas: 0999999999999999999999999999999999999999999999999oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
print("Thanks for playing!")




