import requests
from bs4 import BeautifulSoup
from csv import writer
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import itertools

#connect to moviesjoy website
response = requests.get('https://moviesjoy.to/home')

soup = BeautifulSoup(response.text, 'html.parser')

#get user to type genre of movie they want
print("Please type a movie genre")
user_input = input()

#movies are contained within this div
movies = soup.find_all('div', class_="flw-item")

#iterate through movies list
for movie in itertools.islice(movies, 0, 10):
    #movie's details
    details = movie.find('div', class_="film-detail film-detail-fix")
    film_name = details.h3.a.text
    #go to a seperate webpage containing info about imdb ratings and movie's genres
    url = movie.div.find('a', href=True)
    if "https:" not in url['href']:
        url = "https://moviesjoy.to" + url['href']
    else:
        url = url['href']

    #prevent successive requests from getting blocked
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response1 = session.get(url)

    soup1 = BeautifulSoup(response1.text, 'html.parser')
    response1.close

    #Creating a list of genres for each movie
    items = soup1.find('div', class_='col-xl-5 col-lg-6 col-md-8 col-sm-12')
    if items is not None:
        elements = items.find_all('a')
        genres = []
        for genre in elements:
            if "genre" in genre['href']:
                genres.append(genre.text)
    
    #return everything if the movie's genre matches with the user's search 
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



