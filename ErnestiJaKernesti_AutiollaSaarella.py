import tkinter as tk
import numpy as np
import winsound
import threading
import random

ikkuna=tk.Tk()
ikkuna.geometry("1000x550+100+200")

#Sanakirjan alustus
tiedot={}
tiedot['apinamaara']=0
tiedot['apina']={}
tiedot['aika_askel']=100

#Määrittää saaren ja mantereen rajat jotta apinat lähtee oikeasta kohtaa
saaren_reuna_x = 200
mantereen_reuna_x = 800

#Saaren ja mantereen väli
kokonaismatka_px = mantereen_reuna_x - saaren_reuna_x
askeleen_pituus_px = kokonaismatka_px / 100

#Hätä viesti jota apinat yrittää kuljettaa
hataviesti = "Ernesti ja Kernesti tässä terve! Olemme autiolla saarella, voisiko joku tulla sieltä sivistyneestä maailmasta hakemaan meidät pois! Kiitos!"
hataviesti_sanat = hataviesti.split()

#Toiminto joka luo ja lähettää apinan matkaan
def luo_ja_laheta_apina(start_y, sana):
    global tiedot
    print(f"Luodaaan apina: '{sana}'")
    tiedot['apinamaara']+=1
    apina_id=tiedot['apinamaara']

    #Tässä apinan tiedot tallennetaan sanakirjaan
    tiedot['apina'][apina_id] = {
        'x': saaren_reuna_x,
        'y': start_y ,
        'yksilöllinen_nimi': sana,
        'labeli': None      #Apinan label joka korvataan hätäviestin sanalla
    }

    #Apinakahva on label jolla uivaa apinaa havainnollistetaan
    apinakahva=tk.Label(ikkuna, text=sana)
    apinakahva.place(x=tiedot['apina'][apina_id]['x'],y=tiedot['apina'][apina_id]['y'])

    tiedot['apina'][apina_id]['labeli']=apinakahva

    print(tiedot)

    #Piippaus kun apina lähtee liikkeelle
    threading.Thread(target=lambda: winsound.Beep(1000, 200)).start()

    #Uinti-toiminto liikuttaa apinaa ja piipittää samalla. Kun km_maara ylittää sadan
    #apina lopettaa uimisen if-elsellä ja piippaa merkiksi
    print(f"Lähetetään apina sanan '{sana}' kanssa uimaan")
    def uinti(km_maara=0):
        if km_maara < 100:
            tiedot['apina'][apina_id]['x'] += askeleen_pituus_px
            tiedot['apina'][apina_id]['y'] += np.random.randint(-10, 10)

            if np.random.random() > 0.99:
                tiedot['apina'][apina_id]['labeli'].configure(fg='red')

            tiedot['apina'][apina_id]['labeli'].place(x=tiedot['apina'][apina_id]['x'], y=tiedot['apina'][apina_id]['y'])
            
            winsound.Beep(2000 + apina_id * 10, tiedot['aika_askel'])

            ikkuna.after(tiedot['aika_askel'], uinti, km_maara + 1)
        else:
            print(f"Apina selvisi rantaan sanan '{sana}' kanssa!")
            winsound.Beep(1000, 200)

    ikkuna.after(0, uinti)



#Valitsee random sanan hätäviestistä
def laheta_random_sana(start_y):
    sana = random.choice(hataviesti_sanat)
    threading.Thread(target=luo_ja_laheta_apina, args=(start_y, sana)).start()

def laheta_kymmenen_apinaa(start_y):
    for _ in range(10):
        laheta_random_sana(start_y)

#Nämä asettaa apinan lähtökohdaksi joko saaren pohjois- tai eteläpuolen sekä antaa apinalle sanan
def ernestin_luo_ja_laheta_apina():
    start_y = 100
    laheta_random_sana(start_y)

def kernestin_luo_ja_laheta_apina():
    start_y = 400
    laheta_random_sana(start_y)

#Alla vielä napit sekä saarta ja mannerta hahmottavat palkit

ernestin_painike = tk.Button(text="Ernesti, lähetä apina", command=ernestin_luo_ja_laheta_apina)
ernestin_painike.place(x=350, y=500)

kernestin_painike = tk.Button(text="Kernesti, lähetä apina", command=kernestin_luo_ja_laheta_apina)
kernestin_painike.place(x=200, y=500)

ernestin_kymmenen_painike = tk.Button(text="Ernesti, lähetä 10 apinaa", command=lambda: laheta_kymmenen_apinaa(100))
ernestin_kymmenen_painike.place(x=350, y=540)

kernestin_kymmenen_painike = tk.Button(text="Kernesti, lähetä 10 apinaa", command=lambda: laheta_kymmenen_apinaa(400))
kernestin_kymmenen_painike.place(x=200, y=540)

saari = tk.Frame(ikkuna, width=100, bg="lightgreen")
saari.place(x=0, y=0, width=200, relheight=1.0)

shore_frame = tk.Frame(ikkuna, width=100, bg="burlywood")
shore_frame.place(x=800, y=0, width=200, relheight=1.0)

ikkuna.mainloop()