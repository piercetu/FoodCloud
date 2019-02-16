import requests
from bs4 import BeautifulSoup
import json

def getzip(zipcode, radius):
    url = "https://www.zipcodeapi.com/rest/RzOSXX9PvVlojd25uKLhCsQs5IByWMJMsFj0Lbt1pRYo1CQSSDeRW2BeLZN69idK/radius.json/{}/{}/mile".format(
        str(zipcode), str(radius))
    source = requests.get(url)
    data = source.text
    zips = json.loads(data)['zip_codes']

    for zipcodes in zips:
        print(zipcodes['zip_code'], zipcodes['distance'])
        
    return(zips)


if __name__ == '__main__':
    print(getzip(46556,3))
