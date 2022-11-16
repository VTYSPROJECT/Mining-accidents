import re
from bs4 import BeautifulSoup
import requests

UrlLink = input("Site linki girin: ")
Web = requests.Session()

request = Web.get(UrlLink)
soup = BeautifulSoup(request.content.decode("utf-8"), "html.parser")
Content = soup.text.replace("I", "ı").lower()

with open("Content.txt", "w", encoding="utf-8") as f:
    f.write(Content)

result = []
a = False

for line in Content.splitlines():
    if (len(line) < 12):
        continue

    # 1000 ile 2029 yıl arası sayı içeren ve işçi, kişi ya da madenci kelimesi geçen
    if (re.search("([1][0-9]{3}|20[0-2][0-9])", line) and re.search("(işçi|kişi|madenci)", line)):
        v_eden="Null"
        yıl = re.findall("([1][0-9]{3}|20[0-2][0-9])", line)[0]
        if(int(yıl)==1983):
            a=True
        if(a==False):
            continue
        numara = "([0-9]{1}|[0-9]{2}|[0-9]{3}|[0-9]{4}|[0-9]{5}|[0-9]{6}|[0-9]{1}[.,][0-9]{3}|[0-9]{2}[.,][0-9]{3}|[0-9]{3}[.,][0-9]{3})"
        kisi = "(kişi|madenci|işçi|işçinin|işçiyi)"
        sehir="(Adana|Adıyaman|Afyon|Ağrı|Amasya|Ankara|Antalya|Artvin|Aydın|Balıkesir|Bilecik|Bingöl|Bitlis|Bolu|Burdur|Bursa|Çanakkale|Çankırı|Çorum|Denizli|Diyarbakır|Edirne|Elazığ|Erzincan|Erzurum|Eskişehir|Gaziantep|Giresun|Gümüşhane|Hakkari|Hatay|Isparta|İçel (Mersin)|İstanbul|İzmir|Kars|Kastamonu|Kayseri|Kırklareli|Kırşehir|Kocaeli|Konya|Kütahya|Malatya|Manisa|Kahramanmaraş|Mardin|Muğla|Muş|Nevşehir|Niğde|Ordu|Rize|Sakarya|Samsun|Siirt|Sinop|Sivas|Tekirdağ|Tokat|Trabzon|Tunceli|Şanlıurfa|Uşak|Van|Yozgat|Zonguldak|Aksaray|Bayburt|Karaman|Kırıkkale|Batman|Şırnak|Bartın|Ardahan|Iğdır|Yalova|Karabük|Kilis|Osmaniye|Düzce)"
        sehir2=sehir.lower()
        aylar="("+"Ocak"+"|"+"Şubat"+"|"+"Mart"+"|"+"Nisan"+"|"+"Mayıs"+"|"+"Haziran"+"|"+"Temmuz"+"|"+"Ağustos"+"|"+"Eylül"+"|"+"Ekim"+"|"+"Kasım"+"|"+"Aralık"+")"
        ay=r"(\d+) (ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık+)"
        try:
            v_eden = re.findall("\s" + numara + "\s" + kisi + ".?(\söldürdü|shayatını\skaybetti|öldü|ölmüş|ölürken|ölmesi|yaşamını\syit|can\sver)",line)[0][0]
            sehir=re.findall("\s"+sehir,str(line))
            if(sehir.__len__()==0):
                sehir=re.findall("\s"+sehir2,line)[0]
            ay_bul=re.findall(ay,line)
        except:
            pass
        print(line)
        print("Yıl:", yıl,"\nay :",ay_bul[0][1],"\ngün :",ay_bul[0][0], "\nÖlü:", v_eden)
        print(sehir)
        print("-" * 10)