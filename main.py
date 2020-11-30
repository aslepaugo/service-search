import json


with open("data-2897-2019-01-22.json", "r", encoding="CP1251") as bar_file:
    bar_data = json.load(bar_file)

print(type(bar_data))