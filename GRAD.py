#!/usr/bin/env python
# coding: utf-8

# # CAR PRICE PREDICTION MODEL #MAIN

# In[1]:


from selenium import webdriver
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

##KUTUPHANELERI IMPORT ETTIK VE KOMUT ISTEMINDEN MODULLERI YUKLEDIK

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.set_window_size(1250,740)
driver.set_window_position(0,0)

##CHROME DRIVERIMIZI YUKLEDIK

#LINKIMIZI BELIRLEDIK HER SAYFA PAGE2-3 DİYE GİTTİĞİ İÇİN PAGE NUMBERS BELIRLEDIK
mainLink = "https://www.arabam.com/ikinci-el"
page_numbers = range(2, 4)
#Şimdilik 2 sayfa üzerinde çalışmak için 2,4 belirledim

#BOS BIR LISTE OLUSTURDUM DATALARI BURADA TUTMAK ICIN
linklist = []

#HER SAYFADA TEK TEK DEVAM EDEBILSIN DIYE PAGE NUMBERS BELIRLEDIM BUNA GÖRE URL DUZENLEYIP O URLYE GIDECEK
#ZATEN URL BELLİ BİR DÜZENDE DEVAM EDİYOR.
for number in page_numbers:
    url = mainLink + '?page=' + str(number)
    driver.get(url)
    sleep(2)
#FONKSIYON OLARAK TAGNAME A OLAN BLOĞUN İÇİNDEKİ LİNKLERİ ALACAK BIR FOR DONGUSU DUZENLEDIM
    def get_links(driver, xpath):
        a = driver.find_element(By.XPATH, '//*[@id="js-hook-missing-space-content"]/div[2]/div[2]')
        lnks = a.find_elements(By.TAG_NAME, "a")
        for lnk in lnks:
            href = lnk.get_attribute("href")
            if href and href not in linklist:
                linklist.append(href)
        return linklist
    #HER LINKTEN 7 ADET OLDUĞU ICIN LISTENIN ICINDE VAR MI VARSA ALMA YOKSA AL GIBI BIR IF ELSE DUZENLEDIM (HER LINKTEN BIR TANE OLMASI ICIN)
    linklist = get_links(driver, '//*[@id="js-hook-missing-space-content"]/div[2]/div[2]')
    
print(linklist)
len(linklist)


# In[2]:


# LINK LISTEMDEKI LINKLERE GIDECEK BIR YAPI INSAA ETMEK ISTIYORUM BU YUZDEN ONCE LINKLERI LISTEMDE KONTROL ETTIM
cardetail = []
for link in linklist:
    # GET METHODUYLA LISTEDEKI LINKLERE SELENIUMU GONDERDIM
    driver.get(link)
    
    #LINKLERIN TITTLELARINI YAZDIRDIM
    #print(driver.title)
    
    
    
    #HTML YAPISI ICINDE LI SPAN OLARAK BULUNAN !BENIM ASIL IHTIYACIM OLAN! DATALARI CEKECEK BIR FOR DONGUSU OLUSTURDUM
    for li in driver.find_elements(By.XPATH, '//*[@id="js-hook-for-observer-detail"]/div[2]'):
        #print(li.text)
        item = li.text
        cardetail.append(item)
        
# Close browser
#element = driver.find_element_by_xpath('//*[@id="js-hook-for-observer-detail"]/div[2]')
 #   print(element.text)


# In[3]:


cardetail


# In[4]:


cardetail[0]


# In[5]:


type(cardetail)


# In[6]:


new_data = []

for item in cardetail:
    # Satırları ayırarak bir liste oluşturdum
    item_list = item.split('\n')
    # Boş olan elemanları listeden çıkardım
    item_list = list(filter(None, item_list))
    # İlan tarihi ve marka değerlerini yeni bir liste olarak ekledim
    new_item = []
    for i in range(0, len(item_list), 2):
        new_item.append(item_list[i])
    # Yeni oluşan listeyi ana listede sakladım
    new_data.append(new_item)
    
# Yeni oluşan liste
print(new_data)


# In[7]:


new_data[0]


# In[8]:


new_data[0][0]


# In[9]:


for data in new_data:
    data[0] = data[0].replace(' TL', '')
    data[8] = data[8].replace(' km', '')
new_data    
    #listedeki bütün fiyatların sonundaki TL stringini kaldırmaya çalışıyorum**


# In[10]:


new_data[0]


# In[11]:


type(new_data)


# In[12]:


from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import pprint
load_dotenv(find_dotenv())

#MongoDB için gerekli kütüphaneler


# In[13]:


password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://emirhanbal:{password}@graduation.r68pz0b.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

#MONGODB ile kodumu ilişkilendirme adımı. burada database'imi bağlıyorum.


# In[14]:


import pymongo

db = client["mydatabase"]
collection = db["mycollection"]

for item in new_data:
    data = {
        "Fiyat":item[0],
        "Adres": item[1],
        "ilan Numarası": item[2],
        "ilan Tarihi" : item[3],
        "Marka" : item[4],
        "Seri" : item[5],
        "Model" : item[6],
        "Yıl" : item[7],
        "Kilometre" : item[8],
        "Vites Tipi" : item[9],
        "Yakıt Tipi": item[10],
        "Kasa Tipi" : item[11],
        "Motor Hacmi" : item[12],
        "Motor Gücü" : item[13],
        "Çekiş" : item[14],
        "Ort. Yakıt Tüketimi" : item[15],
        "Yakıt Deposu" : item[16],
        "Boya-değişen" : item[17],
        "Takasa Uygun" : item[18]
        #"Kimden" : item[19]
        
    }
    collection.insert_one(data)
    
#local variable ve dictionary. burada data tiplerimi ve karşılığında ne olmasını istediğimi belirtiyorum.


# In[15]:


dbs = client.list_database_names()
print(dbs)


# In[16]:


collection.find_one()


# In[17]:


denemeSorgusu = {"Marka" : "Fiat"}
#Marka fiyat filtreleyebilmek için deneme sorgusu


# In[18]:


Marka = input()
Seri = input()
#kullanıcıdan input almak için örnek adım


# In[19]:


denemeSorgusu = {"Marka" : Marka, "Seri" : Seri}
#sorguyu yazdırdım


# In[20]:


for i in collection.find(denemeSorgusu, {"_id":0}):
    print(i)
#kullanıcının inputlarına göre datasetimi sorguladım ve sonuçları doğru ve eksiksiz bir biçimde verdi.


# In[83]:


for document in collection.find():
    if "Fiyat" in document:
        try:
            fiyat = int(document["Fiyat"])
            document["Fiyat"] = fiyat
            # Güncellenmiş belgeyi veritabanına geri kaydedin
            collection.replace_one({"_id": document["_id"]}, document)
        except ValueError:
            pass
        
#bu satır çalışmıyor. burada fiyat datasının tipini integer yapmaya çalıştım ancak olmadı. MongoDB içerisindeki updatelemelerle düzenlemeye çalışacağım.


# In[ ]:




