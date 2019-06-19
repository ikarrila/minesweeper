import random
import haravasto
import datetime
import time
import winsound

#Pelaajalle tulostettu kenttä ja todellinen kenttä tallennetaan tänne
tila = {
    "kentta": None,
    "tulostettu_kentta": None,
    "pelattu" : False,
}

#Käytettävissä olevat hiiren näppäimet
NAPIT = {
    1 : "vasen",
    2 : "keski",
    4 : "oikea",
}

#Peliasetukset ja pelin tilanne
ASETUKSET = {
    "leveys" : 0,
    "korkeus" : 0,
    "miinoja" : 0,
    "avattu" : False,
    "lippuja" : 0,
    "klikkaukset" : 0,
    "aloitus_aika" : None,
    "paljastettu" : False,
}

#Miinaharavan päävalikko
def valikko():
    print("\nTervetuloa pelaamaan miinaharavaa!", "(U)usi peli", "(T)ulokset", "(L)opeta",
    sep = "\n")
    while True:
        syote = input("Tee valintasi: ").lower()
        if syote == "u" or syote == "uusi" or syote == "uusi peli":
            uusipeli()
        elif syote == "t" or syote == "tulokset":
            tulokset()
        elif syote == "l" or syote == "lopeta":
            print("Näkemiin!")
            quit()
        else:
            print("Valintaa ei ole olemassa")

#Aloitetaan uusi peli, nollataan asetukset ja kysytään uusia syötteitä
def uusipeli():
    #Palautetaan oletusasetukset
    ASETUKSET["avattu"] = False
    ASETUKSET["paljastettu"] = False
    ASETUKSET["lippuja"] = 0
    ASETUKSET["klikkaukset"] = 0
    ASETUKSET["leveys"] = 0
    ASETUKSET["korkeus"] = 0
    ASETUKSET["miinoja"] = 0
    while True:

        #Kysytään pelaajalta syötteitä joiden pohjalta pelikenttä luodaan
        try:
            while ASETUKSET["leveys"] > 30 or ASETUKSET["leveys"] < 2:
                ASETUKSET["leveys"] = int(input("Anna kentän leveys kokonaislukuna välillä 2-30: "))
                if ASETUKSET["leveys"] > 30:
                    print("Liian leveä kenttä!")
                elif ASETUKSET["leveys"] < 2:
                    print("Liian kapea kenttä!")
            while ASETUKSET["korkeus"] > 20 or ASETUKSET["korkeus"] < 2:
                ASETUKSET["korkeus"] = int(input("Anna kentän korkeus kokonaislukuna välillä 2-20: "))
                if ASETUKSET["korkeus"] > 20:
                    print("Liian korkea kenttä! Mahtuisiko edes ruudulle?")
                elif ASETUKSET["leveys"] < 2:
                    print("Liian matala kenttä!")
            while ASETUKSET["miinoja"] <= 0 or ASETUKSET["miinoja"] >= (ASETUKSET["leveys"]*ASETUKSET["korkeus"]):
                ASETUKSET["miinoja"] = int(input("Anna miinojen lukumäärä välillä 0-{}: "
                .format((ASETUKSET["leveys"]*ASETUKSET["korkeus"]-1))))
                if ASETUKSET["miinoja"] >= (ASETUKSET["leveys"]*ASETUKSET["korkeus"]):
                    print("Liian paljon miinoja!")
                elif ASETUKSET["miinoja"] <= 0:
                    print("Liian vähän miinoja!")
        except ValueError or TypeError:
            print("Kokonaislukuna kiitos")
        else:
            #Luodaan kenttä, piilotetaan miinat ja asetetaan aloitusaika
            luokentta()
            piilotamiinat()
            ASETUKSET["aloitus_aika"] = time.time()
            main()

#Ladataan edellisten pelien tulokset, jos mahdollista
def tulokset():
    try:
        tiedosto = open("miinaharavan_tulokset.txt", "r")
        print("\n" + tiedosto.read())
        print("(U)usi peli", "(T)ulokset", "(L)opeta", sep = "\n")
    except FileNotFoundError:
        print("Tiedoston avaaminen epäonnistui")

#Siirretään miinaa satunnaiseen tyhjään ruutuun
def siirramiinaa(y, x):
    a = x
    b = y
    tila["kentta"][y][x] = " "
    while a == x or b == y and tila["kentta"][b][a] != " ":
        a = random.randint(0, len(tila["kentta"][0]) - 1)
        b = random.randint(0, len(tila["kentta"]) - 1)
    tila["kentta"][b][a] = "x"

#Tarkistetaan onko siirto ensimmäinen ja määritetään tappio tai siirretään miinaa
def maaritakuolema(y, x, avattu):
    if tila["kentta"][y][x] == "x":
        if avattu == True:
            tappio()
        else:
            siirramiinaa(y, x)
            tulvataytto(tila["kentta"], x, y)
            avattu = True

#Asetellaan pelilaudalle n kappaletta miinoja satunnaisiin paikkoihin
def miinoita(kentta, vapaat, n):
    for i in range(n):
        x = random.randint(0, len(kentta[0]) - 1)
        y = random.randint(0, len(kentta) - 1)
        miina = (x, y)
        while miina not in vapaat:
            x = random.randint(0, len(kentta[0]) - 1)
            y = random.randint(0, len(kentta) - 1)
            miina = (x, y)
        vapaat.remove(miina)
        kentta[y][x] = "x"
    tila["kentta"] = kentta

#Luodaan uusi pelikenttä, jonka koko on tallennettu asetuksiin
def luokentta():
    tila["kentta"] = []
    tila["tulostettu_kentta"] = []
    for rivi in range(ASETUKSET["korkeus"]):
        tila["kentta"].append([])
        tila["tulostettu_kentta"].append([])
        for sarake in range(ASETUKSET["leveys"]):
            tila["kentta"][-1].append(" ")
            tila["tulostettu_kentta"][-1].append(" ")
    jaljella = []
    for x in range(ASETUKSET["leveys"]):
        for y in range(ASETUKSET["korkeus"]):
            jaljella.append((x, y))
    miinoita(tila["kentta"], jaljella, ASETUKSET["miinoja"])

#Piilotetaan miinat pelaajalle näkyvältä kentältä
def piilotamiinat():
    ASETUKSET["paljastettu"] = False
    for x in range(ASETUKSET["korkeus"]):
        for y in range(ASETUKSET["leveys"]):
            if tila["kentta"][x][y] == "x":
                tila["tulostettu_kentta"][x][y] = " "

#Paljastetaan pelaajalle näkyvän kentän miinat
def paljastamiinat():
    ASETUKSET["paljastettu"] = True
    for x in range(ASETUKSET["korkeus"]):
        for y in range(ASETUKSET["leveys"]):
            if tila["kentta"][x][y] == "x":
                tila["tulostettu_kentta"][x][y] = "x"

#Lasketaan ruudun x,y ympärillä olevat miinalliset ruudut
def laskemiinat(x, y, huone):
    miinoja = 0
    for r in range(-1, 2):
        for c in range(-1, 2):
            if (y+c >= 0 and x+r >= 0 and y+c <= len(huone)-1 
                and x+r <= len(huone[y-1])-1):
                if huone[y+c][x+r] == "x":
                    miinoja = miinoja + 1
    return miinoja

#Lasketaan tyhjien ruutujen määrä
def lasketyhjat(kentta):
    tyhjia = sum(x.count(" ") for x in kentta)
    return tyhjia

#Käynnistetään tulvatäyttö, eli paljastetaan alue miinakentän rajoille saakka
def tulvataytto(kentta, x, y):
    if kentta[y][x] == " ":
        aloitus = [(y, x)]
        while aloitus:
            y, x = aloitus.pop()
            tila["tulostettu_kentta"][y][x] = laskemiinat(x, y, kentta)
            tila["kentta"][y][x] = laskemiinat(x, y, kentta)
            if kentta[y][x] == 0:
                for r in range(-1, 2):
                    for c in range(-1, 2):
                        if (y+c >= 0 and x+r >= 0 and y+c <= len(kentta)-1 
                            and x+r <= len(kentta[y-1])-1):
                            if kentta[y+c][x+r] == " ":
                                aloitus.append((y+c, x+r))
        ASETUKSET["avattu"] = True
        winsound.PlaySound("kaiva.wav", winsound.SND_ASYNC)

#Lisätään tai poistetaan lippu pelilaudalta
def liputa(x, y, kentta):
    if kentta[y][x] == " ":
        kentta[y][x] = "f"
        ASETUKSET["lippuja"] = ASETUKSET["lippuja"] + 1
        winsound.PlaySound("lippu.wav", winsound.SND_ASYNC)
    elif kentta[y][x] == "f":
        kentta[y][x] = " "
        ASETUKSET["lippuja"] = ASETUKSET["lippuja"] - 1
        winsound.PlaySound("lippu.wav", winsound.SND_ASYNC)

def vasenhiiri(x, y):
    #Osutaan merkitsemättömään miinaan ja määritellään tappio
    if (tila["kentta"][y][x] == "x" and tila["tulostettu_kentta"][y][x] == " " 
        or tila["tulostettu_kentta"][y][x] == "x"):
        maaritakuolema(y, x, ASETUKSET["avattu"])
    #lippua ei avata
    elif tila["tulostettu_kentta"][y][x] == "f":
        pass
    else:
        #Muussa tapauksessa normaali tulvatäyttö
        tulvataytto(tila["kentta"], x, y)
        if lasketyhjat(tila["tulostettu_kentta"]) == 0:
            voitto()

"""Määritellään klikkauksen koordinaatit ja lasketaan mihin ruutuun osutaan.
Jokainen klikkaus lasketaan pelivuoroksi.
Hiiren oikealla näppäimellä asetetaan lippu ja vasemmalla avataan ruutuja"""
def kasittele_hiiri(x, y, nappi, muokkausnapit):
    ASETUKSET["klikkaukset"] = ASETUKSET["klikkaukset"] + 1
    x = int(x / 40)
    y = int(y / 40)
    print("Hiiren nappia {} painettiin ruudussa {}, {}".format(NAPIT[nappi], x, y))
    #Vasen nappi avaa ruutuja
    if nappi == 1:
        vasenhiiri(x, y)
    #Keskinappi näyttää miinojen sijainnit koodin toimivuuden tarkistamiseksi (huijausnappi)
    elif nappi == 2:
        if ASETUKSET["paljastettu"] == False:
            paljastamiinat()
        else:
            piilotamiinat()
    #Oikea nappi asettaa lipun
    elif nappi == 4:
        liputa(x, y, tila["tulostettu_kentta"])
        if lasketyhjat(tila["tulostettu_kentta"]) == 0 or lasketyhjat(tila["kentta"]) == 0:
            voitto()

#Piirretään pelaajan syöttämä kenttä
def piirra_kentta():
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for y, rivi in enumerate(tila["tulostettu_kentta"]):
        for x, ruutu in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(ruutu, x*40, y*40)
    haravasto.piirra_ruudut()

#Tulostaa ja tallentaa pelin tiedot, soittaa fanfaarin ja palaa päävalikkoon
def voitto():
    aika = datetime.datetime.now()
    leveys = str(ASETUKSET["leveys"])
    korkeus = str(ASETUKSET["korkeus"])
    miinat = str(ASETUKSET["miinoja"])
    ruudut = str(ASETUKSET["leveys"]*ASETUKSET["korkeus"])
    lippuja = str(ASETUKSET["lippuja"])
    klikkaukset = str(ASETUKSET["klikkaukset"])
    paivamaara = aika.strftime("%Y-%m-%d %H:%M")
    kesto_s = str(int(time.time() - ASETUKSET["aloitus_aika"]))
    kesto_m = str(round(((time.time() - ASETUKSET["aloitus_aika"])/60), 2))

    #Tulostetaan pelin tiedot
    print("_____________________________________________________\n",
        'Selvitit miinakentän ja voitit pelin, onneksi olkoon!',
        '_____________________________________________________',
        'Pelin tiedot', 'Päivämäärä: ' + paivamaara,
        'Kentän koko: leveys ' + leveys + ', korkeus ' + korkeus,
        'Miinojen määrä: ' + miinat, 'Ruutuja: ' + ruudut,
        'Pelin kesto oli ' + kesto_s + ' sekuntia tai ' + kesto_m + ' minuuttia',
        'Lippuja käytetty: ' + lippuja, 'Pelatut vuorot: ' + klikkaukset,
    sep = "\n")

    #Tallennetaan pelin tiedot
    tiedosto = open("miinaharavan_tulokset.txt", "a")
    tiedosto.write('Voitto! ' + paivamaara + '\n'
        'Kentän leveys ' + leveys + ', korkeus ' + korkeus + '\n'
        'Miinojen määrä: ' + miinat + '\n'
        'Pelin kesto oli ' + kesto_s + ' sekuntia tai ' + kesto_m + ' minuuttia\n'
        'Lippuja käytetty: ' + lippuja + '\n' 'Pelatut vuorot: ' + klikkaukset + '\n\n')

    #soittaa voitonfanfaarin
    winsound.PlaySound("voitto.wav", winsound.SND_ASYNC)
    paljastamiinat()
    tila["pelattu"]=True
    haravasto.lopeta()
    #palaa päävalikkoon
    valikko()

#Tulostaa ja tallentaa pelin tiedot, soittaa räjähdyksen ja palaa päävalikkoon
def tappio():
    aika = datetime.datetime.now()
    leveys = str(ASETUKSET["leveys"])
    korkeus = str(ASETUKSET["korkeus"])
    miinat = str(ASETUKSET["miinoja"])
    lippuja = str(ASETUKSET["lippuja"])
    klikkaukset = str(ASETUKSET["klikkaukset"])
    ruudut = str(ASETUKSET["leveys"]*ASETUKSET["korkeus"])
    tyhjia = str(lasketyhjat(tila["tulostettu_kentta"]))
    paivamaara = aika.strftime("%Y-%m-%d %H:%M")
    kesto_s = str(int(time.time() - ASETUKSET["aloitus_aika"]))
    kesto_m = str(round(((time.time() - ASETUKSET["aloitus_aika"])/60), 2))

    #Tulostetaan pelin tiedot
    print('_______________________________\n',
        'Osuit miinaan ja hävisit pelin!!',
        '_______________________________',
        'Pelin tiedot', 'Päivämäärä: ' + paivamaara,
        'Kentän koko: leveys ' + leveys + ', korkeus ' + korkeus,
        'Miinojen määrä: ' + miinat,
        'Pelin kesto oli ' + kesto_s + ' sekuntia tai ' + kesto_m +' minuuttia',
        'Lippuja käytetty: ' + lippuja, 'Pelatut vuorot: ' + klikkaukset,
        'Ruutuja jäljellä: ' + tyhjia + '/' + ruudut,
    sep = "\n")

    #Tallennetaan pelin tiedot
    tiedosto = open("miinaharavan_tulokset.txt", "a")
    tiedosto.write('Tappio! ' + paivamaara + '\n'
        'Kentän leveys ' + leveys + ', korkeus ' + korkeus + '\n'
        'Miinojen määrä: ' + miinat + '\n'
        'Pelin kesto oli ' + kesto_s + ' sekuntia tai ' + kesto_m + ' minuuttia\n'
        'Lippuja käytetty: ' + lippuja + '\n'
        'Ruutuja jäljellä: ' + tyhjia + '/' + ruudut + '\n'
        'Pelatut vuorot: ' + klikkaukset + '\n\n')

    #soittaa räjähdyksen
    winsound.PlaySound("pommi.wav", winsound.SND_ASYNC)
    haravasto.lopeta()
    #palaa päävalikkoon
    valikko()

def main():
    #Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    haravasto.lataa_kuvat("C:/Users/mjunp/Desktop/ohjelmoinnin alkeet/spritet")
    haravasto.luo_ikkuna(len(tila["kentta"][0]) * 40, len(tila["kentta"]) * 40)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aloita()

if __name__ == "__main__":
    valikko()
