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
    'authorization': "apikey 0o8b4AIoUpmBnQLm8mCOwB:4WX1nyxRV99VnhgsDmM8tr"

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
pencere.geometry("950x720")
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

#Tabloda verimiz varmı yokmu diye kontrol ediyor

cur.execute('''SELECT * FROM Paramız WHERE name = ?''',("Türk Lirası",))
row1 = cur.fetchone()
print(row1)
if row1:
    türkLirası = row1[1]

else:
    cur.execute('''INSERT INTO Paramız(name,value)
    VALUES(?, ?)''',("Türk Lirası",0))
    tablo.commit()


cur.execute('''SELECT * FROM Paramız WHERE name = ?''',("Döviz",))
row2 = cur.fetchone()
print(row2)
if row2:
    döviz = row2[1]

else:
    cur.execute('''INSERT INTO Paramız(name,value)
    VALUES(?, ?)''',("Döviz",0))
    tablo.commit()

cur.execute('''SELECT * FROM Paramız WHERE name = ?''',("Altın",))
row3 = cur.fetchone()
print(row3)
if row3:
    altın = row3[1]

else:
    cur.execute('''INSERT INTO Paramız(name,value)
    VALUES(?, ?)''',("Altın",0))
    tablo.commit()

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






#Her güncellemede çağrılcak func
def canvasFunc():
    arc = myCanvas.create_arc(coord, start=0, extent=((türkLirası * 360) / toplamVarlıklar-0.0001) - 0.0001, fill="red")
    arv2 = myCanvas.create_arc(coord, start=((türkLirası * 360) / toplamVarlıklar - 0.0001),
                               extent=((döviz * 360) / toplamVarlıklar - 0.001), fill="blue")
    arv3 = myCanvas.create_arc(coord, start=((döviz * 360) / toplamVarlıklar - 0.001) + ((türkLirası * 360) / toplamVarlıklar - 0.001)- 0.0001,
                               extent=((altın * 360) / toplamVarlıklar - 0.001)- 0.0001, fill="yellow")



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
        options = []
        for i in myDatas:
            options.append(i[1])
        loweroptions = [s.lower() for s in options]

        selectedOption = simpledialog.askstring("Hesaba Yatırılcak Döviz",
                                                "Bir seçenek yazın:\n\n" + "\n".join(options))
        if selectedOption.lower() in loweroptions:
            print(selectedOption)

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
    options = []
    for i in myDatas:
        options.append(i[1])
    loweroptions = [s.lower() for s in options]

    selectedOption = simpledialog.askstring("Hesaptan Çekilecek Döviz","Bir seçenek yazın:\n\n" + "\n".join(options))
    if selectedOption.lower() in loweroptions:
        print(selectedOption)


    else:

        # Geçersiz seçim mesajı gösterme
        messagebox.showerror("Hata", "Geçersiz seçim!")



    if toplamVarlıklar == 0:
        arc = myCanvas.create_arc(coord, start=0, extent=359.99, fill="white")
    else:
        canvasFunc()
    entryDöviz.delete(0, tk.END)
    entryDöviz.insert(0, "Miktar Girin")
    entryDöviz.config(fg="grey")



def butonAltınParaYatır():
    print("altın yaıtr")

    if entryAltın.get().isdigit() and entryAltın.get() != "0":
        options = []
        for i in myDatas2:
            options.append(i[0])
        loweroptions = [s.lower() for s in options]

        selectedOption = simpledialog.askstring("Hesaba Yatırılcak Altın",
                                                "Bir seçenek yazın:\n\n" + "\n".join(options))
        if selectedOption.lower() in loweroptions:
            print(selectedOption)

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

    options = []
    for i in myDatas2:
        options.append(i[0])
    loweroptions = [s.lower() for s in options]

    selectedOption = simpledialog.askstring("Hesaptan Çekilecek Altın","Bir seçenek yazın:\n\n" + "\n".join(options))
    if selectedOption.lower() in loweroptions:
        print(selectedOption)

    else:

        # Geçersiz seçim mesajı gösterme
        messagebox.showerror("Hata", "Geçersiz seçim!")

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
    text = f"{toplamVarlıklar} Türk Lirası",
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
    fg= "black"
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