import random
from util import print_running_info

class Character:
    def __init__(self, name, health, mana, level = 1):
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.level = level
        self.status_effects = []
        self.damage = 1000
        self.defense = 5
    
    def take_damage(self, damage):
        self.health -= damage
        print_running_info(f"{self.name} takes {damage} damage. {self.name}'s health: {self.health}/{self.max_health}")
        if self.health <= 0:
            print_running_info(f"{self.name} has been defeated!")
            del self
        
    def attack(self, target):
        damage = max(0, random.randint(self.damage - 3, self.damage + 3) - target.defense)
        print_running_info(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)
        
    def apply_status_effect(self, effect):
        if effect not in self.status_effects:
            self.status_effects.append(effect)
            print_running_info(f"{self.name} is now affected by {effect}!")
            if effect == "Poison":
                print_running_info(f"{self.name} takes damage from poison!")
                self.take_damage(random.randint(1, 10))
                
    def remove_status_effect(self, effect):
        if effect in self.status_effects:
            self.status_effects.remove(effect)
            print_running_info(f"{self.name} is no longer affected by {effect}!")
            
    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.max_mana += 5
        self.mana = self.max_mana
        self.damage += 2
        self.defense += 1
        print_running_info(f"{self.name} has leveled up to level {self.level}!")
        
    def to_dict(self):
        return {
            "name": self.name, 
            "health": self.health, 
            "max_health": self.max_health,
            "mana": self.mana, 
            "max_mana": self.max_mana, 
            "level": self.level,
            "status_effects": self.status_effects, 
            "damage": self.damage, 
            "defense": self.defense
        }
    
    @classmethod    
    def from_dict(cls, data):
        return cls(
            data["name"], 
            data["health"], 
            data["mana"], 
            data["level"])
        
    def __del__(self):
        pass