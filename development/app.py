from flask import *
# Flask, render_template, request, 
import requests
import json
import pyrebase
import request
import win32api

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyAAQy9dhBXZwjs79hhWdDl2ROrg394gD58",
    "authDomain": "foodcloud-e429c.firebaseapp.com",
    "databaseURL": "https://foodcloud-e429c.firebaseio.com",
    "projectId": "foodcloud-e429c",
    "storageBucket": "foodcloud-e429c.appspot.com",
    "messagingSenderId": "963030835928"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

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

        return render_template('search.html', zips=zips)

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print("received request")
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        try:
            auth.create_user_with_email_and_password(email, password)
            #alert("Account Created! :)")
            win32api.MessageBox(0, "Account Created! :)", 'Success')
        except requests.exceptions.HTTPError as e:
            errormsg = str(e)
            err = errormsg.split('{')[2].split(',')[1].split(':')[1].strip().replace("\"", "").replace("_", " ").lower()
            # TODO: Update box - pop up
            win32api.MessageBox(0, err, 'Error')
            return redirect(url_for('signup'))
            
    return render_template('login.html')


@app.route('/business', methods=['POST', 'GET'])
def business():
        if request.method == 'POST':
            print("received request")
            email = request.form['email']
            password = request.form['password']
            print(email, password)
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                win32api.MessageBox(0, "Sign in success! :)", 'Success')
            except requests.exceptions.HTTPError as e:
                errormsg = str(e)
                err = errormsg.split('{')[2].split(',')[1].split(
                    ':')[1].strip().replace("\"", "").replace("_", " ").lower()
                win32api.MessageBox(0, err, 'Error')
                return redirect(url_for('business'))

        return render_template('seller.html')


if __name__ == "__main__":
    print("Running FoodCloud")
    app.run(host="127.0.0.1", port=5000)
