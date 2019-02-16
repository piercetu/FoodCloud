from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/business')
def business():
    # in here, do log in logic
    return "in business"


if __name__ == "__main__":
    print("Running FoodCloud")
    app.run(host="127.0.0.1", port=5000, debug=True)
