import json


with open("data-2897-2019-01-22.json", "r", encoding="CP1251") as bar_file:
    bar_list = json.load(bar_file)

for bar_data in bar_list:

    bar_name = bar_data['Name']
    bar_latitude = bar_data['geoData']['coordinates'][0]
    bar_longitude = bar_data['geoData']['coordinates'][1]

    print("{} {} {}".format(bar_name, bar_latitude, bar_longitude))
