import json
import requests
import pprint
import reverse_geocoder as rg
from flask_cors import CORS
import os
from flask import Flask, jsonify, json, request
from geopy.geocoders import Nominatim


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

global entity_type,entity_id

@app.route("/reverse", methods=["GET"])
def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    location = ""
    # result is a list containing ordered dictionary.
    for i in result:
        for key, value in i.items():
            if(key=='name'):
                location = value
    return location
#Developer notes: 
#https://developer.here.com/documentation/geocoder/dev_guide/topics/resource-type-response-geocode.html
#https://developer.here.com/documentation/geocoder/dev_guide/topics/example-location-search-landmark.html
#https://developer.here.com/documentation/geocoder/dev_guide/topics/resource-reverse-geocode.html
#https://developer.here.com/documentation/authentication/dev_guide/topics/api-key-credentials.html
#https://places.sit.ls.hereapi.com/places/v1/discover/search

def get_here_Clinics(latitude, longitude):
    #latitude = "41.8842"
    #longitude = "-87.6388"


    listofClinicsnearby = []
    api_key = 'yourkey'
    #&radius=500&sort=real_distance&order=asc&start=0
    getClinicsFromLatAndLon = 'https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey='+api_key+'&mode=retrieveAddresses&prox='+latitude+','+longitude+',250'
    print(getClinicsFromLatAndLon)
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json"}
    response = requests.get(getClinicsFromLatAndLon, headers=header)
    print(response.json())
    Clinics_info = response.json()["Response"]

    for key,value in Clinics_info.items():
        if(key=='View'):            
            for item in Clinics_info[key][0]["Result"]:
                listofClinicsnearby.append(item["Location"]["Address"]["Label"])
    listofClinicsnearbyjson = {"nearby": [x for x in listofClinicsnearby]}
    return jsonify(listofClinicsnearbyjson)
    #return Clinics_info
   

@app.route("/getlocation", methods=["GET"])
def getlocation():
    lat = request.args['lat']
    lon = request.args['long']
    location = str(lat)+","+str(lon)
    geolocator = Nominatim(user_agent="smart_avatar_application")
    location = geolocator.reverse(location)
    place = location.address
    outputjson = {"place": place.split(',')[0]}

    return jsonify(outputjson)

@app.route("/getClinics", methods=["GET"])
def getClinics():
    #latitude = "41.8842"
    #longitude = "-87.6388"
    latitude = request.args['lat']
    longitude = request.args['long']
    return get_here_Clinics(latitude, longitude)

@app.route("/")
def main():
    return "<h1>OK</h1>"

port = os.getenv('VCAP_APP_PORT', '8080')
if __name__ == "__main__":
  
    app.run(debug=True, host='0.0.0.0', port=port)
    