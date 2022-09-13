import requests
from bs4 import BeautifulSoup as bs
from main.database import Session, Cites


URL = "https://www.hotel24.ru/catalog/russia/162/part/altai_region/9"
r = requests.get(URL)

soup = bs(r.text, "html.parser").find_all('tr')

with Session() as db:
    for i in soup:
        td = i.find_all('td')
        if td != []:
            type_city = td[1].text.strip()
            name_city = td[0].find('a').text.strip()
            type_and_name = f'{name_city} {type_city}'
            new_city = Cites(name_city=type_and_name)
            db.add(new_city)
    db.commit()
print('finish')
