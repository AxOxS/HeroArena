import random
from util import print_running_info

class InventoryManager:
    def __init__(self):
        self.inventory = {"Health Potion": 3, "Mana Potion": 3}
        
    def use_item(self, item_name, target):
        if item_name in self.inventory:
            if self.inventory[item_name] > 0:
                if item_name == "Health Potion":
                    heal_amount = random.randint(20, 30)
                    print_running_info(f"{self.name} uses a Health Potion, healing {heal_amount} HP!")
                    self.health = min(self.health + heal_amount, self.max_health)
                elif item_name == "Mana Potion":
                    restore_amount = random.randint(20, 30)
                    print_running_info(f"{self.name} uses a Mana Potion, restoring {restore_amount} MP!")
                    self.mana = min(self.mana + restore_amount, self.max_mana)
                self.inventory[item_name] -= 1
            else:
                print_running_info(f"{self.name} does not have any {item_name} left!")
        else:
            print_running_info(f"{self.name} does not have the item {item_name}!")
