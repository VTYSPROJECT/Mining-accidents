import re
from bs4 import BeautifulSoup as bs
import requests
from googletrans import Translator

link=input("Site linki girin: ")
r=requests.Session()
req=r.get(link)
soup=bs(req.content.decode("utf-8"), "html.parser")
content=soup.text

with open("Content.txt", "w", encoding="utf-8") as f:
    f.write(content)

#aylar="(Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)"
aylar="(January | February | March |April | May | June | July | August | September | October | November | December)"
#kisi="(işçi|işçiler|madenciler|kişiler|kişi|madenci|insan)"
kisi="( worker | workers | miners | people | person | miner | human )"
#vefat="(hayatını\skaybetti|öldü|ölmüş|ölürken|ölmesi|yaşamını\syitirmiş|yaşamını\syitirdi|can\sverdi|vefat\setti|hayatlarını\kaybetti|öldürdü|ölüm)"
vefat =".*(passed\saway|died|dead|dying|to\sdie|deceased|passed\saway|died|passed\saway|lost\stheir\slives|killed|death|were\skilled)"
result=[]

def cevir():
    trans=Translator()

for line in content.splitlines():
    if (len(line) < 12):
        continue

    if (re.search("([1][0-9]{3}|20[0-2][0-9])", line) and re.search(kisi, line)):
        v_eden="Null"
        tarih  = re.findall("([1][0-9]{3}|20[0-2][0-9])", line)[0]
        sayi = "([0-9] | [1-9][0-9] | [1-9][0-9][0-9] | [1-9][0-9][0-9][0-9])"

        try:
            v_eden=re.findall("\s"+sayi +"\s"+ kisi +"\s"+vefat, line)[0][0]
            if(v_eden=="Null"):
                re.findall("\s"+kisi +"\s"+ sayi, line)[0][0]
            #v_eden=re.findall("[0-9].*"+kisi+".*"+vefat, line)[0][0]
        except:
            pass
        print(line)
        print("tarih : "+tarih+" vefat : "+v_eden)
