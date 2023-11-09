from flask import Flask, jsonify, render_template, request, redirect
from flask import Flask, jsonify, render_template,request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from server.tables import setup
import json
import requests
import flask

from decouple import config

import smtplib, ssl  # for sending emails

import secrets  # help to generate vefirication link token

from sqlalchemy import ForeignKey, create_engine, Column, Integer
from sqlalchemy import String, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
import logging
from sqlalchemy import inspect, update
import json

app = Flask(__name__)
app.secret_key = 'toosecretive'



# Temporary location data
# To be replaced with geolocation api
sample_location = {"westlands": "-1.2519923507234287, 36.805050379582305", "nyali": "-4.022369424127242, 39.71599235637819", "nakuru": "-0.2889319590806711, 36.06197866570238"}

# Parameters for nearby places api

# LOCATION = sample_location["westlands"]
SEARCH_RADIUS = 2000
API_KEY = "AIzaSyA8SGadbzIoWAW2dMVpL1ktZOIZDMI4QOk"

# nearby_places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword={PLACE}&location={LOCATION}&radius={SEARCH_RADIUS}&type=&key={API_KEY}"

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

# function to check if user is logged in
def checkUserStatus():
    """check if user is in signed in /in session"""
    if 'user_id' in flask.session:
            return True
    return False


maps_url = f'https://www.google.com/maps?q={LATITUDE},{LONGITUDE}'



def sendEmailToUser(receiver_email, verification_link):
    """
    function to send the verification link to a registered user
    Don't change the format of the message variable below (ie it's indentation)
    """

    port = 465  # SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "stancillousray@gmail.com" 
    password = config("mail_key") 
    message = f"""\
Subject: [karibu nami] verify your email address

Hi,

This message is sent from Karibu Nami.

Click on the link below to verify your email address:
{verification_link}

If you did not ask to verify this address, you can ignore this email.

Thanks,
Karibu Nami Team
"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="client")


@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", error="server")


@app.route("/verify_user", strict_slashes=False)
def verify_user():
    """page to verify user after they click
    the verification link sent to their email"""
    verification_link = request.args.get('user_token')

    with Session(setup.engine) as session:
        query = select(setup.User).filter_by(verification_link=verification_link)

        try:
            # get user whose verification link matches the verification_link above
            user = session.scalars(query).one()
            user.email_verified = 1  # set the value to 1 (True), meaning it's been verified
            session.commit()
        
        except Exception as e:
            return render_template("error.html", error="wrong link")

    return render_template("login.html", email_verified=True)


@app.route('/register', methods=['GET', 'POST'])
def register():

    error = None
    if request.method == "GET":
        return render_template("register.html")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            error = "Both passwords should match"
            return render_template("register.html", error=error)
        if len(password) < 6:
            error = "Password should be at least 6 characters long"
            return render_template("register.html", error=error)
        


        verification_token = secrets.token_urlsafe()  # generate a 
        verification_link = f"127.0.0.1:5000/verify_user?user_token={verification_token}"  # link to be sent to the user
        

        # call the function to send the ver_link to the user
        sendEmailToUser(email, verification_link)

        
        hashed_password = generate_password_hash(password, method='sha256')

        # check if username exists
        with Session(setup.engine) as session:
            query = select(setup.User).filter_by(username=username)
            emailquery = select(setup.User).filter_by(email=email)

            # user = session.scalars(query).one()
            user = session.scalars(query).first()

            emailInDatabase = session.scalars(emailquery).first()
            
            # check if username/email exists in our database
            if user:
                error = "Username taken, create a unique username."
                return render_template("register.html", error=error)
            if emailInDatabase:
                error = "Email already in use."
                return render_template("register.html", error=error)
                

        with Session(setup.engine) as session:
            newuser = setup.User(
                username=username,
                password=hashed_password,
                email=email,
                email_verified=False,
                verification_link=verification_token
                )
            session.add(newuser)
            session.commit()
        return render_template("login.html", email_verified=False)
        # return redirect(url_for('login'))
    return jsonify("Sign Up Failed!!!")


@app.route("/resend_link", strict_slashes=False, methods={"POST", "GET"})
def resend_verification_link_to_user():
    """func to handle resending a verification link to the user"""

    if request.method == "GET":
        return render_template("verify.html")
    
    if request.method == "POST":
        user_email = request.form.get("email")
        # check for this email in our database, then create a new verification link,
        # send it to the user and update the vefirication link field in the table

        with Session(setup.engine) as session:
            query = select(setup.User).filter_by(email=user_email)

            try:
                user = session.scalars(query).one()
                # generate a new token for the user and update it in the DB
                verification_token = secrets.token_urlsafe()  # generate a unique token
                verification_link = f"127.0.0.1:5000/verify_user?user_token={verification_token}"  # link to be sent to the user

                user.verification_link = verification_token  # update the value in our database
                session.commit()

                sendEmailToUser(user_email, verification_link)  # send the new verification email to the user
                return render_template("login.html", email_verifed=False)


            except Exception as e:
                print("error is ", e)         
                return "error"
        



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # if login fails, update this and send the error to our front-end
    if request.method == "GET":
        return render_template("login.html", email_verified=True)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with Session(setup.engine) as session:
            query = select(setup.User).filter_by(username=username)

            try:
                user = session.scalars(query).one()

                # print("\t\t\tvalue is ", user.email_verified)
                if not user.email_verified:  # if user email not verified
                    return render_template("login.html", email_verified=False)

                else:  # user email verified
                    if user and check_password_hash(user.password, password):
                        flask.session['user_id'] = user.id
                        flask.session['username'] = user.username
                        
                        # print("LOGIN SUCCESS REDIRECT TO HOME PAGE!!!")
                        return redirect(url_for('home_page'))
                    else:
                        error = 'Login failed. Please check your credentials.'            

            except:
                error = 'Login failed. Please check your credentials.'          
            
                # return jsonify(error)
    return render_template("login.html", error=error, email_verified=True)


@app.route('/', strict_slashes = False)
def home_page():
    """Default home page and more landing page features"""

    # check if user is signed in
    user_authenticated = checkUserStatus()
    return render_template("index.html", user_authenticated=user_authenticated)


places_result = []
# @app.route('/place', strict_slashes=False, methods=["POST", "GET"])
@app.route('/place', strict_slashes=False, methods=["POST"])
def get_places():
    """Returns results for places near the user"""
    PLACE = request.form.get("place_name")
    new_lat = request.form.get("location-lat")
    new_long = request.form.get("location-long")

    LOCATION = "{},{}".format(new_lat, new_long)

    # print("\t\tnew lat is ", new_lat)
    # print("\t\tnew long is ", new_long)
    # print("\t\t\tlocation is ", LOCATION)



    nearby_places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword={PLACE}&location={LOCATION}&radius={SEARCH_RADIUS}&type=&key={API_KEY}"


    # limit results for now to avoid visual clutter
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
        single_place_result["google_api_place_id"] = place_id

        # add a place's total ratings
        # single_place_result["total_ratings"] = user_ratings_total

        # This field is only availabe for signed in users
        if 'user_id' in flask.session:
            single_place_result["bookmarked"] = 0
        
        places_result.append(single_place_result)

        if 'user_id' in flask.session:
            # print("\t\tbefore")
            # print("\t\tuser is ", flask.session['user_id'])
            # print("\t\tusername is ", flask.session['username'])

            # print("\t\tafter")

            user_id = flask.session['user_id']
            with Session(setup.engine) as session:
                query = select(setup.Place).filter_by(google_api_place_id=place_id)
                try: 
                    existing_place = session.scalars(query).one()
                
                except:
                    existing_place = None


                if not existing_place:                    
                    new_place = setup.Place(google_api_place_id=place_id, name=name,   rating=rating, open_now=open_now, mobile_number=contacts, location=maps_url, photos=json.dumps(photographs), reviews=json.dumps(place_reviews))

                    session.add(new_place)
                    session.flush()
                    new_place_id = new_place.google_api_place_id

                    # query = select(setup.User).filter_by(id='user_id')
                    # user = session.scalars(query).one()

                    new_bkmk = setup.Bookmark(user_id=user_id, place_id=new_place_id, bookmarked=0)
                    session.add(new_bkmk)
                    session.commit()
    
    return render_template("places.html", places=places_result)


@app.route("/place/<string:place_id>", strict_slashes=False)
def get_specific_place(place_id):
    # specific_place = [place for place in homeplaces_result if place.get("place_name")==place_name]
    with Session(setup.engine) as session:
        query = select(setup.Place).filter_by(google_api_place_id=place_id)

        place = session.scalars(query).one()

        places_dict = {}
        places_dict["place_name"] = place.name
        places_dict["rating"] = place.rating
        places_dict["open_now"] = place.open_now
        places_dict["mobile_number"] = place.mobile_number
        places_dict["location"] = place.location
        places_dict["photos"] = json.loads(place.photos)
        places_dict["reviews"] = json.loads(place.reviews)
        places_dict["google_api_place_id"] = place.google_api_place_id

        # check if user is signed in or not
        user_authenticated = checkUserStatus()

        # if user is signed in, add this place to the user's recently
        # viewed places

        return render_template("place_details.html", place=places_dict, user_authenticated=user_authenticated)


@app.route("/saved_places", strict_slashes=False)
def saved_places():
    """this should return the places that a signed in user has saved/bookmarked
    """

    if 'user_id' in flask.session:
        # username = flask.session['username'] # this name will be displayed to the user

        print("user id is => ", flask.session['user_id'])

        # print("username is => ", flask.session['username'])
        with Session(setup.engine) as session:
            query = select(setup.Bookmark).filter(setup.Bookmark.user_id == flask.session["user_id"]).filter(setup.Bookmark.bookmarked == 1)

            bookmarks = session.scalars(query).all()

            all_bookmarks = []

            for bookmark in bookmarks:
                qry = select(setup.Place).filter_by(google_api_place_id=bookmark.place_id)

                place = session.scalars(qry).one()

                places_dict = {}
                places_dict["place_name"] = place.name
                places_dict["rating"] = place.rating
                places_dict["open_now"] = place.open_now
                places_dict["mobile_number"] = place.mobile_number
                places_dict["location"] = place.location
                places_dict["photos"] = json.loads(place.photos)
                places_dict["reviews"] = json.loads(place.reviews)
                places_dict["google_api_place_id"] = place.google_api_place_id

                all_bookmarks.append(places_dict)
            
            return render_template("saved_places.html", 
            username=flask.session['username'],
            bookmarks=all_bookmarks,
            len_bookmarks=len(all_bookmarks))
            return jsonify(all_bookmarks)
        
    # if non signed in user tries to access this route, redirect them here
    return redirect(url_for('login'))



@app.route("/bookmark/<place_id>", strict_slashes=False)
def bookmark_place(place_id):
    """Allows user to bookmark a place for future reference"""
    # Check if user is logged in
    if 'user_id' in flask.session:
        # print(f"User is signed in!!!")

        with Session(setup.engine) as session:

            query = select(setup.Bookmark).filter_by(place_id=place_id)

            bkmk = session.scalars(query).one()

            if bkmk.bookmarked == 0:
                # print(f"Place NOT bookmarked!!!")
                bkmk.bookmarked = 1
                session.commit()
                return redirect(url_for('saved_places'))
                return redirect(location="/saved_places")
                return jsonify("Place added to saved places")
            
            else:
                # print(f"Place already BOOKMARKED!!!")
                bkmk.bookmarked = 0
                session.commit()
                return redirect(url_for('saved_places'))
                return redirect(location="/saved_places")
                return jsonify("Place removed from saved places")
    

    return jsonify(f"Sign in to use this feature!!!")

        
@app.route('/logout', strict_slashes=False)
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)