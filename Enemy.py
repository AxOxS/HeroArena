from Character import Character
import random
from util import print_running_info

class Enemy(Character):
    def __init__(self, name, health, mana, damage, defense, level = 1):
        super().__init__(name, health, mana, level)
        self.damage = damage
        self.defense = defense
        
    def attack(self, target):
        damage = max(0, random.randint(self.damage - 3, self.damage + 3) - target.defense)
        print_running_info(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)
        if random.random() < 0.2:
            self.apply_status_effect("Poison")
            target.remove_status_effect("Poison")
            
    def to_dict(self):
        data = super().to_dict()
        data["damage"] = self.damage
        data["defense"] = self.defense
        return data
    
    @classmethod
    def from_dict(cls, data):
        enemy = super().from_dict(data)
        enemy.damage = data["damage"]
        enemy.defense = data["defense"]
        return enemy