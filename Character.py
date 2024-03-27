#Galima sakyti, kad ši klasė - pagrindinė šitos programos klasė, superklasė, pagal kurią subklasės kuria veikėjų objektus (priešus ir žaidėją).

#importuojami reikalingi moduliai
import random
from util import print_running_info

#Šios klasės objekto instancijos metu - iškviečiamas konstruktorius, pagal kurį sukuriamas naujas objektas su nurodytomis savybėmis.
#Argumente konstruktorius ir kiti moduliai visada turi turėti self, nes kuriant naują objekto instanciją - 
#pats objektas pirma automatiškai kviečiamas, kaip argumentas. Be self, konstruktorius ar kiti moduliai neveiks.
class Character:
    #Jeigu būtų poreikis - galima argumente nurodyti reikiamus reikšmių tipus, pvz name:str, health:int ir tt...
    #Tuo pačiu galima naudoti assert, kad būtų patikrinta, ar reikšmės yra teisingo tipo, pvz assert isinstance(name, str), assert isinstance(health, int) ir tt...
    #Bet data validation apsiima skirtingos funkcijos ir metodai, kurie yra aprašyti kituose moduliuose. 
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
    
    #Metodas, kuris nuskaičiuoja nurodytą žalą iš žaidėjo gyvybių. Jeigu žalos kiekis didesnis nei žaidėjo gyvybės - žaidėjo gyvybės nustatomos į 0.
    def take_damage(self, damage):
        self.health -= damage
        print_running_info(f"{self.name} takes {damage} damage. {self.name}'s health: {self.health}/{self.max_health}")
        if self.health <= 0:
            print_running_info(f"{self.name} has been defeated!")
    
    #Atakos metodas, kuris priima target kaip argumentą. Atakuojamas target ir atimama atsitiktinė žala tarp damage-3 ir damage+3
    #(+/- 3, kad būtų daugiau kintamumo, atsitiktinumo tarp atakų žalos)
    #Iš apskaičiuotos random žalos atimamas target gynybos lygis, kad būtų nustatyta tikra žala, kurią priešas padarys targetui. (Jeigu gynyba didesnė už ataką - žala bus 0), užtikrinam,
    #kad žala nebus neigiama, naudodami max(0, ...) funkciją.        
    def attack(self, target):
        damage = max(0, random.randint(self.damage - 3, self.damage + 3) - target.defense)
        print_running_info(f"{self.name} attacks {target.name} for {damage} damage!")
        #Nuskaičiuojama žala targetui, naudojant target objekto take_damage metodą.
        target.take_damage(damage)
    
    #Metodas, kuris prideda status_effect'ą prie veikėjo. Status_effect'ai yra būsenos, kurios veikia veikėją tam tikrą laiką, arba tol, kol jie yra pašalinami.
    #Pirma vyksta tikrinimas ar status_effect'as jau nėra pridėtas prie veikėjo. Jeigu status_effect'as nėra pridėtas - jis pridedamas prie veikėjo ir išvedama informacija apie tai.
    #Jei status_effect'as yra nuodai - veikėjas kiekvieną eilę praranda tam tikrą gyvybių kiekį.
    
    #Šiuo metu yra tik vienas status_effect'as - nuodai, bet ateityje būtų galima pridėti daugiau status_effect'ų, kurie veiktų skirtingai ir turėtų skirtingus poveikius veikėjui.
    def apply_status_effect(self, effect):
        if effect not in self.status_effects:
            self.status_effects.append(effect)
            print_running_info(f"{self.name} is now affected by {effect}!")
            if effect == "Poison":
                print_running_info(f"{self.name} takes damage from poison!")
                self.take_damage(random.randint(1, 100))
    
    #Metodas, kuris pašalina status_effect'ą iš veikėjo. Jeigu status_effect'as yra veikėjo status_effect'ų sąraše - jis pašalinamas ir išvedama informacija apie tai.            
    def remove_status_effect(self, effect):
        if effect in self.status_effects:
            self.status_effects.remove(effect)
            print_running_info(f"{self.name} is no longer affected by {effect}!")
    
    #Metodas, skirtas veikėjo instancijos/objekto lygio pakėlimui. Kiekvieną kartą, kai veikėjas pakelia lygį - jo gyvybės, mana, žala ir gynyba padidinamos.    
    def level_up(self):
        self.level += 1
        self.max_health += 25
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.damage += 5
        self.defense += 5
        print_running_info(f"{self.name} has leveled up to level {self.level}!")
    
    #Veikėjo objektas su visais savo atributais yra paverčiamas į dictionary (informacija saugoma key-value poromis), kad būtų galima jį išsaugoti JSON faile.    
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
    
    #@classmethod dekoratorius naudojamas, apibrežiant from_dict metodą, kuris veikia kaip pačios klasės metodas, o ne objekto instancijos (Kadangi šitas metodas atsakingas už instancijų kūrimą).
    #Šioje vietoje naudojam @classmethod, nes from_dict bus naudojamas, kaip konstruktorius, kuris sukuria naują objektą iš dictionary.
    
    #Kadangi naudojam @classmethod - nereikia klasės instancijos (self). Instancija kuriama iš pateiktos metodui informacijos. Todėl vietoj self (klasės objektas/instancija),
    #kaip argumentas, duodamas cls (atstovaujantis pačią klasę, o ne jos instanciją). Taip iškviestas klasės metodas automatiškai priima klasę, kaip pirmąjį argumentą, suteikdamas galimybę kurti naujus objektus
    #ar naudoti kitus metodus, kuriems reikia klasės, o ne instancijos.
    
    #Mūsų atveju šitas klasės metodas, inicijuoja klasės konstruktorių ir leidžia atkurti veikėjo objektą iš gautų duomenų.
        #1. Kuriamas naujas Character objektas: Metodas pradžioje sukuria naują Character objektą, naudodamas perduotus duomenis.
        
        #2. Perduodami duomenys iš žodyno į objekto atributus: Kiekviena key-value pora iš pateikto žodyno yra priskiriama naujam objektui kaip atributas.
        # Tai užtikrina, kad naujai sukurto objekto savybės būtų nustatytos pagal gautus duomenis.

        #3. Sukurtas naujas objektas grąžinamas: Galiausiai, sukurtas naujas Character objektas, turintis visas savybes ir duomenis, kurie buvo nurodyti žodyne,
        # yra grąžinamas iš metodo kaip rezultatas.
    @classmethod    
    def from_dict(cls, data):
        return cls(
            data["name"], 
            data["health"], 
            data["mana"], 
            data["level"])
    
    #Destruktorius, kuris iškviečiamas, kai objektas yra sunaikinamas. Kadangi objektai yra sunaikinami automatiškai pitono garbage collectoriaus, kai jie nebereikalingi, destruktorius nėra būtinas.
    #Bet jį palikau, kadangi užduotyje buvo punktas apie destruktorius    
    def __del__(self):
        pass
    
    #Getter metodas, kuris grąžina veikėjo ginybą. Specifiškai naudojamas Enemy klasėje priešo gynybos lygiui gauti attack metode, kuris POLIMORFIŠKAI perrašomas, kad atitiktų priešo poreikius.
    def get_defense(self):
        return self.defense