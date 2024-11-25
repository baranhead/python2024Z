import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get("https://www.mimuw.edu.pl/")

#sprawdzamy, czy udalo sie pobrac strone
if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, 'html.parser')

    #znajdujemy aktualnosci
    div = soup.find('div', class_='info-grid news-grid')
    
    #znajdujemy tytuly i daty
    titles = div.find_all('h3')
    dates = div.find_all('div', class_='info-item-text-date')

    #tworzymy liste slownikow
    events = [
    {"title": title.get_text(strip=True), "date": date.get_text(strip=True)}
    for title, date in zip(titles, dates)
    ]

    #wypisujemy wydarzenia
    for item in events:
        print(item)

    # zapis do csv przy uzyciu pandas
    df = pd.DataFrame.from_dict(events)
    csv_filename = "events.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8')

    print(f"\nDane zostały zapisane w pliku {csv_filename}")
    

else:
    print(f"Nie udało się pobrać strony. Status: {response.status_code}")