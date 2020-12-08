import argparse
import folium
import json
import os
import requests
import sys

from flask import Flask
from geopy import distance

YANDEX_API_GEO = os.environ.get("YANDEX_API_GEO")
NEAREST_SERVICE_AMOUNT = 5


def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_parsed_service_data(file_path, current_location):
    
    try:
        with open(file_path, "r", encoding="CP1251") as file_context:
            context = json.load(file_context)
    except FileNotFoundError:
        print("File with name {} wasn't found".format(file_path))

    services = []

    for service in context:

        service_latitude = float(service['geoData']['coordinates'][1])
        service_longitude = float(service['geoData']['coordinates'][0])

        service_data = {
            'title': service['Name'],
            'latitude': service_latitude,
            'longitude': service_longitude,
            'distance': distance.distance(
                (current_location['latitude'], current_location['longitude']),
                (service_latitude, service_longitude)).km
        }

        services.append(service_data.copy())
    
    return services


def get_current_location():
    current_location_name = input("Где вы находитесь? ")
    location_coordinates = fetch_coordinates(YANDEX_API_GEO, current_location_name)

    return {
        'latitude': location_coordinates[1],
        'longitude': location_coordinates[0]
    }


def limit_services(services):
    return sorted(
        services,
        key=lambda x: x['distance']
    )[:NEAREST_SERVICE_AMOUNT]


def render_map(current_location, services):
    service_map = folium.Map(
        location=[current_location['latitude'], current_location['longitude']],
        zoom_start=16
    )

    for service in services:
        folium.Marker(
            location=[service['latitude'], service['longitude']]
        ).add_to(service_map)

    service_map.save('index.html')


def index():
    with open('index.html') as file:
        return file.read()


def main():

    parser = argparse.ArgumentParser(
        description="Using data about services from mos.ru script is able to retrieve 5 the most nearest"
    )
    parser.add_argument('-f', '--file_name', help='Path to the file with raw json', required=True)
    args = parser.parse_args()
    file_path = args.file_name

    current_location = get_current_location()
    services = get_parsed_service_data(file_path, current_location) 
    limited_services = limit_services(services)
    render_map(current_location, limited_services)

    app = Flask(__name__)
    app.add_url_rule('/', 'index', index)
    app.run('0.0.0.0')


if __name__ == "__main__":
    main()
