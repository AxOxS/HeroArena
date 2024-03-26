#Funkcija, atsakinga už teksto išvedimo į ekraną atsiradimo greitį. Taip žaidimas tampa interaktyvesnis ir įdomesnis.
#Kai tekstas neatsiranda visas vienu metu - nesijaučia taip lyg būtų per daug informacijos vienu metu.

#importuojami reikalingi moduliai
import time

#Funkcija priima string'ą kaip argumentą, kuris yra išskaidomas į atskirus simbolius, charus,
#kurie yra išvedami į ekraną su 0.05 sekundžių intervalu.    
def print_running_info(text):
    for line in text.split("\n"):
        for char in line:
            #printas spausdina kiekvieną simbolį iš eilės, po simbolio nepradėdanas naujos eilutės.
            #Visi simobliai spausdinami vienas po kito, nelaukiant kol buferis užsipildys iki tam tikros ribos (Šioje situacijoje, jeigu buferis būtų aktyvus - 
            # sistema palauktų, kol visa eilutė simbolių užsikrautų ir tik tada parodytų ją vartotojui. Todėl apeinam buferį, kad galėtume matytu spausdinimą realiuoju laiku).
            print(char, end = "", flush = False)
            time.sleep(0.05)
        #Kai eilutės simboliai išspausdinti, spausdinama nauja eilutė.
        print()