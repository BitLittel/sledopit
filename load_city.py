import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from main.database import Session, Cites


URL = "https://www.hotel24.ru/catalog/russia/162/part/altai_region/9"
r = requests.get(URL)
print(r.status_code)

soup = bs(r.text, "html.parser").find_all('tr')

with Session() as db:
    for i in soup:
        td = i.find_all('td')
        if td != []:
            type_city = td[1].text.strip()
            name_city = td[0].find('a').text.strip()
            # if type_city == 'село':
            #     type_and_name = f'c.{name_city}'
            #     print(f'c.{name_city}')
            # elif type_city == 'поселок':
            #     type_and_name = f'п.{name_city}'
            #     print(f'п.{name_city}')
            # elif type_city == 'город':
            #     type_and_name = f'г.{name_city}'
            #     print(f'г.{name_city}')
            # elif type_city == 'станция':
            #     type_and_name = f'ст.{name_city}'
            #     print(f'ст.{name_city}')
            # elif type_city == 'деревня':
            #     type_and_name = f'д.{name_city}'
            #     print(f'д.{name_city}')
            # else:
            #     type_and_name = f'{type_city}.{name_city}'
            #     print(f'{type_city}.{name_city}')
            type_and_name = f'{name_city} {type_city}'
            new_city = Cites(name_city=type_and_name)
            db.add(new_city)
    db.commit()
