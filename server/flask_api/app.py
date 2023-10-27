from flask import Flask, jsonify, render_template, request, redirect
from server.tables import setup
import requests

from sqlalchemy import ForeignKey, create_engine, Column, Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import inspect



app = Flask(__name__)

# Temporary location data
# To be replaced with geolocation api
sample_location = {"westlands": "-1.2519923507234287, 36.805050379582305", "nyali": "-4.022369424127242, 39.71599235637819", "nakuru": "-0.2889319590806711, 36.06197866570238"}

# Parameters for nearby places api
PLACE = "malls"
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




places_result = []
@app.route('/place', strict_slashes=False)
def get_places():
    """Returns results for places near the user"""
    # limit to 5 results for now to avoid visual clutter
    params = {'limit': 3}

    # Dict containing filtered results
    # places_result = []

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
        loc_lat = location['lat']
        loc_long = location['lng']
        maps_url = f'https://www.google.com/maps?q={loc_lat},{loc_long}'

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
            
            if "photos" in place_id_data["result"]:
                count = 0
                photographs = []
                for photo in place_id_data["result"]["photos"]:
                    if count > 2:
                        break
                    else:
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={MAXWIDTH}&photo_reference={photo['photo_reference']}&key={API_KEY}"
                        photographs.append(photo_url)
                        count += 1

            # get the place's reviews
            place_reviews = []
            if "reviews" in place_id_data["result"]:
                reviews = place_id_data["result"]["reviews"]
                for review in reviews:
                    place_reviews.append({
                        "author_name": review.get("author_name", "name undisclosed"),
                        "author_dp": review.get("profile_photo_url", "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png"),
                        "rating": review.get("rating", 3),
                        "time_posted": review.get("relative_time_description", "a while ago"),
                        "review_text": review.get("text", "No comment")
                    })

        except requests.exceptiomyns.RequestException as e:
            print(f"Request failed: {e}") 

        single_place_result["place_name"] = name
        single_place_result["rating"] = rating
        single_place_result["open_now"] = open_now
        single_place_result["mobile_number"] = contacts
        single_place_result["location"] = maps_url
        single_place_result["photos"] = photographs
        single_place_result["reviews"] = place_reviews
        places_result.append(single_place_result)
    
    return render_template("places.html", places=places_result)
    # return render_template("place_details.html", places=places_result)
    # return jsonify(places_result)
    return render_template("index.html", result=places_result)


@app.route("/place/<string:place_name>", strict_slashes=False)
def get_specific_place(place_name):
    specific_place = [place for place in places_result if place.get("place_name")==place_name]
    return render_template("place_details.html", place=specific_place[0])


@app.route("/saved_places", strict_slashes=False)
def saved_places():
    """this should return the places that a signed in user has saved/bookmarked
        Should get them from the DB, and then pass the json to the template below,
        in the template we'll iterate the saved places and show the user

    """
    return render_template("saved_places.html")


@app.route("/register", methods=["POST", "GET"], strict_slashes=False)
def sign_up():
    """
    this route accepts two methods. if method is GET, we render the register html
    if method is POST, we know it's from a sign up form
    """
    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirm-password")

        if password != confirmPassword:
            # should return an error page, but rn i'm just returning a str
            return "passwords must match"
    
        # ADD USER TO OUR DB BEFORE SENDING THEM TO  THE HOME PAGE
        return redirect(location="/home")


@app.route("/login", methods=["POST", "GET"], strict_slashes=False)
def login():
        
    """
    this route accepts two methods. if method is GET, we render the register html
    if method is POST, we know it's from a login form
    """
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # CHECK IN DB IF THE INPUTS ARE CORRECT BEFORE
        # SENDING THEM TO THE HOME PAGE
    return redirect(location="/home")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)