from flask import Flask
from flask import render_template, redirect
from flask import request
import json
import requests


app = Flask(__name__)


@app.route('/')
def hello_world():

    context = dict()

    return render_template("index.html", **context)


@app.route('/male')
def male():

    context = dict()

    return render_template("male.html", **context)


@app.route('/addBathroom', methods=['GET', 'POST'])
def add_bathroom():

    if request.method == 'POST':
        # Extract data from form
        address = request.form['address']
        openningHour = request.form['openningHour']
        babyChangeRadio = request.form['babyChangeRadio']
        wheelchairFriendlyRadio = request.form['wheelchairRadio']
        accessibilityRadio = request.form['accessibilityRadio']

        gender = request.form.getlist('gender')

        ratingsForBathroom = request.form['ratingsForBathroom']

        # Find lat and lng of address using google map
        address = address.replace(",", " ")
        addressList = address.split()
        addressQuery = ""
        for add in addressList:
            addressQuery += "+"
            addressQuery += add
        addressQuery = addressQuery[1:]
        queryAddress = "https://maps.googleapis.com/maps/api/geocode/json?address=" + addressQuery + "&key=AIzaSyCde1FT2Odgc2S6u5RbkJauf3lXlIOUZU8"

        response = requests.get(queryAddress)
        responseJSON = json.loads(response.text)
        # location = responseJSON['results'][0]['geometry']['location']
        lat = responseJSON['results'][0]['geometry']['location']['lat']
        lng = responseJSON['results'][0]['geometry']['location']['lng']

        print address
        print openningHour
        print babyChangeRadio
        print wheelchairFriendlyRadio
        print accessibilityRadio
        print gender

        print ratingsForBathroom
        print addressQuery

        print lat
        print lng

    context = dict()

    return render_template("addBathroom.html", **context)


if __name__ == '__main__':
    app.run()
