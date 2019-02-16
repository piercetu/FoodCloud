from flask import *
# Flask, render_template, request, 
import requests
import json
import pyrebase

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

        return render_template('search.html', zips=zips)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'
    
    if request.method == 'POST':
        print("***********************************")
        print("received request")
        print("***********************************")
        email = request.form['email']
        print("error email")
        password = request.form['password']
        print("error pw")
        try:
        	auth.sign_in_with_email_and_password(email, password)
        	return render_template('signup.html', s=successful)
        except:
            return render_template('signup.html', us=unsuccessful)

    return render_template('signup.html')


@app.route('/business')
def business():
    # in here, do log in logic
    return render_template('seller.html')


if __name__ == "__main__":
    print("Running FoodCloud")
    app.run(host="127.0.0.1", port=5000)

config = {
    "apiKey": "AIzaSyAAQy9dhBXZwjs79hhWdDl2ROrg394gD58",
    "authDomain": "foodcloud-e429c.firebaseapp.com",
    "databaseURL": "https://foodcloud-e429c.firebaseio.com",
    "projectId": "foodcloud-e429c",
    "storageBucket": "foodcloud-e429c.appspot.com",
    "messagingSenderId": "963030835928"
  }

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Sign up
# email = input('Please enter email\n')
# password = input('Please enter password\n')

# Create user
user = auth.create_user_with_email_and_password(session["email"], session["password"])

# Pass the user's idToken to the push method
auth.get_account_info(user['idToken'])

