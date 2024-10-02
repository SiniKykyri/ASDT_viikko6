import pygame
import random
import time
import threading
from tkinter import Tk, Canvas, Button

#-------- SUUNNITELMA TURVALLISESTA UIMA-ALTAASTA ----------------

# Alustetaan pääikkuna
root = Tk()
canvas = Canvas(root, width=800, height=600, bg='blue') # Sinin taustaväri kuvastamaan  merta
canvas.pack()

# Määritellään saaren koko ja sijainti
autiosaari_alue = {
    "x_min" : 100,
    "x_max" : 700,
    "y_min" : 100,
    "y_max" : 500
}
# Piirretään saari
canvas.create_rectangle(
    autiosaari_alue["x_min"], 
    autiosaari_alue["y_min"], 
    autiosaari_alue["x_max"], 
    autiosaari_alue["y_max"], 
    fill='yellow')

# Määritellään uima-altaan 20 x 60 koko ja sijainti
uima_allas_alue = {
    "x_min" : 200,
    "x_max" : 260,
    "y_min" : 200,
    "y_max" : 220
}
# Piirretään uima-allas
canvas.create_rectangle(
    uima_allas_alue["x_min"], 
    uima_allas_alue["y_min"], 
    uima_allas_alue["x_max"], 
    uima_allas_alue["y_max"], 
    fill='cyan')
# Määritetään Ernestin oja
ernestin_oja_alue = {
    "x_min" : 198,
    "x_max" : 201,
    "y_min" : 100,
    "y_max" : 200
}
# Piirretään Ernestin oja punaisella
canvas.create_rectangle(
    ernestin_oja_alue["x_min"], 
    ernestin_oja_alue["y_min"], 
    ernestin_oja_alue["x_max"], 
    ernestin_oja_alue["y_max"], 
    fill='yellow')

#Määritellään Kernestin oja
kernestin_oja_alue = {
    "x_min" : 258,
    "x_max" : 261,
    "y_min" : 100,
    "y_max" : 200
}
# Piirretään Kernestin oja vihreällä
canvas.create_rectangle(
    kernestin_oja_alue["x_min"], 
    kernestin_oja_alue["y_min"], 
    kernestin_oja_alue["x_max"], 
    kernestin_oja_alue["y_max"], 
    fill='yellow')

# Määritellään uima-allas matriisi listojen avulla. Lukuarvo 0 kuvastaa, että allas on tyhjä.
uima_allas_matriisi = [[0 for x in range(60)] for y in range(20)]
# Määritellään oja matriisi listojen avulla. Arvo 1 = hiekkaa
ernestin_oja_matriisi =[[1 for x in range(2)] for y in range(100)]
kernestin_oja_matriisi =[[1 for x in range(2)] for y in range(100)]

# Luodaan saarelle metsä alue
metsä_alue = {
    "x_min" : 150,
    "x_max" : 650,
    "y_min" : 300,
    "y_max" : 450
}
# Piirretään metsä
canvas.create_rectangle(
    metsä_alue["x_min"], 
    metsä_alue["y_min"], 
    metsä_alue["x_max"], 
    metsä_alue["y_max"], 
    fill='#006400')
# -------- SUUNNITELMA TURVALLISESTA UIMA-ALTAASTA PÄÄTTYY ----------------

# -------- RAKENTAMISEEN TARVITTAVAN TYÖVOIMAN HANKINTA ----------------
# Alustetaan pygame
pygame.mixer.init()
# Ladataan äänet
kaiva_aani = pygame.mixer.Sound("kaiva.wav")

#Funktio äänen soittamiselle
def play_sound(sound):
    sound.play()

# Määritellään sanakirja, jossa apinat ovat 
apinat = {}
# Luodaan funktio, joka luo yhden joutilaan apinan nappia painettaessa.
def luo_joutilas_apina():
    apina_id = len(apinat) + 1 # Luodaan apinalle uniikki ID
    # Sijoitetaan apina satunnaiseen paikkaan metsässä
    x = random.randint(metsä_alue["x_min"], metsä_alue["x_max"]-10) # Arvotaan apinalle x-koordinaatti
    y = random.randint(metsä_alue["y_min"], metsä_alue["y_max"]-10) # Arvotaan apinalle y-koordinaatti
    apinan_kuva = canvas.create_oval(x, y, x + 10, y + 10, fill='saddlebrown') # Piirretään apina
    #Tallenetaan apina sanakirjaan
    apinat[apina_id] = {
       "kuva" : apinan_kuva,
       "tila" : "joutilaana",
       "sijainti" : {
           "x" : x,
           "y" : y
       },
       "henkilö" : None
    }
    print(f"Luotiin apina {apina_id} T. Luo juotilas apina nappi funktio")

# Luodaan funktio, jolla Ernesti hakee yhden apinan ja valmistelee sen tehtävää varten
def ernesti_hakee_apinan():
    joutilaat_apinat = [apina_id for apina_id, apina in apinat.items() if apina["tila"] == "joutilaana"] # Haetaan kaikki joutilaana olevat apinat
    if joutilaat_apinat: # Jos joutilaana olevia apinoita on
        ernestin_valitsema_apina = random.choice(joutilaat_apinat) # Valitaan satunnainen apina joutilaana olevista apinoista
        print(f"Ernesti valitsi apinan {ernestin_valitsema_apina}")
        apinat[ernestin_valitsema_apina]["tila"] = "valmis_työhön" # Muutetaan apinan tila valmiiksi työhön.
        apinat[ernestin_valitsema_apina]["henkilö"] = "Ernesti" # Merkataan apina Ernestin omaksi
        #Arvotaan apinalla satunnainen sijainti Ernestin ojalta
        x= random.randint(ernestin_oja_alue["x_min"], ernestin_oja_alue["x_max"])
        y = random.randint(ernestin_oja_alue["y_min"], ernestin_oja_alue["y_max"])
        apinat[ernestin_valitsema_apina]["sijainti"] = {"x" : x, "y" : y}
        canvas.coords(apinat[ernestin_valitsema_apina]["kuva"], x, y, x + 10, y + 10) # Siirretään apina Ernestin ojalle
    else:
        print("Ei joutilaana olevia apinoita.")
        return
    
# Luodaan funktio, jolla valitaan yksi valmiiksi työhön merkitty apina ja kutsutaan kaiva funktiota
def ernesti_laittaa_apinan_kaivamaan():
    print("Ernesti laittaa apinan kaivamaan")
    valmiit_apinat = [apina_id for apina_id, apina in apinat.items() if apina["tila"] == "valmis_työhön" and apina["henkilö"]=="Ernesti"] # Haetaan kaikki valmiiksi työhön merkityt apinat, jotka ovat Ernestin hakemia
    if valmiit_apinat: #Tarkistetaan onko apinoita, joiden tila on "valmis työhön"
        valittu_apina = random.choice(valmiit_apinat)
        #Käynnistetään kaiva funktio omassa säikeessään
        threading.Thread(target=ernesti_kaiva, args=(valittu_apina,)).start()
    else:
        print("Ei valmiiksi työhön merkittyjä apinoita.")
        return
    
# Luodaan funktio joka kuvastaa kaivamista   
def ernesti_kaiva(apina_id):
    print(f"Apina {apina_id} kaivaa")
    # Haetaan apinan tiedot sanakirjasta
    apina = apinat[apina_id]
    x = apina["sijainti"]["x"]
    y = apina["sijainti"]["y"]
    # Määritellään aloituspaikka kaivamiselle, koska apina on satunnaisessa kohti ernestin ojaa
    aloitus_indeksi = y # Tästä lähdetään
    lopetus_ideksi = ernestin_oja_alue["y_min"] # Tähän lopetetaan
    indeksi = abs(lopetus_ideksi - aloitus_indeksi) # Lasketaan kaivamisen pituus ja palautetaan absoluuttinen arvo
    matriisi_indeksi = abs(aloitus_indeksi - len(ernestin_oja_matriisi)) # Aloitetaan oja matriisin täyttäminen tästä indeksistä. Ajatus, että indeksi 100 on altaan päässä ja 0 meren päässä.
    lepoaika = 1 # Kaivamisen lepoaika
    print(f"Kaivetaan {indeksi} yksikköä")
    
    # Simuloidaan kaivamista
    for i in range(indeksi):
        print(matriisi_indeksi) # Tulostetaan matriisi indeksi, jotta nähdään mihin kohtaan ojaa kaivetaan
        matriisi_indeksi -= 1 # Siirretään matriisi indeksiä yksi taaksepäin
        ernestin_oja_matriisi[matriisi_indeksi][0] = 0 # Kaivetaan ojaa
        play_sound(kaiva_aani) # Soitetaan kaiva ääni
        print(f"Apina {apina_id} kaivaa kohdasta {i}") # Tulostetaan kaivamisen tilaa
        canvas.coords(apina["kuva"], x, y - i, x + 10, y - i + 10) # Siirretään apina kaivamisen aikana
        time.sleep(lepoaika) # Muutetaan lepo aikaa apinan väsymyksen mukaan.
        print(f"Lepoaika on {lepoaika}")
        lepoaika *=2 # Tuplataan lepoaika aina seuraavalle kierrokselle.
       
# Luodaan nappi, jolla lisätään joutilas apina
lisaa_joutilas_apina_nappi = Button(root, text='Kohta 2: Lisää joutilas apina', command=luo_joutilas_apina)
lisaa_joutilas_apina_nappi.place(x=300, y=455)
# Luodaan nappi, jolla Ernesti hakee yhden apinan. Kutsutaan funktiota omassa säikeessään.
ernesti_hakee_apinan_nappi = Button(root, text='Kohta 2: Ernesti hakee apinan', command=lambda: threading.Thread(target =ernesti_hakee_apinan).start())
ernesti_hakee_apinan_nappi.place(x=10, y=50)
# Luodaan nappi, jolla Ernesti laittaa yhden apinan kaivamaan.
ernesti_laittaa_apinan_kaivamaan_nappi = Button(root, text='Kohta 2: Ernesti: Laita apina kaivamaan', command=ernesti_laittaa_apinan_kaivamaan) 
ernesti_laittaa_apinan_kaivamaan_nappi.pack()

# -------- RAKENTAMISEEN TARVITTAVAN TYÖVOIMAN HANKINTA PÄÄTTYY ----------------

# --------------------- YHDESSÄ ENEMMÄN ----------------------------------------
# LIPPU
stop_thread = False
#LUKKO
lukko = threading.Lock()

# Luodaan funktio, jolla Kernesti hakee yhden apinan ja valmistelee sen tehtävää varten
def kernesti_hakee_apinan():
    joutilaat_apinat = [apina_id for apina_id, apina in apinat.items() if apina["tila"] == "joutilaana"] # Haetaan kaikki joutilaana olevat apinat
    if joutilaat_apinat: # Jos joutilaana olevia apinoita on
        Kernestin_valitsema_apina = random.choice(joutilaat_apinat) # Valitaan satunnainen apina joutilaana olevista apinoista
        print(f"Kernesti valitsi apinan {Kernestin_valitsema_apina}")
        apinat[Kernestin_valitsema_apina]["tila"] = "valmis_työhön" # Muutetaan apinan tila valmiiksi työhön.
        apinat[Kernestin_valitsema_apina]["henkilö"] = "Kernesti" # Merkataan apina Ernestin omaksi
        #Arvotaan apinalla satunnainen sijainti Ernestin ojalta
        x= random.randint(kernestin_oja_alue["x_min"], kernestin_oja_alue["x_max"])
        y = random.randint(kernestin_oja_alue["y_min"], kernestin_oja_alue["y_max"])
        apinat[Kernestin_valitsema_apina]["sijainti"] = {"x" : x, "y" : y}
        canvas.coords(apinat[Kernestin_valitsema_apina]["kuva"], x, y, x + 10, y + 10) # Siirretään apina Kernestin ojalle
    else:
        print("Ei joutilaana olevia apinoita.")
        return
    
# Luodaan funktio joka kuvastaa kaivamista   
def kernesti_kaiva(apina_id):
    print(f"Apina {apina_id} kaivaa")
    # Haetaan apinan tiedot sanakirjasta
    apina = apinat[apina_id]
    x = apina["sijainti"]["x"]
    y = apina["sijainti"]["y"]
    # Määritellään aloituspaikka kaivamiselle, koska apina on satunnaisessa kohti ernestin ojaa
    aloitus_indeksi = y # Tästä lähdetään
    lopetus_ideksi = kernestin_oja_alue["y_min"] # Tähän lopetetaan
    indeksi = abs(lopetus_ideksi - aloitus_indeksi) # Lasketaan kaivamisen pituus ja palautetaan absoluuttinen arvo
    matriisi_indeksi = abs(aloitus_indeksi - len(kernestin_oja_matriisi)) # Aloitetaan oja matriisin täyttäminen tästä indeksistä. Ajatus, että indeksi 100 on altaan päässä ja 0 meren päässä.
    lepoaika = 1 # Kaivamisen lepoaika
    print(f"Kaivetaan {indeksi} yksikköä")
    
    # Simuloidaan kaivamista
    for i in range(indeksi):
        print(matriisi_indeksi) # Tulostetaan matriisi indeksi, jotta nähdään mihin kohtaan ojaa kaivetaan
        matriisi_indeksi -= 1 # Siirretään matriisi indeksiä yksi taaksepäin
        kernestin_oja_matriisi[matriisi_indeksi][0] = 0 # Kaivetaan ojaa
        play_sound(kaiva_aani) # Soitetaan kaiva ääni
        print(f"Apina {apina_id} kaivaa kohdasta {i}") # Tulostetaan kaivamisen tilaa
        canvas.coords(apina["kuva"], x, y - i, x + 10, y - i + 10) # Siirretään apina kaivamisen aikana
        time.sleep(lepoaika) # Muutetaan lepo aikaa apinan väsymyksen mukaan.
        print(f"Lepoaika on {lepoaika}")
        lepoaika *=2 # Tuplataan lepoaika aina seuraavalle kierrokselle.

# Luodaan funktio, jolla valitaan yksi valmiiksi työhön merkitty apina ja kutsutaan kaiva funktiota
def kernesti_laittaa_apinan_kaivamaan():
    print("kernesti laittaa apinan kaivamaan")
    valmiit_apinat = [apina_id for apina_id, apina in apinat.items() if apina["tila"] == "valmis_työhön" and apina["henkilö"]=="Kernesti"] # Haetaan kaikki valmiiksi työhön merkityt apinat, jotka ovat Ernestin hakemia
    if valmiit_apinat: #Tarkistetaan onko apinoita, joiden tila on "valmis työhön"
        valittu_apina = random.choice(valmiit_apinat)
        #Käynnistetään kaiva funktio omassa säikeessään
        threading.Thread(target=kernesti_kaiva, args=(valittu_apina,)).start() 
    else:
        print("Ei valmiiksi työhön merkittyjä apinoita.")
        return

# FUNKTIOT UUDEN APINAN KAIVUUTYÖHÖN LAITTAMISEEN

# Luodaan funktio, jolla Ernesti voi lisätä uuden apinan kaivamaan. Tässä lisäyksenä edelliseen kaivamis funktioon, on että apinan tila muutetaan työssä, jotta sitä ei enää valita uudestaan.
def ernesti_laittaa_uuden_apinan_kaivamaan():
    print("Ernesti laittaa uuden apinan kaivamaan")
    valmiit_apinat = [apina_id for apina_id, apina in apinat.items() if apina["tila"] == "valmis_työhön" and apina["henkilö"]=="Ernesti"] # Haetaan kaikki valmiiksi työhön merkityt apinat, jotka ovat Ernestin hakemia
    if valmiit_apinat: #Tarkistetaan onko apinoita, joiden tila on "valmis työhön"
        valittu_apina = random.choice(valmiit_apinat)
        #Muutetaan apinan tila kertomaan, että se tekee jo töitä
        apinat[valittu_apina]["tila"] = "työssä"
        apinat[valittu_apina]["thredi"] = threading.Thread(target=ernesti_kaiva_uusi_apina, args=(valittu_apina,)) #Tallennetaan theredi apinan tietoihin myöhempää käyttöä varten
        apinat[valittu_apina]["thredi"].start() #Käynnistetään kaiva funktio omassa säikeessään
    else:
        print("Ei valmiiksi työhön merkittyjä apinoita.")
        return

# Kaivuu funktio. Tämä funktio noudattaa samaa periaatetta kuin kohdan 2 funktio, mutta tässä apinan kaivaa ojaa aina syvemmälle 
# sekä tähän on lisätty ojan kaivamisen edistyminen. 

def ernesti_kaiva_uusi_apina(apina_id):
    global stop_thread

    with lukko: #Käytetään lukkoa, jotta vain yksi säie voi käyttää tätä koodia kerrallaan
        # Haetaan apinan tiedot sanakirjasta
        apina = apinat[apina_id]
        x = apina["sijainti"]["x"]
        y = apina["sijainti"]["y"]
        # Määritellään aloituspaikka kaivamiselle, koska apina on satunnaisessa kohti ernestin ojaa
        aloitus_indeksi = y # Tästä lähdetään
        lopetus_ideksi = ernestin_oja_alue["y_min"] # Tähän lopetetaan
        indeksi = abs(lopetus_ideksi - aloitus_indeksi) # Lasketaan kaivamisen pituus ja palautetaan absoluuttinen arvo
        matriisi_indeksi = abs(aloitus_indeksi - len(ernestin_oja_matriisi)) # Aloitetaan oja matriisin täyttäminen tästä indeksistä. Ajatus, että indeksi 100 on altaan päässä ja 0 meren päässä.
        lepoaika = 1 # Kaivamisen lepoaika
        canvas.itemconfig(apina["kuva"], fill='black')#Muutetaan apinan väri osoittamaan, että se tekee töitä

        ojan_korkeus = ernestin_oja_alue["y_max"] - ernestin_oja_alue["y_min"] # Lasketaan ojan korkeus pikseleinä
        matriisin_korkeus = len(ernestin_oja_matriisi) # Lasketaan matriisin korkeus
        pikselit_per_askel = ojan_korkeus / matriisin_korkeus # Lasketaan kuinka monta pikseliä yksi askel on
       
    # Simuloidaan kaivamista
    for i in range(indeksi):
        if stop_thread: # Jos lippu on tosi, niin lopetetaan kaivaminen
            print("Kaivaminen pyydetty pysäyttämään")
            return
        with lukko: #Käytetään lukkoa, jotta vain yksi säie voi käyttää tätä koodia kerrallaan
            print(matriisi_indeksi) # Tulostetaan matriisi indeksi, jotta nähdään mihin kohtaan ojaa kaivetaan
            matriisi_indeksi -= 1 # Siirretään matriisi indeksiä yksi taaksepäin
            ernestin_oja_matriisi[matriisi_indeksi][0] -= 1 # Kaivetaan ojaa
            play_sound(kaiva_aani) # Soitetaan kaiva ääni
            
            # Lasketaan canvasin y-koordinaattit kaivamisen perusteella
            y_alku = ernestin_oja_alue["y_min"] + matriisi_indeksi * pikselit_per_askel # Lasketaan visuaallisen alueen y-koordinaatin yläraja
            y_loppu = y_alku + pikselit_per_askel # Lasketaan visuaallisen alueen y-koordinaatin alaraja
            if ernestin_oja_matriisi[matriisi_indeksi][0] <= 0: #Muuta ojan väriä, jos arvo on 0 tai vähemmän
                canvas.create_rectangle( # Piirretään ojan osa uudella värillä
                    ernestin_oja_alue["x_min"], 
                    y_alku, 
                    ernestin_oja_alue["x_max"], 
                    y_loppu, 
                    fill='red', 
                    outline='red')
                canvas.update()

        print(f"Apina {apina_id} kaivaa kohdasta {i}") # Tulostetaan kaivamisen tilaa
        canvas.coords(apina["kuva"], x, y - i, x + 10, y - i + 10) # Siirretään apina kaivamisen aikana
        time.sleep(lepoaika) # Muutetaan lepo aikaa apinan väsymyksen mukaan.
        lepoaika *=2 # Tuplataan lepoaika aina seuraavalle kierrokselle.

# Luodaan funktio, jolla Ernesti voi lisätä uuden apinan kaivamaan. Tässä lisäyksenä edelliseen kaivamis funktioon, on että apinan tila muutetaan työssä, jotta sitä ei enää valita uudestaan.
def kernesti_laittaa_uuden_apinan_kaivamaan():
    print("Kernesti laittaa uuden apinan kaivamaan")
    valmiit_apinat = [apina_id for apina_id, apina in apinat.items() if apina["tila"] == "valmis_työhön" and apina["henkilö"]=="Kernesti"] # Haetaan kaikki valmiiksi työhön merkityt apinat, jotka ovat Ernestin hakemia
    if valmiit_apinat: #Tarkistetaan onko apinoita, joiden tila on "valmis työhön"
        valittu_apina = random.choice(valmiit_apinat)
        #Muutetaan apinan tila kertomaan, että se tekee jo töitä
        apinat[valittu_apina]["tila"] = "työssä"
        apinat[valittu_apina]["thredi"] = threading.Thread(target=kernesti_kaiva_uusi_apina, args=(valittu_apina,)) #Tallennetaan theredi apinan tietoihin myöhempää käyttöä varten
        apinat[valittu_apina]["thredi"].start() #Käynnistetään kaiva funktio omassa säikeessään
    else:
        print("Ei valmiiksi työhön merkittyjä apinoita.")
        return

# Kaivuu funktio. Tämä funktio noudattaa samaa periaatetta kuin kohdan 2 funktio, mutta tässä apinan kaivaa ojaa aina syvemmälle.
def kernesti_kaiva_uusi_apina(apina_id):
    global stop_thread
    with lukko: #Käytetään lukkoa, jotta vain yksi säie voi käyttää tätä koodia kerrallaan
        # Haetaan apinan tiedot sanakirjasta
        apina = apinat[apina_id]
        x = apina["sijainti"]["x"]
        y = apina["sijainti"]["y"]
        # Määritellään aloituspaikka kaivamiselle, koska apina on satunnaisessa kohti kernestin ojaa
        aloitus_indeksi = y # Tästä lähdetään
        lopetus_ideksi = kernestin_oja_alue["y_min"] # Tähän lopetetaan
        indeksi = abs(lopetus_ideksi - aloitus_indeksi) # Lasketaan kaivamisen pituus ja palautetaan absoluuttinen arvo
        matriisi_indeksi = abs(aloitus_indeksi - len(kernestin_oja_matriisi)) # Aloitetaan oja matriisin täyttäminen tästä indeksistä. Ajatus, että indeksi 100 on altaan päässä ja 0 meren päässä.
        lepoaika = 1 # Kaivamisen lepoaika
        canvas.itemconfig(apina["kuva"], fill='black') #Muutetaan apinan väri osoittamaan, että se tekee töitä

        ojan_korkeus = kernestin_oja_alue["y_max"] - kernestin_oja_alue["y_min"] # Lasketaan ojan korkeus pikseleinä
        matriisin_korkeus = len(kernestin_oja_matriisi) # Lasketaan matriisin korkeus
        pikselit_per_askel = ojan_korkeus / matriisin_korkeus # Lasketaan kuinka monta pikseliä yksi askel on
       
        # Simuloidaan kaivamista
    for i in range(indeksi):
        if stop_thread: # Jos lippu on tosi, niin lopetetaan kaivaminen
            print("Kaivaminen pyydetty pysäyttämään")
            return
        with lukko: #Käytetään lukkoa, jotta vain yksi säie voi käyttää tätä koodia kerrallaan
            print(matriisi_indeksi) # Tulostetaan matriisi indeksi, jotta nähdään mihin kohtaan ojaa kaivetaan
            matriisi_indeksi -= 1 # Siirretään matriisi indeksiä yksi taaksepäin
            kernestin_oja_matriisi[matriisi_indeksi][0] -= 1 # Kaivetaan ojaa
            play_sound(kaiva_aani) # Soitetaan kaiva ääni
            # Lasketaan canvasin y-koordinaattit kaivamisen perusteella
            y_alku = kernestin_oja_alue["y_min"] + matriisi_indeksi * pikselit_per_askel # Lasketaan visuaallisen alueen y-koordinaatin yläraja
            y_loppu = y_alku + pikselit_per_askel # Lasketaan visuaallisen alueen y-koordinaatin alaraja
            if kernestin_oja_matriisi[matriisi_indeksi][0] <= 0: #Muuta ojan väriä, jos arvo on 0 tai vähemmän
                canvas.create_rectangle( # Piirretään ojan osa uudella värillä
                    kernestin_oja_alue["x_min"], 
                    y_alku, 
                    kernestin_oja_alue["x_max"], 
                    y_loppu, 
                    fill='red', 
                    outline='red')
                canvas.update()

        print(f"Apina {apina_id} kaivaa kohdasta {i}") # Tulostetaan kaivamisen tilaa
        canvas.coords(apina["kuva"], x, y - i, x + 10, y - i + 10) # Siirretään apina kaivamisen aikana
        time.sleep(lepoaika) # Muutetaan lepo aikaa apinan väsymyksen mukaan.
        print(f"Lepoaika on {lepoaika}")
        lepoaika *=2 # Tuplataan lepoaika aina seuraavalle kierrokselle.
              

# Luodaan nappi, jolla Kernesti hakee yhden apinan. Kutsutaan funktiota omassa säikeessään.
kernesti_hakee_apinan_nappi = Button(root, text='Kohta 3: Kernesti hakee apinan', command=lambda: threading.Thread(target =kernesti_hakee_apinan).start())
kernesti_hakee_apinan_nappi.place(x=250, y=50)
# Luodaan nappi, jolla Ernesti laittaa yhden apinan kaivamaan.
kernesti_laittaa_apinan_kaivamaan_nappi = Button(root, text='Kohta 3: Kernesti: Laita apina kaivamaan', command=kernesti_laittaa_apinan_kaivamaan) 
kernesti_laittaa_apinan_kaivamaan_nappi.pack()
# Luodaan nappi, jolla Ernesti voi lisätä uuden apinan kaivamaan. 
ernesti_laita_uusi_apina_kaivamaan_nappi = Button(root, text='Kohta 3: Ernesti: Laita uusi apina kaivamaan', command=ernesti_laittaa_uuden_apinan_kaivamaan)
ernesti_laita_uusi_apina_kaivamaan_nappi.pack()
# Luodaan nappi, jolla Kernesti voi lisätä uuden apinan kaivamaan. 
kernesti_laita_uusi_apina_kaivamaan_nappi = Button(root, text='Kohta 3: Kernesti: Laita uusi apina kaivamaan', command=kernesti_laittaa_uuden_apinan_kaivamaan)
kernesti_laita_uusi_apina_kaivamaan_nappi.pack()

# --------------------- YHDESSÄ ENEMMÄN PÄÄTTYY --------------------------------
# --------------------- OPTIMAALINEN RESURSSIEN KÄYTTÖ --------------------------

#Luodaan toiminto, jolla Ernestin ja Kernestin ojat täytetään
def tayta_ojat():
    print("Täytetään ojat")
    ilmoitus = canvas.create_text(300, 330, text="Ojien täyttäminen käynnissä", fill='black', font=('Arial', 20)) # Tulostetaan ruudulle, että ojien täyttämistä tehdään
    global stop_thread
    stop_thread = True # Annetaan kaikille threadeille lippu, että ne lopettavat kaivamisen

    # Poistetaan työssä ja valmiina työhon olevat apinat ojan reunalta. Koodi voisi myös palauttaa ne joutilaaksi, mutta tässä ne ovat nyt kerta käyttöisiä apinoita.
    with lukko: # Käytitään lukitusta, jotta apinoiden tilaa ei muuteta samaan aikaan, kun niitä poistetaan
        for apina_id, apina in apinat.items(): # Käydään läpi kaikki apinat sanakirjassa
            if apina["tila"] == "työssä": # Jos apina on työssä
                # Suljetaan apinan säie
                if "thredi" in apina:
                    apina["thredi"].join() # Odotetaan, että apinan säie on lopettanut
                    del apina["thredi"] # Poistetaan apinan säie
                    canvas.delete(apina["kuva"]) # Poistetaan apina ruudusta
            elif apina["tila"] == "valmis_työhön":
                canvas.delete(apina["kuva"])
     
    for i in range(100): #Muutetaan sekä ernestin, että kernestin oja matriisi arvot 1:ksi. Tämä kuvastaa, että oja on täynnä hiekkaa.
        ernestin_oja_matriisi[i][1] = 1
        kernestin_oja_matriisi[i][1] = 1
 
    # Muuttaa ojan väri takaisin alkuperäiseen.
    canvas.create_rectangle( # Ernestin oja
        ernestin_oja_alue["x_min"], 
        ernestin_oja_alue["y_min"], 
        ernestin_oja_alue["x_max"], 
        ernestin_oja_alue["y_max"], 
        fill='yellow')

    canvas.create_rectangle( # Kernestin oja 
        kernestin_oja_alue["x_min"], 
        kernestin_oja_alue["y_min"], 
        kernestin_oja_alue["x_max"], 
        kernestin_oja_alue["y_max"], 
        fill='yellow')
    
    stop_thread = False # Poistetaan lippu, jotta kaivaminen voidaan aloittaa uudestaan
    
    

# Luodaan nappi, jolla täytetään ojat
tayta_ojat_nappi = Button(root, text='Kohta 4: Täytä ojat', command=tayta_ojat)
tayta_ojat_nappi.pack()

# --------------------- OPTIMAALINEN RESURSSIEN KÄYTTÖ PÄÄTTYY ------------------
# ----------- DEBUGGIN ------------------
# Tämä on nyt vain debuggausta varten oleva funktio, jolla voin tarkistaa apinoiden tilan
def tulosta_apinat():
    print(apinat)

def tulosta_ernestin_oja_matriisi():
    print(ernestin_oja_matriisi)

def tulosta_kernestin_oja_matriisi():
    print(kernestin_oja_matriisi)

# Luodaan nappi, jolla tulostetaan apinoiden tila
tulosta_apinat_nappi = Button(root, text='Tulosta apinat', command=tulosta_apinat)
tulosta_apinat_nappi.pack()

tulosta_ernestin_oja_nappi = Button(root, text='Tulosta Ernestin oja', command=tulosta_ernestin_oja_matriisi)
tulosta_ernestin_oja_nappi.pack()

tulosta_kernestin_oja_nappi = Button(root, text='Tulosta Kernestin oja', command=tulosta_kernestin_oja_matriisi)
tulosta_kernestin_oja_nappi.pack()
#-------- DEBUGGIN PÄÄTTYY ----------------



# Käynnistetään pääikkuna
root.mainloop()