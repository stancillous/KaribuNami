import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from server.tables.bookmarks import Bookmark, Base
# from server.tables.users import User
# from server.tables.places import Place
from server.tables import setup
import logging
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)


class TestBookmarksTable(unittest.TestCase):
    def setUp(self):
        # self.engine = create_engine('sqlite:///:memory:')
        # Base.metadata.create_all(self.engine)
        # self.Session = sessionmaker(bind=self.engine)
        # try:
        #     with Session(setup.engine) as session:
        #         bookmark_to_delete = session.query(Bookmark).filter_by(place_id="test_place_id").first()

        #         session.delete(bookmark_to_delete)
        #         session.commit()

        #         place_to_delete = session.query(setup.Place).filter_by(google_api_place_id="test_place_id").first()

        #         session.delete(place_to_delete)
        #         session.commit()
        # except:
        #     pass
        pass

    def test_bookmark_creation(self):
        with Session(setup.engine) as session:
            user = setup.User(username='test_user', password='test_password')
            place = setup.Place(
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
            print(f"\n***{user.id}***\n")
            print(f"\n***{place.google_api_place_id}***\n")
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
    
    # def test_bookmark_retrieval(self):
    #     with Session(setup.engine) as session:
    #         user = setup.User(username='test_user', password='test_password')
    #         place = setup.Place(
    #             google_api_place_id='test_place_id',
    #             name='Test Place',
    #             rating='4.5',
    #             open_now='Yes',
    #             mobile_number='123-456-7890',
    #             location='Test Location',
    #             photos='Test Photos',
    #             reviews='Test Reviews'
    #         )
    #         session.add(user)
    #         session.add(place)
    #         session.commit()

    #         bookmark = Bookmark(
    #             user_id=user.id,
    #             place_id=place.google_api_place_id,
    #             bookmarked=1
    #         )
    #         session.add(bookmark)
    #         session.commit()

    #         retrieved_bookmark = session.query(Bookmark).filter_by(user_id=user.id, place_id=place.google_api_place_id).first()
    #         self.assertIsNotNone(retrieved_bookmark)
    #         self.assertEqual(retrieved_bookmark.bookmarked, 1)

    # def test_bookmark_update(self):
    #     with Session(setup.engine) as session:
    #         user = setup.User(username='test_user', password='test_password')
    #         place = setup.Place(
    #             google_api_place_id='test_place_id',
    #             name='Test Place',
    #             rating='4.5',
    #             open_now='Yes',
    #             mobile_number='123-456-7890',
    #             location='Test Location',
    #             photos='Test Photos',
    #             reviews='Test Reviews'
    #         )
    #         session.add(user)
    #         session.add(place)
    #         session.commit()

    #         bookmark = Bookmark(
    #             user_id=user.id,
    #             place_id=place.google_api_place_id,
    #             bookmarked=0  # Change to unbookmarked
    #         )
    #         session.add(bookmark)
    #         session.commit()

    #         updated_bookmark = session.query(Bookmark).filter_by(user_id=user.id, place_id=place.google_api_place_id).first()
    #         self.assertEqual(updated_bookmark.bookmarked, 0)

    # def test_bookmark_deletion(self):
    #     with Session(setup.engine) as session:
    #         user = setup.User(username='test_user', password='test_password')
    #         place = setup.Place(
    #             google_api_place_id='test_place_id',
    #             name='Test Place',
    #             rating='4.5',
    #             open_now='Yes',
    #             mobile_number='123-456-7890',
    #             location='Test Location',
    #             photos='Test Photos',
    #             reviews='Test Reviews'
    #         )
    #         session.add(user)
    #         session.add(place)
    #         session.commit()

    #         bookmark = Bookmark(
    #             user_id=user.id,
    #             place_id=place.google_api_place_id,
    #             bookmarked=1
    #         )
    #         session.add(bookmark)
    #         session.commit()

    #         # Delete the bookmark
    #         bookmark_to_delete = session.query(Bookmark).filter_by(user_id=user.id, place_id=place.google_api_place_id).first()
    #         session.delete(bookmark_to_delete)
    #         session.commit()

    #         # Verify the bookmark is deleted
    #         deleted_bookmark = session.query(Bookmark).filter_by(user_id=user.id, place_id=place.google_api_place_id).first()
    #         self.assertIsNone(deleted_bookmark)


    def tearDown(self):
        try:
            with Session(setup.engine) as session:
                bookmark_to_delete = session.query(Bookmark).filter_by(place_id="test_place_id").first()

                session.delete(bookmark_to_delete)
                session.commit()

                place_to_delete = session.query(setup.Place).filter_by(google_api_place_id="test_place_id").first()

                session.delete(place_to_delete)
                session.commit()
        
        except:
            pass

if __name__ == '__main__':
    unittest.main()
