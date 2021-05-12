import requests
from bs4 import BeautifulSoup
from csv import writer
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import itertools

response = requests.get('https://moviesjoy.to/home')

soup = BeautifulSoup(response.text, 'html.parser')

user_input = input()

movies = soup.find_all('div', class_="flw-item")
for movie in itertools.islice(movies, 0, 10):
    details = movie.find('div', class_="film-detail film-detail-fix")
    film_name = details.h3.a.text
    #print(film_name)
    url = movie.div.find('a', href=True)
    if "https:" not in url['href']:
        url = "https://moviesjoy.to" + url['href']
    else:
        url = url['href']

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response1 = session.get(url)

    soup1 = BeautifulSoup(response1.text, 'html.parser')
    response1.close

    items = soup1.find('div', class_='col-xl-5 col-lg-6 col-md-8 col-sm-12')
    if items is not None:
        elements = items.find_all('a')
        genres = []
        for genre in elements:
            if "genre" in genre['href']:
                genres.append(genre.text)

    for genre in genres:
        if genre == user_input:
            print(film_name)
            for genre in genres:
                print(genre)
            rating = soup1.find('button', class_="btn btn-sm btn-radius btn-warning btn-imdb")
            if rating is not None:
                rating = rating.text
                print(rating)
            print("_______________________")



