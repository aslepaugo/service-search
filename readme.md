# Coffee/Bar search

Coffee map with bars and cafes to find nearest place.

Script uses data from CSV file (example is availabel form data.mos.ru)



### How to install

You will need to get Yandex API key [developer.tech.yandex.ru](https://developer.tech.yandex.ru/services/)

Set environmental variable YANDEX_API_GEO

```
export YANDEX_API_GEO=a0270305-....-fa12caad00c
```

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```


### Prepare and run
1. You need a file with data. In example folder you can find file with data about bars of Moscow;
    
    to obtain updated version of the data please visit data.mos.ru

    a) open https://data.mos.ru/opendata

    b) choose category "Food Services"

    c) add filters you need
    
    d) choose export->json

2. Run main.py script with path to your file. 
example:
```
python3 main.py ./example/mos.data.bar.json
```


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).