import http.client
import json
import tkinter as tk
from tkinter import  font #custom fontlar için lazım.
import datetime
import time
import asyncio #asenkron işlemler için
import locale
import sqlite3
from tkinter import simpledialog,messagebox #Kullanıcıya mesaj göndermek için

from tkinter import ttk #Tkinter'ın temel modülüne ek olarak, ttk modülü daha gelişmiş ve özelleştirilebilir GUI bileşenlerini sağlar.

#Varlıklarım Uygulamam


conn = http.client.HTTPSConnection("api.collectapi.com") #Döviz için
conn2 = http.client.HTTPSConnection("api.collectapi.com") #Altın için

headers = {
    'content-type': "application/json",
    'authorization': "apikey 2fs6zshAYFYRR2OISZHqEV:5HeoZPsQ0xO5EKc39VOSSl"

    }

conn.request("GET", "/economy/currencyToAll?int=10&base=TRY", headers=headers)
conn2.request("GET", "/economy/goldPrice", headers=headers)

res = conn.getresponse()
res2 = conn2.getresponse()
data = res.read()
data2 = res2.read()

results = (data.decode("utf-8"))
results2 = data2.decode("utf-8")

print(results)
print(results2)

jsonData = json.loads(results)
jsonData2 = json.loads(results2)

mylist = [13,50,49,6,38,36,28,7,24]#Döviz için çevireceğim bunları seçtim
#Euro,US Dollar,British Pound,Bulgarian Lev,Russian Ruble,Qatari Riyal,Mexican Peso,Canadian Dollar,Kuwaiti Dinar

mylist2 = [0,2,3,4]#Altın için bunları çevireceğim
#Gram,Çeyrek,Yarım,Tam

myDatas = [] #Döviz Verileri bunun içinde matris olarak saklancak a11 a12 a13, a21 a22 a23, ...
myDatas2 = []#Altın verileri bunda saklanacak
for i in mylist:
    myDatas.append([round((1.0/jsonData["result"]["data"][i]["rate"]),2),(jsonData["result"]["data"][i]["name"]),(jsonData["result"]["data"][i]["code"])])

for i in mylist2:
    myDatas2.append([jsonData2["result"][i]["name"],jsonData2["result"][i]["buying"],jsonData2["result"][i]["selling"]])



for i in myDatas:
    print("1",i[1],i[0],"Türk Lirası")

for i in myDatas2:
    print(i)



#---------------------------- APİ İŞLEMLERİ BİTTİ ŞİMDİ TKİNTER VE SQL ------------------------------------------


#Properties

euro = 0
usDollar = 0
britishPound = 0
bulgarianLev = 0
russianRuble = 0
qatariRiyal = 0
mexicanPeso = 0
canadianDollar = 0
kuwaitiDinar= 0
gramAltin = 0
ceyrekAltin = 0
yarımAltin = 0
tamAltin = 0


türkLirası = 0
döviz = 0
altın = 0
toplamVarlıklar = türkLirası + döviz + altın


#Date
locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
now = datetime.datetime.now()
today = now.date()
formattedDate = now.strftime("%d %B %Y, %H:%M")


#Pencere oluşumu
pencere = tk.Tk()
pencere.geometry("1020x720")
pencere.title("Varlıklarım Uygulaması") #En tepedeki pencere titlesi


#Özel Fontlar
titleFont = font.Font(family="Comfortaa",size=22,weight="bold")
dateFont = font.Font(family="Comfortaa",size=15)
infoFont = font.Font(family="Comfortaa",size=13,slant="italic")
customFont = font.Font(family="Comfortaa",size=17)


#SQL
tablo = sqlite3.connect("database.db")
cur = tablo.cursor()
#Tablolar oluştu
cur.execute('''CREATE TABLE IF NOT EXISTS Paramız
                (name TEXT,value INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Tarihler
                (date TEXT,value INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Dövizlerimiz
                (name TEXT,value FLOAT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Altınlarımız
                (name TEXT,value FLOAT)''')




#Tabloda verimiz varmı yokmu diye kontrol ediyor

#-----------TÜRK LİRASI - DÖVİZ - ALTIN KONTROLÜ-----------
cur.execute('''SELECT * FROM Paramız WHERE name = ?''',("Türk Lirası",))
row1 = cur.fetchone()
if row1:
    türkLirası = row1[1]

else:
    cur.execute('''INSERT INTO Paramız(name,value)
    VALUES(?, ?)''',("Türk Lirası",0))
    tablo.commit()


cur.execute('''SELECT * FROM Paramız WHERE name = ?''',("Döviz",))
row2 = cur.fetchone()
if row2:
    döviz = row2[1]

else:
    cur.execute('''INSERT INTO Paramız(name,value)
    VALUES(?, ?)''',("Döviz",0))
    tablo.commit()

cur.execute('''SELECT * FROM Paramız WHERE name = ?''',("Altın",))
row3 = cur.fetchone()
if row3:
    altın = row3[1]

else:
    cur.execute('''INSERT INTO Paramız(name,value)
    VALUES(?, ?)''',("Altın",0))
    tablo.commit()



#DETAYLI DÖVİZ VE ALTIN TABLOSU

cur.execute('''SELECT * FROM Dövizlerimiz WHERE name = ?''', ("Euro",))
fetchEuro = cur.fetchone()
if fetchEuro:
    euro = fetchEuro[1]
else:
    cur.execute("""INSERT INTO Dövizlerimiz(name,value) VALUES(?, ?)""", ("Euro", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Dövizlerimiz WHERE name = ?''', ("Us dollar",))
fetchUsDollar = cur.fetchone()
if fetchUsDollar:
    usDollar = fetchUsDollar[1]
else:
    cur.execute("""INSERT INTO Dövizlerimiz(name,value) VALUES(?, ?)""", ("Us dollar", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Dövizlerimiz WHERE name = ?''', ("British pound",))
fetchBritishPound = cur.fetchone()
if fetchBritishPound:
    britishPound = fetchBritishPound[1]
else:
    cur.execute("""INSERT INTO Dövizlerimiz(name,value) VALUES(?, ?)""", ("British pound", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Dövizlerimiz WHERE name = ?''', ("Bulgarian lev",))
fetchBulgarianLev = cur.fetchone()
if fetchBulgarianLev:
    bulgarianLev = fetchBulgarianLev[1]
else:
    cur.execute("""INSERT INTO Dövizlerimiz(name,value) VALUES(?, ?)""", ("Bulgarian lev", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Dövizlerimiz WHERE name = ?''', ("Russian ruble",))
fetchRussianRuble = cur.fetchone()
if fetchRussianRuble:
    russianRuble = fetchRussianRuble[1]
else:
    cur.execute("""INSERT INTO Dövizlerimiz(name,value) VALUES(?, ?)""", ("Russian ruble", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Dövizlerimiz WHERE name = ?''', ("Qatari riyal",))
fetchQatariRiyal = cur.fetchone()
if fetchQatariRiyal:
    qatariRiyal = fetchQatariRiyal[1]
else:
    cur.execute("""INSERT INTO Dövizlerimiz(name,value) VALUES(?, ?)""", ("Qatari riyal", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Dövizlerimiz WHERE name = ?''', ("Mexican peso",))
fetchMexicanPeso = cur.fetchone()
if fetchMexicanPeso:
    mexicanPeso = fetchMexicanPeso[1]
else:
    cur.execute("""INSERT INTO Dövizlerimiz(name,value) VALUES(?, ?)""", ("Mexican peso", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Dövizlerimiz WHERE name = ?''', ("Canadian dollar",))
fetchCanadianDollar = cur.fetchone()
if fetchCanadianDollar:
    canadianDollar = fetchCanadianDollar[1]
else:
    cur.execute("""INSERT INTO Dövizlerimiz(name,value) VALUES(?, ?)""", ("Canadian dollar", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Dövizlerimiz WHERE name = ?''', ("Kuwaiti dinar",))
fetchKuwaitiDinar = cur.fetchone()
if fetchKuwaitiDinar:
    kuwaitiDinar = fetchKuwaitiDinar[1]
else:
    cur.execute("""INSERT INTO Dövizlerimiz(name,value) VALUES(?, ?)""", ("Kuwaiti dinar", 0))
    tablo.commit()




cur.execute('''SELECT * FROM Altınlarımız WHERE name = ?''', ("Gram Altın",))
fetchGramAltin = cur.fetchone()
if fetchGramAltin:
    gramAltin = fetchGramAltin[1]
else:
    cur.execute("""INSERT INTO Altınlarımız(name,value) VALUES(?, ?)""", ("Gram Altın", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Altınlarımız WHERE name = ?''', ("Çeyrek Altın",))
fetchCeyrekAltin = cur.fetchone()
if fetchCeyrekAltin:
    ceyrekAltin = fetchCeyrekAltin[1]
else:
    cur.execute("""INSERT INTO Altınlarımız(name,value) VALUES(?, ?)""", ("Çeyrek Altın", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Altınlarımız WHERE name = ?''', ("Yarım Altın",))
fetchYarimAltin = cur.fetchone()
if fetchYarimAltin:
    yarımAltin = fetchYarimAltin[1]
else:
    cur.execute("""INSERT INTO Altınlarımız(name,value) VALUES(?, ?)""", ("Yarım Altın", 0))
    tablo.commit()

cur.execute('''SELECT * FROM Altınlarımız WHERE name = ?''', ("Tam Altın",))
fetchTamAltin = cur.fetchone()
if fetchTamAltin:
    tamAltin = fetchTamAltin[1]
else:
    cur.execute("""INSERT INTO Altınlarımız(name,value) VALUES(?, ?)""", ("Tam Altın", 0))
    tablo.commit()



döviz = round((euro * myDatas[0][0]) + (usDollar * myDatas[1][0])  + (britishPound * myDatas[2][0]) + (bulgarianLev * myDatas[3][0]) + (russianRuble * myDatas[4][0]) + (qatariRiyal * myDatas[5][0]) + (mexicanPeso * myDatas[6][0]) + (canadianDollar * myDatas[7][0]) + (kuwaitiDinar * myDatas[8][0]),2)
altın = round((gramAltin * myDatas2[0][1]) + (ceyrekAltin * myDatas2[1][1]) + (yarımAltin * myDatas2[2][1]) + (tamAltin * myDatas2[3][1]),2)





#SQL Tarihler tablosuna uygulama her açıldığında eklenecek
cur.execute('''INSERT INTO Tarihler(date,value)
VALUES(?, ?)''',(formattedDate,toplamVarlıklar))
tablo.commit()
toplamVarlıklar = türkLirası + döviz + altın
cur.execute("""UPDATE Tarihler
       SET value = ?
       WHERE date = ?
       """, (toplamVarlıklar, f"{formattedDate}"))
tablo.commit()


#Kar-Zarar durumu
cur.execute("""SELECT value FROM Tarihler""")
fetchLastValue = cur.fetchall()
sonKayitliPara = (fetchLastValue[-2][0]) # -1 olan son kayıtlı olan yeni girerkenki önceki -2 olur


karZarar = toplamVarlıklar - sonKayitliPara
print(karZarar)


#Her güncellemede çağrılcak func
def canvasFunc():


    arc = myCanvas.create_arc(coord, start=0, extent=((türkLirası * 360) / toplamVarlıklar-0.0001), fill="red")
    arv2 = myCanvas.create_arc(coord, start=((türkLirası * 360) / toplamVarlıklar - 0.0001),
                               extent=((döviz * 360) / toplamVarlıklar - 0.001), fill="blue")
    arv3 = myCanvas.create_arc(coord, start=((döviz * 360) / toplamVarlıklar - 0.001) + ((türkLirası * 360) / toplamVarlıklar - 0.001),
                               extent=((altın * 360) / toplamVarlıklar - 0.001), fill="yellow")



#Canvas
myCanvas = tk.Canvas(pencere, height=130, width=130)
coord = 10, 10, 130, 130
if toplamVarlıklar == 0:
    arc = myCanvas.create_arc(coord,start=0,extent=359.99,fill ="white") #360 derece yapmak sıkıntı çıkarıyor ondan böyle
else:
   canvasFunc()

#Buton fonksiyonları
def butonTlParaYatır():
    print("tl yaıtr")
    if entryTl.get().isdigit() and entryTl.get() != "0" :
       print(entryTl.get())
       global türkLirası
       türkLirası += int(entryTl.get())
       cur.execute("""UPDATE Paramız
       SET value = ?
       WHERE name = ?
       """,(türkLirası,"Türk Lirası"))
       tablo.commit()
       global  toplamVarlıklar
       toplamVarlıklar = türkLirası + döviz + altın
       cur.execute("""UPDATE Tarihler
           SET value = ?
           WHERE date = ?
           """, (toplamVarlıklar, f"{formattedDate}"))
       tablo.commit()
       etiket3.config(text=f"{toplamVarlıklar} Türk Lirası")
       etiket5.config(text=f"{türkLirası} Türk Lirası")

    else:
        print("olmaz")
        messagebox.showerror("HATA", "Geçerli Bir Değer Girin")
    canvasFunc()
    entryTl.delete(0, tk.END)
    entryTl.insert(0, "")
    entryTl.config(fg="black")




def butonTlParaCek():
    print("tl çek")
    if entryTl.get().isdigit() and entryTl.get() != "0":
        global türkLirası
        if türkLirası >= int(entryTl.get()):
            türkLirası -= int(entryTl.get())
            cur.execute("""UPDATE Paramız
                SET value = ?
                WHERE name = ?
                """, (türkLirası, "Türk Lirası"))
            tablo.commit()
            global toplamVarlıklar
            toplamVarlıklar = türkLirası + döviz + altın
            cur.execute("""UPDATE Tarihler
            SET value = ?
            WHERE date = ?
            """, (toplamVarlıklar, f"{formattedDate}"))
            tablo.commit()
            etiket3.config(text=f"{toplamVarlıklar} Türk Lirası")
            etiket5.config(text=f"{türkLirası} Türk Lirası")
        else:
            messagebox.showerror("HATA", "Yeterli Para Yok")
    else:
        messagebox.showerror("HATA", "Geçerli Bir Değer Girin")
    if toplamVarlıklar == 0:
        arc = myCanvas.create_arc(coord, start=0, extent=359.99, fill="white")
    else:
        canvasFunc()
    entryTl.delete(0, tk.END)
    entryTl.insert(0, "")
    entryTl.config(fg="black")


def butonDovizParaYatır():
    print("döviz yaıtr")

    if entryDöviz.get().isdigit() and entryDöviz.get() != "0":
        yatirilcakTutar = int(entryDöviz.get())
        global toplamVarlıklar
        options = []
        for i in myDatas:
            options.append(i[1])
        loweroptions = [s.lower() for s in options]

        selectedOption = simpledialog.askstring("Hesaba Yatırılcak Döviz",
                                                "Bir seçenek yazın:\n\n" + "\n".join(options))
        print(selectedOption.lower().capitalize())

        if selectedOption.lower() in loweroptions:
            cur.execute("""UPDATE Dövizlerimiz
                   SET value = ?
                   WHERE name = ?
                   """, (yatirilcakTutar, f"{selectedOption.capitalize()}"))
            tablo.commit()



            if selectedOption.lower().capitalize() == "Euro":
                global euro
                euro += yatirilcakTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (euro, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Us dollar":
                global usDollar
                usDollar += yatirilcakTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (usDollar, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "British pound":
                global britishPound
                britishPound += yatirilcakTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (britishPound, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Bulgarian lev":
                global bulgarianLev
                bulgarianLev += yatirilcakTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (bulgarianLev, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Russian ruble":
                global russianRuble
                russianRuble += yatirilcakTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (russianRuble, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Qatari riyal":
                global qatariRiyal
                qatariRiyal += yatirilcakTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (qatariRiyal, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Mexican peso":
                global mexicanPeso
                mexicanPeso += yatirilcakTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (mexicanPeso, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Canadian dollar":
                global canadianDollar
                canadianDollar += yatirilcakTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (canadianDollar, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Kuwaiti dinar":
                global kuwaitiDinar
                kuwaitiDinar += yatirilcakTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (kuwaitiDinar, f"{selectedOption.capitalize()}"))
                tablo.commit()
            döviz = round((euro * myDatas[0][0]) + (usDollar * myDatas[1][0]) + (britishPound * myDatas[2][0]) + (
                        bulgarianLev * myDatas[3][0]) + (russianRuble * myDatas[4][0]) + (
                                qatariRiyal * myDatas[5][0]) + (mexicanPeso * myDatas[6][0]) + (
                                canadianDollar * myDatas[7][0]) + (kuwaitiDinar * myDatas[8][0]),2)
            toplamVarlıklar = türkLirası + döviz + altın
            etiket3.config(text=f"{round(toplamVarlıklar,2)} Türk Lirası")
            etiket7.config(text=f"{döviz} Türk Lirası")

            cur.execute("""UPDATE Tarihler
                       SET value = ?
                       WHERE date = ?
                       """, (toplamVarlıklar, f"{formattedDate}"))
            tablo.commit()

        else:

            # Geçersiz seçim mesajı gösterme
            messagebox.showerror("Hata", "Geçersiz seçim!")

    else:
        messagebox.showerror("HATA", "Geçerli Bir Değer Girin")
    canvasFunc()
    entryDöviz.delete(0, tk.END)
    entryDöviz.insert(0, "")
    entryDöviz.config(fg="black")




def butonDovizParaCek():
    print("döviz çek")

    if entryDöviz.get().isdigit() and entryDöviz.get() != "0":
        cekilecekTutar = int(entryDöviz.get())
        options = []
        for i in myDatas:
            options.append(i[1])
        loweroptions = [s.lower() for s in options]

        selectedOption = simpledialog.askstring("Hesaptan Çekilecek Döviz",
                                                "Bir seçenek yazın:\n\n" + "\n".join(options))
        if selectedOption.lower() in loweroptions:
            if selectedOption.lower().capitalize() == "Euro":
                global euro
                euro -= cekilecekTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (euro, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Us dollar":
                global usDollar
                usDollar -= cekilecekTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (usDollar, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "British pound":
                global britishPound
                britishPound -= cekilecekTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (britishPound, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Bulgarian lev":
                global bulgarianLev
                bulgarianLev -= cekilecekTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (bulgarianLev, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Russian ruble":
                global russianRuble
                russianRuble -= cekilecekTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (russianRuble, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Qatari riyal":
                global qatariRiyal
                qatariRiyal -= cekilecekTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (qatariRiyal, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Mexican peso":
                global mexicanPeso
                mexicanPeso -= cekilecekTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (mexicanPeso, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Canadian dollar":
                global canadianDollar
                canadianDollar -= cekilecekTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (canadianDollar, f"{selectedOption.capitalize()}"))
                tablo.commit()
            elif selectedOption.lower().capitalize() == "Kuwaiti dinar":
                global kuwaitiDinar
                kuwaitiDinar -= cekilecekTutar
                cur.execute("""UPDATE Dövizlerimiz
                                   SET value = ?
                                   WHERE name = ?
                                   """, (kuwaitiDinar, f"{selectedOption.capitalize()}"))
                tablo.commit()

            döviz = round((euro * myDatas[0][0]) + (usDollar * myDatas[1][0]) + (britishPound * myDatas[2][0]) + (
                    bulgarianLev * myDatas[3][0]) + (russianRuble * myDatas[4][0]) + (
                                  qatariRiyal * myDatas[5][0]) + (mexicanPeso * myDatas[6][0]) + (
                                  canadianDollar * myDatas[7][0]) + (kuwaitiDinar * myDatas[8][0]), 2)
            toplamVarlıklar = türkLirası + döviz + altın
            etiket3.config(text=f"{round(toplamVarlıklar, 3)} Türk Lirası")
            etiket7.config(text=f"{döviz} Türk Lirası")

            cur.execute("""UPDATE Tarihler
                         SET value = ?
                         WHERE date = ?
                         """, (toplamVarlıklar, f"{formattedDate}"))
            tablo.commit()


        else:

            # Geçersiz seçim mesajı gösterme
            messagebox.showerror("Hata", "Geçersiz seçim!")
    else:
        messagebox.showerror("HATA", "Geçerli Bir Değer Girin")




    if toplamVarlıklar == 0:
        arc = myCanvas.create_arc(coord, start=0, extent=359.99, fill="white")
    else:
        canvasFunc()
    entryDöviz.delete(0, tk.END)
    entryDöviz.insert(0, "Miktar Girin")
    entryDöviz.config(fg="grey")



def butonAltınParaYatır():
    print("altın yatır")

    if entryAltın.get().isdigit() and entryAltın.get() != "0":
        yatirilcakAdet = int(entryAltın.get())
        options = []
        for i in myDatas2:
            options.append(i[0])
        loweroptions = [s.lower() for s in options]

        selectedOption = simpledialog.askstring("Hesaba Yatırılcak Altın",
                                                "Bir seçenek yazın:\n\n" + "\n".join(options))
        print(selectedOption.title())
        if selectedOption.lower() in loweroptions:
            cur.execute("""UPDATE Altınlarımız
                               SET value = ?
                               WHERE name = ?
                               """, (yatirilcakAdet, f"{selectedOption.title()}"))
            tablo.commit()

            if selectedOption.lower() == "gram altın":
                global gramAltin
                gramAltin += yatirilcakAdet
                cur.execute("""UPDATE Altınlarımız
                                              SET value = ?
                                              WHERE name = ?
                                              """, (gramAltin, f"{selectedOption.title()}"))
                tablo.commit()
            elif selectedOption.lower() == "çeyrek altın":
                global ceyrekAltin
                ceyrekAltin += yatirilcakAdet
                cur.execute("""UPDATE Altınlarımız
                                              SET value = ?
                                              WHERE name = ?
                                              """, (ceyrekAltin, f"{selectedOption.title()}"))
                tablo.commit()
            elif selectedOption.lower() == "yarım altın":
                global yarımAltin
                yarımAltin += yatirilcakAdet
                cur.execute("""UPDATE Altınlarımız
                                              SET value = ?
                                              WHERE name = ?
                                              """, (yarımAltin, f"{selectedOption.title()}"))
                tablo.commit()
            elif selectedOption.lower() == "tam altın":
                global tamAltin
                tamAltin += yatirilcakAdet
                cur.execute("""UPDATE Altınlarımız
                                              SET value = ?
                                              WHERE name = ?
                                              """, (tamAltin, f"{selectedOption.title()}"))
                tablo.commit()
            altın = round(
                (gramAltin * myDatas2[0][1]) + (ceyrekAltin * myDatas2[1][1]) + (yarımAltin * myDatas2[2][1]) + (
                            tamAltin * myDatas2[3][1]), 2)

            toplamVarlıklar = türkLirası + döviz + altın
            etiket3.config(text=f"{round(toplamVarlıklar,3)} Türk Lirası")
            etiket9.config(text=f"{altın} Türk Lirası")

            cur.execute("""UPDATE Tarihler
                         SET value = ?
                         WHERE date = ?
                         """, (toplamVarlıklar, f"{formattedDate}"))
            tablo.commit()


        else:

            # Geçersiz seçim mesajı gösterme
            messagebox.showerror("Hata", "Geçersiz seçim!")
    else:
        messagebox.showerror("HATA", "Geçerli Bir Değer Girin")



    canvasFunc()
    entryAltın.delete(0, tk.END)
    entryAltın.insert(0, "Altın Adeti Girin")
    entryAltın.config(fg="grey")
def butonAltınParaCek():
    print("altın çek")

    if entryAltın.get().isdigit() and entryAltın.get() != "0":
        cekilecekAdet = int(entryAltın.get())
        options = []
        for i in myDatas2:
            options.append(i[0])
        loweroptions = [s.lower() for s in options]

        selectedOption = simpledialog.askstring("Hesaptan Çekilecek Altın",
                                                "Bir seçenek yazın:\n\n" + "\n".join(options))
        if selectedOption.lower() in loweroptions:
            if selectedOption.title() == "Gram Altın":
                global gramAltin
                if cekilecekAdet <= gramAltin:
                    gramAltin -= cekilecekAdet
                    cur.execute("""UPDATE Altınlarımız
                                                  SET value = ?
                                                  WHERE name = ?
                                                  """, (gramAltin, f"{selectedOption.title()}"))
                    tablo.commit()

                else:
                    messagebox.showerror("HATA", "Yeterli Para Yok")
            elif selectedOption.title() == "Çeyrek Altın":
                global ceyrekAltin
                if cekilecekAdet <= ceyrekAltin:
                    ceyrekAltin -= cekilecekAdet
                    cur.execute("""UPDATE Altınlarımız
                                                  SET value = ?
                                                  WHERE name = ?
                                                  """, (ceyrekAltin, f"{selectedOption.title()}"))
                    tablo.commit()
                else:
                    messagebox.showerror("HATA", "Yeterli Para Yok")
            elif selectedOption.title() == "Yarım Altın":
                global yarımAltin
                if cekilecekAdet <= yarımAltin:

                    yarımAltin -= cekilecekAdet
                    cur.execute("""UPDATE Altınlarımız
                                                  SET value = ?
                                                  WHERE name = ?
                                                  """, (yarımAltin, f"{selectedOption.title()}"))
                    tablo.commit()
                else:
                    messagebox.showerror("HATA", "Yeterli Para Yok")
            elif selectedOption.title() == "Tam Altın":
                global tamAltin
                if cekilecekAdet <= tamAltin:
                    tamAltin -= cekilecekAdet
                    cur.execute("""UPDATE Altınlarımız
                                                  SET value = ?
                                                  WHERE name = ?
                                                  """, (tamAltin, f"{selectedOption.title()}"))
                    tablo.commit()
                else:
                    messagebox.showerror("HATA", "Yeterli Para Yok")

            altın = round(
                (gramAltin * myDatas2[0][1]) + (ceyrekAltin * myDatas2[1][1]) + (yarımAltin * myDatas2[2][1]) + (
                            tamAltin * myDatas2[3][1]), 2)

            toplamVarlıklar = türkLirası + döviz + altın
            cur.execute("""UPDATE Tarihler
                                       SET value = ?
                                       WHERE date = ?
                                       """, (toplamVarlıklar, f"{formattedDate}"))
            tablo.commit()
            etiket3.config(text=f"{toplamVarlıklar} Türk Lirası")
            etiket9.config(text=f"{altın} Türk Lirası")
        else:

            # Geçersiz seçim mesajı gösterme
            messagebox.showerror("Hata", "Geçersiz seçim!")

    else:
        messagebox.showerror("HATA", "Geçerli Bir Değer Girin")

    if toplamVarlıklar == 0:
        arc = myCanvas.create_arc(coord, start=0, extent=359.99, fill="white")
    else:
        canvasFunc()
    entryAltın.delete(0, tk.END)
    entryAltın.insert(0, "Altın Adeti Girin")
    entryAltın.config(fg="grey")


#Anlık kur gösteren infomessage func
kurlarStr = ""
for i in myDatas:
    kurlarStr += f"{i[1]}:{i[0]}\n"
for i in myDatas2:
    kurlarStr += f"{i[0]} Alış:{i[1]}, Satış:{i[2]}\n"
def showInfoMessage():
    messagebox.showinfo(f"{formattedDate}Tarihi Anlık Kurlar",kurlarStr),


"""
#Açılır Kutu
acilir_kutu = tk.StringVar()
acilir_kutu = ttk.Combobox(
    pencere,
    textvariable=acilir_kutu,
    values=("Euro","US Dollar","British Pound","Bulgarian Lev","Russian Ruble","Qatari Riyal","Mexican Peso","Canadian Dollar","Kuwaiti Dinar"),
    state="readonly"
)
acilir_kutu.grid(row=4,column=2,pady=100)
"""

etiket = tk.Label(
    pencere, #Butonun ekleneceği yer
    text = "Varlıklarım",
    font= customFont,
    fg = "red",



)
etiket2 = tk.Label(
    pencere, #Butonun ekleneceği yer
    text = "Toplam Varlıklarım",
    font= titleFont,
    fg = "black",


)
etiket3 = tk.Label(
    pencere, #Butonun ekleneceği yer
    text = f"{round(toplamVarlıklar,2)} Türk Lirası",
    font= titleFont,
    fg = "black",


)
etiket4 = tk.Label(
    pencere, #Butonun ekleneceği yer
    text = "Türk Lirası",
    font= customFont,
    fg = "#242535",


)
etiket5 = tk.Label(
    pencere, #Butonun ekleneceği yer
    text = f"{türkLirası} Türk Lirası",
    font= customFont,
    fg="#242535",


)
etiket6 = tk.Label(
    pencere, #Butonun ekleneceği yer
    text = "Döviz",
    font= customFont,
    fg = "#242535",


)
etiket7 = tk.Label(
    pencere, #Butonun ekleneceği yer
    text = f"{döviz} Türk Lirası",
    font= customFont,
    fg = "#242535",


)
etiket8 = tk.Label(
    pencere, #Butonun ekleneceği yer
    text = "Altın",
    font= customFont,
    fg="#242535",

)

etiket9 = tk.Label(
    pencere, #Butonun ekleneceği yer
    text = f"{altın} Türk Lirası",
    font= customFont,
    fg = "#242535",


)
etiketDate = tk.Label(
    pencere,
    text=formattedDate,
    font= dateFont,
    fg= "black",
    anchor="s"
)

türkLirasıYatır = tk.Button(
    pencere,
    text= "Türk Lirası Yatır",
    relief="raised",
    command= butonTlParaYatır


)
türkLirasıCek = tk.Button(
    pencere,
    text= "Türk Lirası Çek",
    relief="sunken",
    command= butonTlParaCek

)
dövizYatır = tk.Button(
    pencere,
    text="Döviz Yatır",
    relief="sunken",
    command= butonDovizParaYatır
)
dövizCek = tk.Button(
    pencere,
    text="Döviz Çek",
    relief="sunken",
    command= butonDovizParaCek
)
altınYatır = tk.Button(
    pencere,
    text="Altın Yatır",
    relief="sunken",
    command= butonAltınParaYatır
)
altınCek = tk.Button(
    pencere,
    text="Altın Çek",
    relief="sunken",
    command= butonAltınParaCek
)
renkbilgisi = tk.Label(
    pencere,
    text="Kırmızı: Türk Lirası\nMavi: Döviz\nSarı: Altın",
    font= infoFont,
    fg = "gray"

)

anlikfiyat1 = tk.Label(
    pencere,
    text=f"{myDatas[0][2]}:{myDatas[0][0]}TL"
)
anlikfiyat2 = tk.Label(
    pencere,
    text=f"{myDatas[1][2]}:{myDatas[1][0]}TL"
)

anlikfiyat3 = tk.Label(
    pencere,
    text=f"{myDatas2[0][0]}:{myDatas2[0][1]}TL"
)
anlikfiyat4 = tk.Label(
    pencere,
    text = "her 5saniyede bir yeni üret"
)
anlikfiyatinfo = tk.Button(
    pencere,
    text= "Anlık Kurları Gör",
    bitmap= "info",
    relief="groove",
    compound="left", #bitmap yazının solunda olcak
    borderwidth=10,
    command=showInfoMessage
)

entryTl = tk.Entry(
    pencere,
    width=11,
    border=4,
    borderwidth=1
)
entryDöviz = tk.Entry(
    pencere,
    width=11,
    border = 4,
    borderwidth = 1

)
entryAltın = tk.Entry(
    pencere,
    width=11,
    border=4,
    borderwidth=1,


)
def entryTiklandi(event):
    if entryTl.get() == "Miktar Girin":
        entryTl.delete(0,tk.END)
        entryTl.config(fg="black")
def entryCikildi(event):
    if entryTl.get() != "Miktar Girin":
        entryTl.delete(0, tk.END)
        entryTl.insert(0, "Miktar Girin")
        entryTl.config(fg="grey")
def entryTiklandidoviz(event):
    if entryDöviz.get() == "Miktar Girin":
        entryDöviz.delete(0,tk.END)
        entryDöviz.config(fg="black")
def entryCikildidoviz(event):
    if entryDöviz.get() != "Miktar Girin":
        entryDöviz.delete(0, tk.END)
        entryDöviz.insert(0, "Miktar Girin")
        entryDöviz.config(fg="grey")
def entryTiklandialtin(event):
    if entryAltın.get() == "Altın Adeti Girin":
        entryAltın.delete(0,tk.END)
        entryAltın.config(fg="black")
def entryCikildialtin(event):
    if entryAltın.get() != "Altın Adeti Girin":
        entryAltın.delete(0, tk.END)
        entryAltın.insert(0, "Altın Adeti Girin")
        entryAltın.config(fg="grey")

entryTl.insert(0,"Miktar Girin")
entryTl.config(fg="grey")
entryDöviz.insert(0,"Miktar Girin")
entryDöviz.config(fg="grey")
entryAltın.insert(0,"Altın Adeti Girin")
entryAltın.config(fg="grey")

entryTl.bind('<FocusIn>',entryTiklandi)
entryTl.bind('<FocusOut>',entryCikildi)
entryDöviz.bind('<FocusIn>',entryTiklandidoviz)
entryDöviz.bind('<FocusOut>',entryCikildidoviz)
entryAltın.bind('<FocusIn>',entryTiklandialtin)
entryAltın.bind('<FocusOut>',entryCikildialtin)

#etiket.pack() #Swift silindeki add.subview gibi düşün mutlaka olmalı!
# pack(pady=...) aralara boşluk koyar!

#Total
etiket2.grid(row=0,column=0,padx=25,pady=70)
etiket3.grid(row=0,column=1,padx=25,pady=70)

#Canvas
myCanvas.grid(row=0,column=3,padx=20,pady=70)

#Renk bilgisi
renkbilgisi.grid(row=0,column=2,padx=20,pady=70)

#Tl
etiket4.grid(row=1,column=0,padx=25,pady=15)
etiket5.grid(row=1,column=1,pady=15)
türkLirasıYatır.grid(row=1,column=2,padx=5,pady=15)
türkLirasıCek.grid(row=1,column=3,padx=10,pady=15)

#Döviz
etiket6.grid(row=2,column=0,padx=25,pady=15)
etiket7.grid(row=2,column=1,pady=15)
dövizYatır.grid(row=2,column=2,padx=5,pady=15)
dövizCek.grid(row=2,column=3,padx=10,pady=15)
#Altın
etiket8.grid(row=3,column=0,padx=25,pady=15)
etiket9.grid(row=3,column=1,pady=15)
altınYatır.grid(row=3,column=2,padx=5,pady=15)
altınCek.grid(row=3,column=3,padx=10,pady=15)

#Tarih
etiketDate.grid(row=4,column=0,pady=100)

#Anlık fiyatlar
anlikfiyat1.grid(row=5,column=0,pady=0)
anlikfiyat2.grid(row=5,column=1,pady=0)
anlikfiyat3.grid(row=5,column=2,pady=0)
anlikfiyat4.grid(row=5,column=3,pady=0)
anlikfiyatinfo.grid(row=5,column=4,pady=0)

#Entry
entryTl.grid(row=1,column=4,padx=5,pady=15)
entryDöviz.grid(row=2,column=4,padx=5,pady=15)
entryAltın.grid(row=3,column=4,padx=5,pady=15)


pencere.mainloop() #Pencereyi görebilmemiz için çalışmalı, Her zaman en altta olmalı



"""
if 'result' in jsonData:
    for currency in jsonData['result']:
        currency_code = currency['name']
        currency_value = currency['rate']
        print(f"{currency_code}: {currency_value}")
else:
    print("Sonuç Bulunamadı.")
"""