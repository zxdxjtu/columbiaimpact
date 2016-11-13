from flask import Flask
from flask import render_template, redirect
from flask import request
import json
import requests
import pandas as pd
import os
import sys
from flask_socketio import SocketIO, send
from random import randrange


reload(sys)
sys.setdefaultencoding('utf8')

# Find root directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')


app = Flask(__name__)

socketio = SocketIO(app)


allBathrooms = []
maleBathrooms = []
femaleBathrooms = []
unisexBathrooms = []


@app.route('/')
def hello_world():

    global allBathrooms
    global maleBathrooms
    global femaleBathrooms
    global unisexBathrooms

    # Read data from file
    allBathrooms, maleBathrooms, femaleBathrooms, unisexBathrooms = read_data()

    context = dict()

    return render_template("index.html", **context)


@app.route('/male')
def male():

    context = dict(maleBathrooms = maleBathrooms[:30])

    return render_template("male.html", **context)

@app.route('/female')
def female():

    context = dict(femaleBathrooms = femaleBathrooms[:30])

    return render_template("female.html", **context)

@app.route('/unisex')
def unisex():

    context = dict(unisexBathrooms = unisexBathrooms[:30])

    return render_template("unisex.html", **context)

@socketio.on('message')
def handle_connected(messagae):
    global maleBathrooms
    global femaleBathrooms
    global unisexBathrooms

    locations = {}
    locations['latitude'] = []
    locations['longitude'] = []
    if messagae == 'Male':
        for bathroom in maleBathrooms[:30]:
            locations['latitude'].append(bathroom['latitude'])
            locations['longitude'].append(bathroom['longitude'])
    elif messagae == 'Female':
        for bathroom in femaleBathrooms[:30]:
            locations['latitude'].append(bathroom['latitude'])
            locations['longitude'].append(bathroom['longitude'])
    elif messagae == 'Unisex':
        for bathroom in unisexBathrooms[:30]:
            locations['latitude'].append(bathroom['latitude'])
            locations['longitude'].append(bathroom['longitude'])

    locationsJSON = json.dumps(locations)
    send(locationsJSON)


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

        male = False
        female = False
        unisex = False
        for entry in gender:
            if entry == 'Male':
                male = True
            if entry == 'Female':
                female = True
            if entry == 'Unisex':
                unisex = True

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


def read_data():
    data = pd.read_csv(os.path.join(APP_STATIC, 'data.csv'))
    dataframe = pd.DataFrame(data, columns=['ToiletID', 'Address1', 'Male', 'Female', 'Unisex', 'AccessibleMale',
                                        'OpeningHoursSchedule', 'BabyChange', 'PaymentRequired', 'Latitude',
                                        'Longitude', 'rating', 'URL'])
    allBathrooms = []
    maleBathRooms = []
    femaleBathrooms = []
    unisexBathrooms = []

    for index, row in dataframe.iterrows():
        toiletID = row['ToiletID']
        AddressOne = row['Address1']
        Male = row['Male']
        Female = row['Female']
        Unisex = row['Unisex']
        WheelchairFriendly = row['AccessibleMale']
        OpeningHours = row['OpeningHoursSchedule']
        BabyChange = row['BabyChange']
        PaymentRequired = row['PaymentRequired']
        Latitude = row['Latitude']
        Longitude = row['Longitude']
        rating = randrange(20, 100, 1) / 10.0
        url = row['URL']

        tempDict = dict(toiletID = toiletID, addressOne = AddressOne, male = Male, female = Female, unisex = Unisex,
                        wheelchairFriendly = WheelchairFriendly, openingHours = OpeningHours, babyChange = BabyChange,
                        paymentRequired = PaymentRequired, latitude = Latitude, longitude = Longitude, rating = rating,
                        url = url)

        if tempDict['male'] == True:
            maleBathRooms.append(tempDict)
        if tempDict['female'] == True:
            femaleBathrooms.append(tempDict)
        if tempDict['unisex'] == True:
            unisexBathrooms.append(tempDict)
        allBathrooms.append(tempDict)

    return allBathrooms, maleBathRooms, femaleBathrooms, unisexBathrooms


if __name__ == '__main__':
    socketio.run(app, debug=True)
