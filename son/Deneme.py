import folium
import psycopg2
from geopy.geocoders import Nominatim

conn = psycopg2.connect(
    database="VTYS", user='postgres', password='ONURonur44', host='127.0.0.1', port='5432'
)
m = folium.Map(location=[39.1667, 35.6667], zoom_start=12)

cursor = conn.cursor()
komut_SELECT = "select * from abd_tr_data ORDER BY sehir ASC"
cursor.execute(komut_SELECT)
liste = cursor.fetchall()


def mapping(lat, long,html, renk):
    tooltip = "click here"
    iframe = folium.IFrame(html)
    popup = folium.Popup(iframe,
                         min_width=400,
                         max_width=400,
                         max_height=300,
                         min_height=300
                         )
    folium.Marker(
        [lat, long], popup=popup, tooltip=tooltip, icon=folium.Icon(color=renk)).add_to(m)


def mapping2(lat, long, city, aciklama):
    tooltip = "click here"
    iframe = folium.IFrame("<h1>{}</h1>"
                           "<p>{} {}</p>".format(city, aciklama.split(":")[0], aciklama.split(":")[1]))
    popup = folium.Popup(iframe,
                         min_width=400,
                         max_width=400)
    folium.Marker(
        [lat, long], popup=popup, tooltip=tooltip, icon=folium.Icon(color="black")).add_to(m)
    #'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray


def get_cord(city):
    geolocator = Nominatim(user_agent="location script")
    location = geolocator.geocode(city)
    coordinate_values = (location.latitude, location.longitude)
    dicto = coordinate_values
    lat = str(dicto).split("(")[1].split(",")[0]
    long = str(dicto).split("(")[1].split(",")[1].split(")")[0]
    return lat + "," + long


renk = ""
sehir = str(liste[0][5])
temp=sehir
lat = str(liste[0][3]).split(",")[0].split("(")[1].strip()
long = str(liste[0][3]).split(",")[1].split(")")[0].strip()
toplam = ""
kont=False
say=1
ölü=0
for i in range(634):
    if(i==633):
        break
    sehir = str(liste[i][5])
    lat = str(liste[i][3]).split(",")[0].split("(")[1].strip()
    long = str(liste[i][3]).split(",")[1].split(")")[0].strip()
    html = "<p>Kazanın Yaşandığı Tarih : {}<br/>" \
           "Kaza Nedeni : {}<br/>" \
           "Kaza Sonucunda Hayatını Kaybedenlerin Sayısı : {} <br/>" \
           "</p>".format("Bulunamadı" if (str(liste[i][4]) == None) else str(liste[i][4]),str(liste[i][1]), str(liste[i][2]))
    if (sehir == str(liste[i+1][5])):
        say+=1
        ölü=ölü+int(liste[i][2])
        toplam=toplam+html
        continue
    else:
        temp_lat=lat
        temp_long=long
        ölü=ölü+int(liste[i][2])
        toplam="<h1><strong>{}</strong></h1>".format(str(liste[i][5]))+toplam+html+"<p><strong>Toplam Ölü Sayısı : {}</strong></p>".format(ölü)

        if (ölü > 100):
            renk = "darkred"
        elif (50 < ölü < 100):
            renk = "orange"
        else:
            renk = "darkgreen"
        mapping(temp_lat,temp_long,toplam, renk)
        ölü=0
        toplam=""
        say=1
        kont=False

komut_SELECT = "select * from sehir_aciklama_wiki"
cursor.execute(komut_SELECT)
liste = cursor.fetchall()
for i in liste:

    cord=str(i[3]).split(",")
    lat=float(cord[0])
    long=float(cord[1])
    mapping2(lat,long,str(i[1]),str(i[2]))

m.get_root().html.add_child(folium.Element(
    """
    <div style="position:fixed;left:800px;top150px;width:200px;height:240px;background-color:white;z-index:900;width: 35%;">
    <p>HTML</p>
<div style="width: 100%;background-color: #ddd;width: 90%; background-color: #04AA6D;  background-position: left;  background-repeat: no-repeat; "class="container">
  <div style="text-align: right;padding-top: 3px;  padding-bottom: 3px;color: white;" class="skills html">90%</div>
</div>

<p>CSS</p>
<div style="width: 100%;background-color: #ddd;width: 80%; background-color: #2196F3;background-position: left;  background-repeat: no-repeat; " class="container">
  <div style="text-align: right;padding-top: 3px;  padding-bottom: 3px;color: white;" class="skills css">80%</div>
</div>

<p>JavaScript</p>
<div style="width: 100%;background-color: #ddd;width: 65%; background-color: #f44336;background-position: left;  background-repeat: no-repeat;" class="container">
  <div style="text-align: right;padding-top: 3px;  padding-bottom: 3px;color: white;" class="skills js">65%</div>
</div>

<p>PHP</p>
<div style="width: 100%;background-color: #ddd;width: 60%; background-color: #808080; background-position: left; background-repeat: no-repeat;" class="container">
  <div style="text-align: right;padding-top: 3px;  padding-bottom: 3px;color: white;" class="skills php">60%</div>
</div>
    </div>
    
    """
))

m.save('Map.html')