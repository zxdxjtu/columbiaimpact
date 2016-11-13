import pandas as pd
import numpy as np
from pymongo import MongoClient
import json

#df = pd.read_csv('ToiletMap.csv', names=['ToiletID','Address1','Male','Female','Unisex','AccessibleMale','OpenningHoursSchedule','BabyChange','paymentRequired','Latitude','Longitude','rating'])
data = pd.read_csv('ToiletMap.csv')
dataframe = pd.DataFrame(data, columns=['ToiletID','Address1','Male','Female','Unisex','AccessibleMale','OpeningHoursSchedule','BabyChange','PaymentRequired','Latitude','Longitude','rating'])

#client = MongoClient('localhost', 27017)
# db = client.test_database
# collection = db.test_collection
# db.collection.insert_many(frame.to_dict("records"))
#result = collection.insert_many([{'x': i} for i in range(2)])


allBathrooms = []
maleBathRooms = []
femaleBathrooms = []
unisexBathrooms = []

for index, row in dataframe.iterrows():
	if row['Male'] == True:
		maleBathRooms.append(row)
	if row['Female'] == True:
		femaleBathrooms.append(row)
	if row['Unisex'] == True:
		unisexBathrooms.append(row)
	allBathrooms.append(row)

print len(unisexBathrooms)
print unisexBathrooms[0]
print type(unisexBathrooms[0])


# bathrooms = []

# for index, row in dataframe.iterrows():
# 	print row['Male']

