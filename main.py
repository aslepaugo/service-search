from geopy import distance
import json
import os
from pprint import pprint
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


with open("data-2897-2019-01-22.json", "r", encoding="CP1251") as bar_file:
    bar_list = json.load(bar_file)

place = input("Где вы находитесь? ")
local_coords = fetch_coordinates(YANDEX_API_GEO, place)
local_coords = (float(local_coords[1]), float(local_coords[0]))

navigation_bar_list = []
bar_limited_data = dict()

for bar_data in bar_list:

    bar_limited_data['title'] = bar_data['Name']
    bar_limited_data['latitude'] = bar_data['geoData']['coordinates'][1]
    bar_limited_data['longitude'] = bar_data['geoData']['coordinates'][0]
    bar_limited_data['distance'] = distance.distance(local_coords, (bar_data['geoData']['coordinates'][1], bar_data['geoData']['coordinates'][0])).km

    navigation_bar_list.append(bar_limited_data.copy())

pprint(navigation_bar_list)