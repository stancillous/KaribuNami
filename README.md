
## Karibu Nami
##### [Web app link](https://www.botontapwater.tech/)

<h5>Karibu Nami is a web application that is designed to assist travelers, tourists, and anyone exploring new areas who seek quick and user-friendly access to information about local establishments. 
</h5>
<h5>The app aims to address the challenge of efficiently accessing and understanding information about local businesses and services when one visits an unfamiliar place. Current search methods provide information that is often not well visualized and challenging for users to digest and utilize effectively.
</h5>

<h3>Video Demo</h3>


https://github.com/stancillous/KaribuNami/assets/99094257/8cf1b291-42b7-4c5a-870f-50f98e3b99a0


<h3>How to Insall and Run the app</h3>
<h5>The app uses MySQL as the primary database. Before running the app, there are environment variables (all strings), that the app uses and should be kept in a .env file. These are:
</h5>

```
mail_key = password of email used  # This is the app key needed in order to send verification links to users after they register. You can change the email used in the app.py file and include yours, then use the passowrd of that email

The ones below are credentials needed to log in to your MySQL database.

MYSQLUSERNAME =  your MySQL username
PASSWORD = your MYSQL password
HOST = eg localhost
DB = name of the database

```

<h5>With those in place, you can run the app with the following command</h5>

```
python3 -m server.flask_api.app
```


<h5>The server/flask_api/app.py file is the entry point of our app and where our flask routes lie.</h5>
<h5>The different routes available are:</h5>

```
/home page
/places - returns a list of places that the user searched for
/saved_places - stores a list of the places that a signed in user has saved/bookmarked.
/login -  the login page
/verify_user - page to verify that signed up users have clicked on the right verification link
/reset_password - for users who want to change their account password
/resend_link - handles resending a verification link to a user after they’ve signed up
/register - for new users to sign up
/place/place_id - page with more details about a place
/log_out - allows signed in users to log out
/bookmark/place_id - Allows user to bookmark a place for future reference
```
<h3>Tests</h3>
<h5>The unittests are in the /tests directory. You can run the tests with the following command</h5>

```
python3 -m unittest discover tests
```

<h3>How to contribute</h3>

<h5>If you want to contribute to the project and make it better, your help is welcome. Follow the necessary steps when doing that. I'll list them below, but they won't be too detailed.</h5>
<h5> 1. Fork the repository</h5>
<h5> 2. Clone the repo on your local machine</h5>
<h5> 3. Create a branch from which you'll make the changes</h5>
<h5> 4. Make necessary changes and commit them</h5>
<h5> 5. Push your changes to github.</h5>
<h5> 6. Submit a pull request</h5>
<h5> The team will review and merge the changes into the main branch of this project. You will get a notification email once the changes have been merged.</h5>


<h3>Team</h3>

##### [Brandon Munda](https://github.com/Bot-on-Tapwater)
##### [Stancillous Raymond](https://github.com/stancillous)

