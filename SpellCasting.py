#SpellCasting klasė inkapsuliacijos principu (datos ir metodu "surišimas" su klase. Inkapsuliuoti metodai, duomenys, prieinami tik per klasės objektą, tai padeda išvengti netyčinių
#duomenų pakeitimų, ar metodų iškvietimų, kurie gali sugadinti programos veikimą. Ši klasė nėra nei super, nei sub klasė, o tiesiog atskira klasė, kurią naudoja Player klasė.)

#Importuojami reikalingi moduliai
import random
from util import print_running_info

#Klasė, su kiekviena nauja Player objekto instancija, automatiškai priskirianti žaidėjui 2 burtus (konstruktoriumi): Fireball ir Heal {dictionary, kur key-value poros yra burtų pavadinimai ir dar 
#papildomi dictionary (kaip value), kurių key-value poros yra burtų savybės, kaip žala, manos kaina ir cooldown periodas, kiek kartų nebus galima naudoti burto po panaudojimo}. 

#Ateityje būtų galima padaryti, kaip su Enemies klase, kur burtų sąrašas būtų saugomas json faile, o ne būtų hardcoded į klasės konstruktorių.
#Su kiekvienu lygio pasikėlimu ar iš burtų parduotuvės, veikėjas galėtų gauti naują burtą su skirtingomis savybėmis ir panaudojimo galimybėmis.

#Konstruktoriaus kviesti nereikia, jis automatiškai iškviečiamas, kai sukuriamas naujas objektas. Argumente konstruktorius ir kiti moduliai visada turi turėti
#self, nes kuriant naują objekto instanciją - pats objektas pirma automatiškai kviečiamas, kaip argumentas. Be self, konstruktorius ar kiti moduliai neveiks.
class SpellCasting:
    def __init__(self):
        self.spells = {"Fireball": {"damage": (100, 1000), "mana_cost": 20, "cooldown": 3},
                       "Heal": {"heal_amount": (1, 100), "mana_cost": 20, "cooldown": 3}}
    
    #Metodas, per kurį panaudojamas burtas. Metodas priima burto 'taikinį' ir burto pavadinimą, kaip argumentus.
    #Pirma vyksta tikrinimai, ar pasirinktas burtas yra žaidėjo burtų sąraše (dictionary), ar žaidėjas turi pakankamai manos iškviesti pasirinktą burtą ir ar
    #pasirinktas burtas nėra cooldown'e (po paskutinio panaudojimo praėjo bent trys ėjimai).
    
    #Praėjus visus tikrinimus - nuskaitoma veikėjo mana burto panaudojimui ir atliekami veiksmai pagal burtą: atakuoti ar gydyti. 
    def cast_spell(self, target, spell_name):
        if spell_name in self.spells:
            spell = self.spells[spell_name]
            if self.mana >= spell["mana_cost"]:
                if spell_name not in self.status_effects:
                    self.mana -= spell["mana_cost"]
                    
                    if "damage" in spell:
                        #Nustatoma, kiek žalos padarys burtas:
                            #1. random.randint(*spell["damage"]) - randamas atsitiktinis skaičius tarp nurodytų ribų "damage tupl'e" (* - operatorius šioje situacijoje
                            #išskleidžia tupl'ą į du atskirus argumentus, kurie yra perduodami funkcijai random.randint (min ir max))
                            
                            #2.Iš gauto atsitiktinio skaičiaus atimama priešo defense reikšmė, kad būtų nustatyta kiek tiksliai žalos padarys burtas.
                            
                            #3. max(0, ...) - užtikrina, kad žala priešui nebus neigiama. Jeigu priešo ginyba didesnė už atsitiktinę žalą - žala bus 0, o ne -n.
                        #Naudojant custom print'ą - išvedama burto eigos informacija žaidėjui ir priešui priskiriama suteikta žala.
                        damage = max(0, random.randint(*spell["damage"]) - target.defense)
                        print_running_info(f"{self.name} casts {spell_name} on {target.name} for {damage} damage!")
                        target.take_damage(damage)
                    elif "heal_amount" in spell:
                        #Panašus principas, kaip gydimas su eleksyru per InventoryManager klasę: Nustatome kiek gyvybių atstatys burtas, išpakuodami gyvybių atstatymo ribas iš
                        #spell["heal_amount"] tuplo.
                        #Atspausdinama informacija apie gydymą ir atstatoma gyvybės kiekis, bet ne daugiau nei maksimalus galimas gyvybių kiekis.
                        heal_amount = random.randint(*spell["heal_amount"])
                        print_running_info(f"{self.name} casts {spell_name} on themselves, healing {heal_amount} HP!")
                        self.health = min(self.health + heal_amount, self.max_health)
                    #Po burto panaudojimo, jeigu burtas turi cooldown'ą - jis priskiriamas status_effect'ui, kuris neleidžia panaudoti burto tolimesnį nurodytą laikotarpį.
                    self.apply_status_effect(spell_name)
                    print_running_info(f"{self.name}'s {spell_name} is on cooldown for {spell['cooldown']} turns.")
                else:
                    print_running_info(f"{self.name}'s {spell_name} is still cooldown!")
            else:
                print_running_info(f"{self.name} does not have enough mana to cast {spell_name}!")
        else:
            print_running_info(f"{self.name} does not know the spell {spell_name}!")