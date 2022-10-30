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

for line in Content.splitlines():
    if len(line) < 12:
        continue

    # 1000 ile 2029 yıl arası sayı içeren ve işçi, kişi ya da madenci kelimesi geçen
    if re.search("([1][0-9]{3}|20[0-2][0-9])", line) and re.search("(işçi|kişi|madenci)", line):
        year = "Null"
        dead = "Null"
        injured = "Null"
        country = "Null"
        city = "Null"
        name = "Null"

        year = re.findall("([1][0-9]{3}|20[0-2][0-9])", line)[0]
        numberPattern = "([0-9]{1}|[0-9]{2}|[0-9]{3}|[0-9]{4}|[0-9]{5}|[0-9]{6}|[0-9]{1}[.,][0-9]{3}|[0-9]{2}[.,][0-9]{3}|[0-9]{3}[.,][0-9]{3})"
        personPattern = "(kişi|madenci|işçi)"
        try:
            dead = re.findall(
                "\s" + numberPattern + "\s" + personPattern + ".?(hayatını\skaybetti|öldü|ölmüş|ölürken|ölmesi|yaşamını\syit|can\sver)",
                line)[0][0]
        except:
            pass
        print(line)
        print("Yıl:", year, "Ölü:", dead)
        print("-" * 10)