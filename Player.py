import random
from Character import Character

class Player(Character):
    def __init__(self, name, health, mana, level = 1):
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
                    print(f"{self.name}'s {spell_name} is still cooldown!")
            else:
                print(f"{self.name} does not have enough mana to cast {spell_name}!")
        else:
            print(f"{self.name} does not know the spell {spell_name}!")
            
    def use_item(self, item_name, target):
        if item_name in self.inventory:
            if self.inventory[item_name] > 0:
                if item_name == "Health Potion":
                    heal_amount = random.randint(20, 30)
                    print(f"{self.name} uses a Health Potion, healing {heal_amount} HP!")
                    self.health = min(self.health + heal_amount, self.max_health)
                elif item_name == "Mana Potion":
                    restore_amount = random.randint(20, 30)
                    print(f"{self.name} uses a Mana Potion, restoring {restore_amount} MP!")
                    self.mana = min(self.mana + restore_amount, self.max_mana)
                self.inventory[item_name] -= 1
            else:
                print(f"{self.name} does not have any {item_name} left!")
        else:
            print(f"{self.name} does not have the item {item_name}!")
    
    def gain_experience(self, amount):
        self.experience += amount
        print(f"{self.name} gains {amount} experience!")
        if self.experience >= 100 * self.level:
            self.level_up()
            
    def to_dict(self):
        data = super().to_dict()
        data["experience"] = self.experience
        data["spells"] = self.spells
        data["inventory"] = self.inventory
        return data
    
    @classmethod
    def from_dict(cls, data):
        player = super().from_dict(data)
        player.experience = data["experience"]
        player.spells = data["spells"]
        player.inventory = data["inventory"]
        return player