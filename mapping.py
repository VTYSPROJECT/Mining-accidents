import folium
import psycopg2
from geopy.geocoders import Nominatim

conn = psycopg2.connect(
   database="VTYS", user='postgres', password='ONURonur44', host='127.0.0.1', port= '5432'
)
m = folium.Map(location=[39.1667, 35.6667], zoom_start=12)

cursor=conn.cursor()
komut_SELECT = "select * from abd_tr_data"
cursor.execute(komut_SELECT)
liste = cursor.fetchall()
def mapping(lat,long,city,olay,ölü,tarih,renk):
   tooltip = "click here"
   iframe=folium.IFrame("<h1><strong>{}</strong></h1><p><br/>"
                         "Kazanın Yaşandığı Tarih : {}<br/>"
                          "Kaza Nedeni : {}<br/>"
                         "Kaza Sonucunda Hayatını Kaybedenlerin Sayısı {}: <br/>"
                         "</p>".format(city,tarih,olay,ölü))
   popup = folium.Popup(iframe,
                        min_width=300,
                        max_width=300)
   folium.Marker(
      [lat, long], popup=popup, tooltip=tooltip,icon=folium.Icon(color=renk)).add_to(m)
def mapping2(lat,long,city,aciklama):
   tooltip = "click here"
   iframe=folium.IFrame("<h1>{}</h1>"
                        "<br/><p>{} {}</p>".format(city,aciklama.split(":")[0],aciklama.split(":")[1]))
   popup = folium.Popup(iframe,
                        min_width=300,
                        max_width=300)
   folium.Marker(
      [lat, long], popup=popup, tooltip=tooltip,color="#ff2400").add_to(m)
def get_cord(city):
   geolocator = Nominatim(user_agent="location script")
   location = geolocator.geocode(city)
   coordinate_values = (location.latitude,location.longitude)
   dicto =coordinate_values
   lat=str(dicto).split("(")[1].split(",")[0]
   long=str(dicto).split("(")[1].split(",")[1].split(")")[0]
   return lat+","+long
renk=""
for i in liste:
    print(i)
    lat=str(i[3]).split(",")[0].split("(")[1].strip()
    long=str(i[3]).split(",")[1].split(")")[0].strip()
    if(int(i[2])> 100):
        renk="darkred"
    elif(50<int(i[2])< 100):
        renk="orange"
    else:
        renk="darkgreen"
    mapping(lat,long,str(i[5]),str(i[1]),str(i[2]),"Bulunamadı" if(str(i[4])==None) else str(i[4]),renk)
m.save('konum.html')
komut_SELECT = "select * from sehir_aciklama"
cursor.execute(komut_SELECT)
liste = cursor.fetchall()
"""for i in liste:
    cord=get_cord(i[1]).split(",")
    lat=cord[0]
    long=cord[1]
    mapping2(lat,long,str(i[1]),str(i[2]))"""
m.save('recep.html')