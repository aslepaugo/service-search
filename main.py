import json


with open("data-2897-2019-01-22.json", "r", encoding="CP1251") as bar_file:
    bar_data = json.load(bar_file)

print('Bar name {}'.format(bar_data[0]['Name']))
print('Bar coordinate Latitude: {}'.format(bar_data[0]['geoData']['coordinates'][0]))
print('Bar coordinate Longitude: {}'.format(bar_data[0]['geoData']['coordinates'][1]))
