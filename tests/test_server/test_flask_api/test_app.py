import unittest
from flask import Flask
from server.flask_api.app import app
from server.flask_api.app import setup
import logging
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    # def test_register_post(self):
    # # Assuming 'testuser' is a username that already exists in your test database
    #     with app.app_context():
    #         # Check if the user already exists
    #         user_exists = setup.User.query.filter_by(username='testuser').first()

    #         # If the user exists, the registration should fail
    #         if user_exists:
    #             response = self.app.post('/register', data={
    #                 'username': 'testuser',
    #                 'password': 'testpassword',
    #                 'confirm-password': 'testpassword'
    #             })
    #             self.assertEqual(response.status_code, 200)  # Adjust the status code as needed
    #         else:
    #             # If the user doesn't exist, proceed with registration
    #             response = self.app.post('/register', data={
    #                 'username': 'testuser',
    #                 'password': 'testpassword',
    #                 'confirm-password': 'testpassword'
    #             })
    #             self.assertEqual(response.status_code, 302)  # Adjust the status code as needed


    def test_login_post(self):
        response = self.app.post('/login', data={
            'username': 'test_user',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)  # Assuming you're redirecting after login

    def test_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)  # Assuming you're redirecting after logout

    # def test_place(self):
    #     response = self.app.get('/place')
    #     self.assertEqual(response.status_code, 200)

    def test_get_specific_place(self):
        place_id = 'ChIJZzchjUEXLxgRSwVR566d3Ls'
        response = self.app.get(f'/place/{place_id}')
        self.assertEqual(response.status_code, 200)

    def test_saved_places(self):
        response = self.app.get('/saved_places')
        self.assertEqual(response.status_code, 302)  # Assuming you're redirecting if the user is not logged in

    def test_bookmark_place(self):
        place_id = 'ChIJZzchjUEXLxgRSwVR566d3Ls'
        response = self.app.get(f'/bookmark/{place_id}')
        self.assertEqual(response.status_code, 200)  # Assuming you're redirecting after bookmarking

if __name__ == '__main__':
    unittest.main()
