import json
import os
import requests


YANDEX_API_GEO = os.environ.get("YANDEX_API_GEO")

def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


place = input("Где вы находитесь? ")
coords = fetch_coordinates(YANDEX_API_GEO, place)
print(coords)

exit()

with open("data-2897-2019-01-22.json", "r", encoding="CP1251") as bar_file:
    bar_list = json.load(bar_file)

for bar_data in bar_list:

    bar_name = bar_data['Name']
    bar_latitude = bar_data['geoData']['coordinates'][0]
    bar_longitude = bar_data['geoData']['coordinates'][1]

    print("{} {} {}".format(bar_name, bar_latitude, bar_longitude))



