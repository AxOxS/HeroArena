import random
from util import print_running_info

class SpellCasting:
    def __init__(self):
        self.spells = {"Fireball": {"damage": (15, 25), "mana_cost": 15, "cooldown": 3},
                       "Heal": {"heal_amount": (15, 25), "mana_cost": 15, "cooldown": 3}}
        
    def cast_spell(self, target, spell_name):
        if spell_name in self.spells:
            spell = self.spells[spell_name]
            if self.mana >= spell["mana_cost"]:
                if spell_name not in self.status_effects:
                    self.mana -= spell["mana_cost"]
                    if "damage" in spell:
                        damage = max(0, random.randint(*spell["damage"]) - target.defense)
                        print_running_info(f"{self.name} casts {spell_name} on {target.name} for {damage} damage!")
                        target.take_damage(damage)
                    elif "heal_amount" in spell:
                        heal_amount = random.randint(*spell["heal_amount"])
                        print_running_info(f"{self.name} casts {spell_name} on themselves, healing {heal_amount} HP!")
                        self.health = min(self.health + heal_amount, self.max_health)
                    self.apply_status_effect(spell_name)
                    print_running_info(f"{self.name}'s {spell_name} is on cooldown for {spell['cooldown']} turns.")
                else:
                    print_running_info(f"{self.name}'s {spell_name} is still cooldown!")
            else:
                print_running_info(f"{self.name} does not have enough mana to cast {spell_name}!")
        else:
            print_running_info(f"{self.name} does not know the spell {spell_name}!")