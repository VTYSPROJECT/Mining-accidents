import requests
import bs4
import re
import psycopg2
from googletrans import Translator
from geopy.geocoders import Nominatim
conn = psycopg2.connect(
   database="VTYS", user='postgres', password='ONURonur44', host='127.0.0.1', port= '5432')
cursor=conn.cursor()
req=requests.get("https://en.wikipedia.org/wiki/Mining_accident")
bs_source=bs4.BeautifulSoup(req.content,"html.parser")
a=True
b=True
list=list()
def get_cord(city):
   geolocator = Nominatim(user_agent="location script")
   location = geolocator.geocode(city)
   coordinate_values = (location.latitude,location.longitude)
   dicto =coordinate_values
   lat=str(dicto).split("(")[1].split(",")[0]
   long=str(dicto).split("(")[1].split(",")[1].split(")")[0]
   return lat+","+long

def cevir(sentence):
    translator = Translator()
    sentence = sentence
    trans = translator.translate(sentence, dest="TR").text
    return trans
a=True
b=False
for i in bs_source.find_all('ul'):
    if(a):
        for j in i.find_all_next('li'):
            if("May 25, 1812:" in j.text):
                b=True
            if(b):
                list.append(j.text)
            else:
                pass
            if("October 14, 2022" in j.text):
                a=False
                b=True
                break
    else:
        break
cursor.execute("""Select * from sehir_aciklama""")
sehirs=cursor.fetchall()
print(sehirs)
sehir_loc={}
sehir_acik={}
for i in sehirs:
    try:
        sehir_loc[str(i[1]).strip()]=get_cord(str(i[1]).strip())
        sehir_acik[str(i[1]).strip()]=str(i[2]).strip()
    except:
        sehir_loc[str(i[1]).strip()]=0.0
        sehir_acik[str(i[1]).strip()]=str(i[2]).strip()
        pass
print(sehir_acik)
print(sehir_loc)
script = """INSERT INTO public.sehir_aciklama_wiki(
	sehir,aciklama,location)
	VALUES (%s,%s,%s);"""
for i in sehir_acik.keys():
    print(i)
    cursor.execute(script,(str(i),str(sehir_acik[i]),str(sehir_loc[i]),))
    conn.commit()

