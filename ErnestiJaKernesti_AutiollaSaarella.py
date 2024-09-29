import tkinter as tk
import time
import numpy as np
import winsound
import threading

ikkuna=tk.Tk()

ikkuna.geometry("1000x550+100+200")

tiedot={}
tiedot['apinamaara']=0
tiedot['apina']={}
tiedot['aika_askel']=100

saaren_reuna_x = 200
mantereen_reuna_x = 800

kokonaismatka_px = mantereen_reuna_x - saaren_reuna_x
askeleen_pituus_px = kokonaismatka_px / 100


def luo_ja_laheta_apina(start_y):
    global tiedot
    print("Luodaaan apina...")
    tiedot['apinamaara']+=1
    apina_id=tiedot['apinamaara']

    tiedot['apina'][apina_id] = {
        'nimi': 'Ernestin apina',
        'x': saaren_reuna_x,
        'y': start_y ,
        'lempiväri': 'oranssi',
        'yksilöllinen_nimi': ''.join(['E', str(apina_id)])
    }


    # mitä kaikkea sanakirjaan voidaankaan laittaa...
    apinakahva=tk.Label(text=tiedot['apina'][apina_id]['yksilöllinen_nimi'])
    apinakahva.place(x=tiedot['apina'][apina_id]['x'],y=tiedot['apina'][apina_id]['y'])

    tiedot['apina'][apina_id]['labeli']=apinakahva

    print(tiedot)

    #time.sleep(0.5)
    threading.Thread(target=lambda: winsound.Beep(1000, 200)).start()
    #time.sleep(0.5)

    print("Lähetetään se uimaan")
    def uinti(km_maara=0):
        if km_maara < 100:
            tiedot['apina'][apina_id]['x'] += askeleen_pituus_px
            tiedot['apina'][apina_id]['y'] += np.random.randint(-10, 10)

            if np.random.random() > 0.9:
                tiedot['apina'][apina_id]['labeli'].configure(fg='red')

            tiedot['apina'][apina_id]['labeli'].place(x=tiedot['apina'][apina_id]['x'], y=tiedot['apina'][apina_id]['y'])
            
            winsound.Beep(2000 + apina_id * 10, tiedot['aika_askel'])

            ikkuna.after(tiedot['aika_askel'], uinti, km_maara + 1)
        else:
            print("Apina selvisi rantaan!")
            winsound.Beep(1000, 200)

    ikkuna.after(0, uinti)

def ernestin_luo_ja_laheta_apina():
    luo_ja_laheta_apina(100)

def kernestin_luo_ja_laheta_apina():
    luo_ja_laheta_apina(400)

def luo_ja_laheta_apina_saikeistin_ylhaalta():
    kahva = threading.Thread(target=ernestin_luo_ja_laheta_apina)
    kahva.start()

def luo_ja_laheta_apina_saikeistin_alhaalta():
    kahva = threading.Thread(target=kernestin_luo_ja_laheta_apina)
    kahva.start()

#def tarkkaile():
    #global tiedot
    #for i in range(100):
        #for api in range(tiedot['apinamaara']):
            #y_koordinaatti_juuri_talla_apinalla=tiedot['apina'][api]['y']
            #print("Tarkasteltava apina on korkeudella",y_koordinaatti_juuri_talla_apinalla)

        #if tiedot['apinamaara']>20:
            #winsound.Beep(4000,1000)
            #print("Meressä on ahdasta!")
        #winsound.Beep(262,200)
        #time.sleep(1)

#def tarkkaile_saikeistin():
    #kahva=threading.Thread(target=tarkkaile)
    #kahva.start()


ernestin_painike = tk.Button(text="Ernesti, lähetä apina", command=ernestin_luo_ja_laheta_apina)
ernestin_painike.place(x=350, y=500)

kernestin_painike = tk.Button(text="Kernesti, lähetä apina", command=kernestin_luo_ja_laheta_apina)
kernestin_painike.place(x=200, y=500)

#tarkkailija_painike=tk.Button(text="Tarkkaile Ernestin apinoita",command=tarkkaile_saikeistin)
#tarkkailija_painike.place(x=500,y=500)

saari = tk.Frame(ikkuna, width=100, bg="lightgreen")
saari.place(x=0, y=0, width=200, relheight=1.0)

shore_frame = tk.Frame(ikkuna, width=100, bg="burlywood")
shore_frame.place(x=800, y=0, width=200, relheight=1.0)

#niksi
#ikkuna.after(1000,ikkuna.destroy)

ikkuna.mainloop()