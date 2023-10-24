from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

app = Flask(__name__)

# Temporary location data
# To be replaced with geolocation api
sample_location = {"westlands": "-1.2519923507234287, 36.805050379582305", "nyali": "-4.022369424127242, 39.71599235637819", "nakuru": "-0.2889319590806711, 36.06197866570238"}

# Parameters for nearby places api
PLACE = "Barbershop"
LOCATION = sample_location["westlands"]
SEARCH_RADIUS = 2000
API_KEY = "AIzaSyA8SGadbzIoWAW2dMVpL1ktZOIZDMI4QOk"

nearby_places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword={PLACE}&location={LOCATION}&radius={SEARCH_RADIUS}&type=&key={API_KEY}"

# Parameters for place details api
PLACE_ID = ""

place_details_url = f"https://maps.googleapis.com/maps/api/place/details/json?placeid={PLACE_ID}&fields=&key={API_KEY}"

#Parameters for places photos api
MAXWIDTH = 400
PHOTO_REFERENCE = ""

places_photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={MAXWIDTH}&photo_reference={PHOTO_REFERENCE}&key={API_KEY}"

#Parameters for google maps location HTTP request
LATITUDE = ""
LONGITUDE = ""

maps_url = f'https://www.google.com/maps?q={LATITUDE},{LONGITUDE}'


@app.route('/home', strict_slashes = False)
def home_page():
    """Default home page and more landing page features"""
    search_bar = "***SEARCH BAR WILL BE RIGHT HERE***"
    return jsonify(search_bar)

@app.route('/place', strict_slashes = False)
def get_places():
    """Returns results for places near the user"""
    # limit to 5 results for now to avoid visual clutter
    params = {'limit': 3}

    # Dict containing filtered results
    places_result = []

    # Make a GET request to API
    try:
        response = requests.get(nearby_places_url, params=params)
        response.raise_for_status()
        nearby_places_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    # Filter results
    nearby_places = nearby_places_data["results"]

    for place in nearby_places:
        single_place_result = {}
        name = place["name"]
        place_id = place["place_id"]
        rating = place["rating"]
        location = place["geometry"]['location']

        # Get contact info and open/close status from places details api
        try:
            PLACE_ID = place_id

            # This is a repetition of the URL provided above, resolve duplicates
            response = requests.get(f"https://maps.googleapis.com/maps/api/place/details/json?placeid={PLACE_ID}&fields=&key={API_KEY}")
            response.raise_for_status()
            place_id_data = response.json()

            if "formatted_phone_number" in place_id_data["result"]:
                contacts = place_id_data["result"]["formatted_phone_number"]
            else:
                contacts = None
            
            if "current_opening_hours" in place_id_data["result"]:
                if "open_now" in place_id_data["result"]["current_opening_hours"]:
                    open_now = place_id_data["result"]["current_opening_hours"]["open_now"]
                else:
                    open_now = None
            else:
                open_now = None
            # contacts = place_id_data["result"]["formatted_phone_number"]
            # open_now = place_id_data["result"]["current_opening_hours"]["open_now"]
            # print(f"\n{place_id_data['result']['formatted_phone_number']}\t")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}") 

        # places_result.append(f"***\nname: {name}\nplace_id: {place_id}\nrating: {rating}\nlocation: {location}\ncontacts: {contacts}\nopen_now: {open_now}***")
        single_place_result["name"] = name
        single_place_result["rating"] = rating
        single_place_result["open_now"] = open_now
        single_place_result["mobile_number"] = contacts
        places_result.append(single_place_result)
        

        # places_result.append(f"***\nname: {name}\nplace_id: {place_id}\nrating: {rating}\nlocation: {location}***")
    
    return jsonify(places_result)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)