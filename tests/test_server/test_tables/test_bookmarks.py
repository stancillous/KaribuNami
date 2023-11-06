import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.tables.bookmarks import Bookmark, Base
from server.tables.users import User
from server.tables.places import Place

class TestBookmarksTable(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def test_bookmark_creation(self):
        session = self.Session()
        user = User(username='test_user', password='test_password')
        place = Place(
            google_api_place_id='test_place_id',
            name='Test Place',
            rating='4.5',
            open_now='Yes',
            mobile_number='123-456-7890',
            location='Test Location',
            photos='Test Photos',
            reviews='Test Reviews'
        )
        session.add(user)
        session.add(place)
        session.commit()  # Commit the user and place first

        bookmark = Bookmark(
            user_id=user.id,  # Set user_id attribute
            place_id=place.google_api_place_id,  # Set place_id attribute
            bookmarked=1
        )
        session.add(bookmark)  # Add the bookmark to the session
        session.commit()

        retrieved_bookmark = session.query(Bookmark).filter_by(user_id=user.id, place_id=place.google_api_place_id).first()
        self.assertIsNotNone(retrieved_bookmark)
        self.assertEqual(retrieved_bookmark.bookmarked, 1)


    def tearDown(self):
        self.engine.dispose()

if __name__ == '__main__':
    unittest.main()
