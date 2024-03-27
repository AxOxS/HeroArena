#InventoryManager klasė/brėžinys, inkapsuliacijos principu valdo žaidėjo inventory (Prie inventory data prieinam use_item metodu). Ši klasė nėra nei super, nei sub klasė, o
#tiesiog atskira klasė, kuria naudojasi Player klasė.

#Importuojami reikalingi moduliai
import random
from util import print_running_info

#Klasė, su kiekviena nauja Player objekto instancija, automatiškai priskirianti žaidėjui 10 gyvybės ir 10 manos eleksyrų {dictionary, kadangi šioje vietoje labai patogu
# apsirašyti itemus key-value poromis "pavadinimas-kiekis"}, naudojant konstruktorių.
#Konstruktoriaus kviesti nereikia, jis automatiškai iškviečiamas, kai sukuriamas naujas objektas. Argumente konstruktorius ir kiti moduliai visada turi turėti
#self, nes kuriant naują objekto instanciją - pats objektas pirma automatiškai kviečiamas, kaip argumentas. Be self, konstruktorius ar kiti moduliai neveiks.
class InventoryManager:
    def __init__(self):
        self.inventory = {"Health Potion": 10, "Mana Potion": 10}
        
    #Metodas, per kurį prieinama prie žaidėjo inventory. Metodas priima daikto pavadinimą, kaip argumentą.
    def use_item(self, item_name):
        #Kad būtų galima naudoti daiktą, pirma patikrinama ar jis yra žaidėjo inventoriuje {dictionary}. Jeigu if'as True - tikrinam ar daikto kiekis didesnis už 0.
        #Jei ir šis if'as True - tikrinama ar daiktas yra Health Potion, ar Mana Potion ir atliekam atitinkamus veiksmus su jais
        #Inventory metodą galima praplėsti, kad kiekvienai žaidėjo instancijai skirtų random du itemus iš didelio itemų sąrašo, saugomo json faile (kaip su priešais). Bet dabar
        #užteks ir dviejų daiktų, kurių naudojimą galima aprašyti trumpai ir švariai.
        if item_name in self.inventory:
            if self.inventory[item_name] > 0:
                if item_name == "Health Potion":
                    #Kiekvieną kartą, kai naudojamas Health/Mana potion, Gyvybės arba Manos kiekis atstatomas atsitiktinai tarp 10 ir 1000. Tai prideda azarto.
                    #Informacija apie veiksmus su eleksyrais išvedama į ekraną naudojant savo parašytą spausdinimo funkciją, kuri leidžia matyti tekstą realiuoju laiku, taip
                    #padidinant žaidimo interaktyvumą ir užtikrinant, kad nebūtų per daug informacijos vienu metu.
                    heal_amount = random.randint(10, 1000)
                    print_running_info(f"{self.name} uses a Health Potion, healing {heal_amount} HP!")
                    #Žaidėjo instancijos health kintamasis atstatomas iki tiek, kiek pagydo eleksyras, bet ne daugiau nei max hp.
                        #1. Apskaičiuojama kiek išviso gyvybių po atstatymo: self.health + heal_amount
                        #2. Naudojant min funkciją, užtikrinam, kad gyvybės po atstatymo neviršytų maksimalių galimų gyvybių. (jeigu po atstatymo 150, o max gyvybės 100 - gyvybės
                        # bus nustatytos į 100, o ne 150)
                    self.health = min(self.health + heal_amount, self.max_health)
                #Tas pats principas, kaip su Health Potion, tik šį kartą atstatoma mana.
                elif item_name == "Mana Potion":
                    restore_amount = random.randint(10, 1000)
                    print_running_info(f"{self.name} uses a Mana Potion, restoring {restore_amount} MP!")
                    self.mana = min(self.mana + restore_amount, self.max_mana)
                #Po kiekvieno eleksyro naudojimo, eleksyras yra pašalinamas iš žaidėjo inventoriaus. Šiuo metu nėra jokio būdo atstatyti eleksyrų, žaidėjo sukūrimo instancijos metu,
                #skiriama 10 eleksyrų, todėl žaidėjas turi juos naudoti atsargiai, nes, pasibaigus eleksyrams - nebegalės su jais atstatyti savo HP ar MP.
                #Tačiau atstatymui yra or kitų būdų, kituose metoduose. (Ateityje būtų galima įvesti loot sistema, kur priešai išmeta random drop'us, arba pinigų sistemą, kur veikėjas gali
                # pirkti itemus už pinigus, kuriuos laimėjo prieš priešus ar gavo pasikėlęs lygį).
                self.inventory[item_name] -= 1
            else:
                print_running_info(f"{self.name} does not have any {item_name} left!")
        else:
            print_running_info(f"{self.name} does not have the item {item_name}!")