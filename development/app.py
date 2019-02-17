from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import pyrebase
# import win32api

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
db = firebase.database()

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
        url = "https://www.zipcodeapi.com/rest/HBxMce6VETPlGOKfisR4MXrgeQ006chpJ81XcorspiOPDIL4qluy1Ye1md0gxSnC/radius.json/{}/{}/mile".format(
            str(zipcode), str(radius))
        source = requests.get(url)
        data = source.text
        zips = json.loads(data)['zip_codes']
        foodlst = []
        all_users = db.child("users").get()
        for zipp in zips:
            for user in all_users.each():
                try: 
                    if zipp['zip_code'] == user.val()['zipcode']:
                        foodlst.append(user.val())
                except: 
                    continue
        print(foodlst)
        return render_template('customer-view.html', foodlst = foodlst)

@app.route('/signup')
def signup():
    return render_template('business/business-signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print("received request")
        print(str(request))
        companyzip = {}
        companyname = request.form['companyname']
        zipcode = request.form['zipcode']
        companyid = companyname + zipcode
        data = {"name": companyname}

        email = request.form['email']
        password = request.form['password']
        print(email, password)
        try:
            user = auth.create_user_with_email_and_password(email, password)
            # TODO: print message to frontend: account created!
            print("account created!")
        except requests.exceptions.HTTPError as e:
            errormsg = str(e)
            print(errormsg)
            err = errormsg.split('{')[2].split(',')[1].split(':')[1].strip().replace("\"", "").replace("_", " ").lower()
            # TODO:  print message to frontend: err
            print("error: "+str(err))
            return redirect(url_for('signup'))
        results = db.child("users").child(companyid).set(data)
    return render_template('business/business-login.html')


@app.route('/business', methods=['POST', 'GET'])
def business():
    if request.method == 'POST':
        print("received request")
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            errormsg = str(e)
            err = errormsg.split('{')[2].split(',')[1].split(':')[1].strip().replace("\"", "").replace("_", " ").lower()
            return redirect(url_for('business'))

    return render_template('seller.html')

@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'POST':
        companyname = request.form['provider']
        zipcode = request.form['zipcode']
        companyid = companyname + zipcode

        foodname = request.form['foodname']
        price = request.form['price']
        description = request.form['description']
        fooddict = {}
        fooddict[foodname] = (price, description)
        db.child("users").child(companyid).update({"name": companyname, "zipcode": zipcode, "foodname": foodname, "price": price, "description": description})
        # db.child("users").push(data).set(fooddict)
        
    return render_template('success.html')

if __name__ == "__main__":
    print("Running FoodCloud")
    app.run(host="127.0.0.1", port=5000)
