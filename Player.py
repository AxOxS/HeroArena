from SpellCasting import SpellCasting
from InventoryManager import InventoryManager
from Character import Character

class Player(Character, SpellCasting, InventoryManager):
    def __init__(self, name, health, mana, level=1):
        Character.__init__(self, name, health, mana, level)
        SpellCasting.__init__(self)
        InventoryManager.__init__(self)
        self.experience = 0
        
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