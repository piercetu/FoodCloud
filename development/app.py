from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/customer')
def customer():
    return render_template('buyer.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        print("received request")
        zipcode = request.form['zipcode']
        radius = request.form['radius']
        print("{} {}".format(zipcode, radius))
        url = "https://www.zipcodeapi.com/rest/RzOSXX9PvVlojd25uKLhCsQs5IByWMJMsFj0Lbt1pRYo1CQSSDeRW2BeLZN69idK/radius.json/{}/{}/mile".format(
            str(zipcode), str(radius))
        source = requests.get(url)
        data = source.text
        zips = json.loads(data)['zip_codes']

        for zipcodes in zips:
            print(zipcodes['zip_code'], zipcodes['distance'])

        return render_template('search.html', zips)


@app.route('/business')
def business():
    # in here, do log in logic
    return render_template('seller.html')


if __name__ == "__main__":
    print("Running FoodCloud")
    app.run(host="127.0.0.1", port=5000)
