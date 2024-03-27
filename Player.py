#Player klasė - Character (pagrinde), SpellCasting ir InventoryManager superklasių subklasė, t.y, paveldi šių klasių savybes ir metodus.
#Iš esmės subklasės labai naudingos kuriant jau egzistuojančios klasės specializuotus atvejus (kaip šitoje situacijoje, veikėjų klasė turi specializuotas savo subklases, 
#priešų ir žaidėjo.) Šios klasės turi daug panašių savybių, kurias paveldi iš Character superklasės, bet, tuo pačiu, ir savo unikalių savybių, kurios jas išskiria iš kitų klasių.
#Player klasė skirta veikėjo objektui/instancijai sukurti. Veikėjas turi savo gyvybes, maną, lygį, patirtį, burtus, inventorių...

#Importuojamos reikiamos klasės, funkcijos ir moduliai
from SpellCasting import SpellCasting
from InventoryManager import InventoryManager
from Character import Character
from util import print_running_info

#Kaip ir kitose klasėse, Player klasė pradeda nuo konstruktoriaus, kuris automatiškai iškviečiamas, kai sukuriamas naujas žaidėjo objektas. Konstruktorius nurodo, kokias savybes
#turi turėti žaidėjas, kai jis yra sukurtas.
#Kadangi Player klasė paveldi ne iš vienos superklasės, o iš trijų (daugybinis paveldėjimas), vietoj super() funkcijos, tiesiogiai iškviečiami superklasių konstruktoriai
#Veikėjas savo pagrindines savybes ir metodus paveldi iš Character superklasės, o burtų ir inventoriaus savybes ir metodus paveldi iš SpellCasting ir InventoryManager klasių.

#Kadangi šitos savybės jau yra aprašomos superklasėje - jų nereikia aprašyti subklasėje, nes jos automatiškai paveldėjamos). _experience savybė yra private tipo, nes ji yra unikali žaidėjui ir
#nereikia, kad būtų prieinama tiesiogiai iš išorės (be get/set metodo).

#Kadangi pitono kalba, priešingai nei kitos, neturi stiprių reguliacijų dėl private/public/restricted savybių,
#tai šis private žymėjimas su _ žodžio pradžioje yra tik simbolinis ir padeda programuotojui suprasti, kad ši savybė yra private tipo ir geriau su ja nesielgti, kaip su public savybe.
class Player(Character, SpellCasting, InventoryManager):
    def __init__(self, name, health, mana, level=1):
        Character.__init__(self, name, health, mana, level)
        SpellCasting.__init__(self)
        InventoryManager.__init__(self)
        self._experience = 0  # Private attribute prefixed with underscore

    #getteris, naudojamas atvaizduoti žaidėjo xp functions faile (seterio šioje situacijoje nereikia, tuo pasirūpina gain_experience metodas)
    def get_experience(self):
        return self._experience

    #Metodas, kuris prideda xp žaidėjui, kai jis kažką padaro (pvz. nugali priešą).
    #xp padidinamas nurodytu kiekiu, atspausdinama informacija apie tai ir jeigu pasiektas lygio pakėlimo kriterijus - žaidėjui pakyla lygis ir xp nustatomas į 0. 
    def gain_experience(self, amount):
        self._experience += amount
        print_running_info(f"{self.name} gains {amount} experience!")
        if self._experience >= 100 * self.level:
            self.level_up()
            self._experience = 0

    #Žaidėjo to_dict metodas, kuris paverčia žaidėjo objektą į dictionary, kad būtų galima jį išsaugoti JSON faile.
    #Naudojam superklasės Character to_dict metodą, kad būtų išsaugotos pagrindinės savybės, o po to pridedamos unikalios šiai klasei savybės.   
    def to_dict(self):
        data = super().to_dict()
        data["experience"] = self._experience
        data["spells"] = self.spells
        data["inventory"] = self.inventory
        return data

    #@classmethod dekoratorius naudojamas, apibrežiant from_dict metodą, kuris veikia kaip pačios klasės metodas, o ne objekto instancijos (Kadangi šitas metodas atsakingas už instancijų kūrimą).
    #Šioje vietoje naudojam @classmethod, nes from_dict bus naudojamas, kaip konstruktorius, kuris sukuria naują objektą iš dictionary.
    
    #Kadangi naudojam @classmethod - nereikia klasės instancijos (self). Instancija kuriama iš pateiktos metodui informacijos. Todėl vietoj self (klasės objektas/instancija),
    #kaip argumentas, duodamas cls (atstovaujantis pačią klasę, o ne jos instanciją). Taip iškviestas klasės metodas automatiškai priima klasę, kaip pirmąjį argumentą, suteikdamas galimybę kurti naujus objektus
    #ar naudoti kitus metodus, kuriems reikia klasės, o ne instancijos.
    #Mūsų atveju šitas klasės metodas, inicijuoja klasės konstruktorių ir kuria naują žaidėjo objektą pagal duotą dictionary data iš JSON failo.
    @classmethod
    def from_dict(cls, data):
        player = super().from_dict(data)
        player._experience = data["experience"]
        player.spells = data["spells"]
        player.inventory = data["inventory"]
        return player
