import folium
import json
import os
import requests
import sys

from flask import Flask
from geopy import distance
from pprint import pprint

YANDEX_API_GEO = os.environ.get("YANDEX_API_GEO")
NEAREST_BARS_AMOUNT = 5

def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat

def get_bar_distance(navigation_bar):
    return navigation_bar['distance']

def index():
    with open('index.html') as file:
        return file.read()
try:
    with open(sys.argv[1], "r", encoding="CP1251") as bar_file:
        bar_list = json.load(bar_file)
except IndexError:
    print("Please run script with path to the data file")
except FileNotFoundError:
    print("File with name {} wasn't found".format(sys.argv[1]))

place = input("Где вы находитесь? ")
local_coords = fetch_coordinates(YANDEX_API_GEO, place)
local_coords = (float(local_coords[1]), float(local_coords[0]))

navigation_bar_list = []

for bar_data in bar_list:

    bar_limited_data = {
        'title': bar_data['Name'],
        'latitude': bar_data['geoData']['coordinates'][1],
        'longitude': bar_data['geoData']['coordinates'][0],
        'distance': distance.distance(
            local_coords, 
            (bar_data['geoData']['coordinates'][1], bar_data['geoData']['coordinates'][0])).km
    }

    navigation_bar_list.append(bar_limited_data.copy())

bar_resulted_list = sorted(navigation_bar_list, key=get_bar_distance)[:NEAREST_BARS_AMOUNT]

m = folium.Map(
    location=[local_coords[0], local_coords[1]],
    zoom_start=16
)

for bar_data in bar_resulted_list:
    folium.Marker(
        location=[bar_data['latitude'], bar_data['longitude']]
    ).add_to(m)

m.save('index.html')

app = Flask(__name__)
app.add_url_rule('/', 'index', index)
app.run('0.0.0.0')