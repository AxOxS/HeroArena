#Enemy klasė - Character superklasės subklasė, t.y, paveldi Character klasės savybes ir metodus.
#Iš esmės subklasės labai naudingos kuriant jau egzistuojančios klasės specializuotus atvejus (kaip šitoje situacijoje, veikėjų klasė turi specializuotas savo subklases, 
#priešų ir žaidėjo.) Šios klasės turi daug panašių savybių, kurias paveldi iš Character superklasės, bet, tuo pačiu, ir savo unikalių savybių, kurios jas išskiria iš kitų klasių.
#Enemy klasė skirta priešų instancijų objektams, su kuriais žaidėjas kovoja. Priešai turi savo gyvybes, maną, lygį, žalos ir gynybos reikšmes.

#Importuojami reikalingi moduliai, klassės ir funkcijos
from Character import Character
import random
from util import print_running_info

#Kaip ir kitose klasėse, Enemy klasė pradeda nuo konstruktoriaus, kuris automatiškai iškviečiamas, kai sukuriamas naujas priešo objektas. Konstruktorius nurodo, kokias savybes
#turi turėti priešas, kai jis yra sukurtas.
#Konstruktoriuje, naudojant super() funkciją, iškviečiamas superklasės konstruktorius, kuris priskiria priešui pagrindines savybes, kaip vardą, gyvybes, maną ir lygį. (Kadangi
# šitos savybės jau yra aprašomos superklasėje - jų nereikia aprašyti subklasėje, nes jos automatiškai paveldėjamos). Damage ir defense savybės, kad ir yra subklasėje - jas vis tiek
# reikia nurodyti, nes jos yra unikalios šiai klasei. (Superklasėje jos yra hardcodintos, kur šioje klasėje jos yra unikalios kiekvienam priešui). Tuo pačiu jas padarysime private tipo, 
#kad jos būtų prieinamos tik šiai klasei. (Tai padeda išvengti netyčinių duomenų pakeitimų, kurie gali sugadinti programos veikimą).

#Kadangi pitono kalba, priešingai nei kitos, neturi stiprių reguliacijų dėl private/public/restricted savybių,
#tai šis private žymėjimas su _ žodžio pradžioje yra tik simbolinis ir padeda programuotojui suprasti, kad ši savybė yra private tipo ir geriau su ja nesielgti, kaip su public savybe.
class Enemy(Character):
    def __init__(self, name, health, mana, damage, defense, level = 1):
        super().__init__(name, health, mana, level)
        self._damage = damage #Private savybės, kurios yra prieinamos tik šiai klasei.
        self._defense = defense #Private savybės, kurios yra prieinamos tik šiai klasei.
    
    #Kadangi priešus su šitais atributais gaunu tiesiogiai iš JSON failo, juos sugeneruodamas random - getter ir setter metodai nėra būtini, bet juos palieku ateičiai,
    #jeigu būtų tokia reikiamybė tiesiogiai prieiti prie šių atributų.
    
    # Getter damage metodas
    def get_damage(self):
        return self._damage
    
    # Setter damage metodas
    def set_damage(self, damage):
        self._damage = damage
    
    #Getter defense metodas
    def get_defense(self):
        return self._defense
    
    # Setter defense metodas
    def set_defense(self, defense):
        self._defense = defense    
    
    #Priešo atakos metodas, kuris priima target kaip argumentą. Priešas atakuoja target ir atima atsitiktinę žalą tarp damage-3 ir damage+3
    # (+/- 3, kad būtų daugiau kintamumo, atsitiktinumo tarp atakų žalos)
    #Iš apskaičiuotos random žalos atimamas target gynybos lygis, kad būtų nustatyta tikra žala, kurią priešas padarys targetui. (Jeigu gynyba didesnė už ataką - žala bus 0), užtikrinam,
    #kad žala nebus neigiama, naudodami max(0, ...) funkciją.    
    def attack(self, target):
        damage = max(0, random.randint(self._damage - 3, self._damage + 3) - target.get_defense())
        print_running_info(f"{self.name} attacks {target.name} for {damage} damage!")
        #Žalos davimas užtikrinamas naudojant metodą iš superklasės.
        target.take_damage(damage)
        #Extra punktas: Priešas turi 20% šansą užkrėsti targetą nuodais. Jeigu target'as jau yra užkrėstas nuodais - nuodai yra pašalinami iš target'o.
        if random.random() < 0.2:
            self.apply_status_effect("Poison")
            target.remove_status_effect("Poison")
    
    #Priešo to_dict metodas, kuris paverčia priešo objektą į dictionary, kad būtų galima jį išsaugoti JSON faile.
    #Naudojam superklasės to_dict metodą, kad būtų išsaugotos pagrindinės savybės, o po to pridedamos unikalios šiai klasei savybės.        
    def to_dict(self):
        data = super().to_dict()
        data["damage"] = self._damage
        data["defense"] = self._defense
        return data
    
    #@classmethod dekoratorius naudojamas, apibrežiant from_dict metodą, kuris veikia kaip pačios klasės metodas, o ne objekto instancijos (Kadangi šitas metodas atsakingas už instancijų kūrimą).
    #Šioje vietoje naudojam @classmethod, nes from_dict bus naudojamas, kaip konstruktorius, kuris sukuria naują objektą iš dictionary.
    
    #Kadangi naudojam @classmethod - nereikia klasės instancijos (self). Instancija kuriama iš pateiktos metodui informacijos. Todėl vietoj self (klasės objektas/instancija),
    #kaip argumentas, duodamas cls (atstovaujantis pačią klasę, o ne jos instanciją). Taip iškviestas klasės metodas automatiškai priima klasę, kaip pirmąjį argumentą, suteikdamas galimybę kurti naujus objektus
    #ar naudoti kitus metodus, kuriems reikia klasės, o ne instancijos.
    #Mūsų atveju šitas klasės metodas, inicijuoja klasės konstruktorių ir kuria naujus priešų objektus pagal duotą dictionary data iš JSON failo.
    @classmethod
    def from_dict(cls, data):
        enemy = super().from_dict(data)
        enemy._damage = data["damage"]
        enemy._defense = data["defense"]
        return enemy