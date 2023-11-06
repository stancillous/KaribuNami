import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.tables.places import Place, Base
import logging
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)


class TestPlacesTable(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def test_place_creation(self):
        session = self.Session()
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
        session.add(place)
        session.commit()

        retrieved_place = session.query(Place).filter_by(google_api_place_id='test_place_id').first()
        self.assertIsNotNone(retrieved_place)
        self.assertEqual(retrieved_place.name, 'Test Place')
    
    # def test_place_creation_empty_fields(self):
    #     session = self.Session()
        
    #     # Create a place with missing required fields (location and name)
    #     with self.assertRaises(Exception):  # Expect an exception
    #         place = Place(google_api_place_id='test_place_id', rating='4.5')
    #         session.add(place)
    #         session.commit()
        
    #     # Create a place with missing optional fields (photos and reviews)
    #     place = Place(
    #         google_api_place_id='test_place_id',
    #         name='Test Place',
    #         rating='4.5',
    #         open_now='Yes',
    #         mobile_number='123-456-7890',
    #         location='Test Location'
    #     )
    #     session.add(place)
    #     session.commit()
        
    #     # Verify the place is successfully created
    #     retrieved_place = session.query(Place).filter_by(google_api_place_id='test_place_id').first()
    #     self.assertIsNotNone(retrieved_place)

    def test_place_retrieval(self):
        session = self.Session()
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
        session.add(place)
        session.commit()
        
        retrieved_place = session.query(Place).filter_by(google_api_place_id='test_place_id').first()
        self.assertIsNotNone(retrieved_place)
        self.assertEqual(retrieved_place.name, 'Test Place')

    def test_place_update(self):
        session = self.Session()
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
        session.add(place)
        session.commit()
        
        # Update the place's name
        updated_name = 'Updated Place'
        place.name = updated_name
        session.commit()
        
        retrieved_place = session.query(Place).filter_by(google_api_place_id='test_place_id').first()
        self.assertEqual(retrieved_place.name, updated_name)

    def test_place_deletion(self):
        session = self.Session()
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
        session.add(place)
        session.commit()
        
        # Delete the place
        session.delete(place)
        session.commit()
        
        # Attempt to retrieve the deleted place
        retrieved_place = session.query(Place).filter_by(google_api_place_id='test_place_id').first()
        self.assertIsNone(retrieved_place)


    def tearDown(self):
        self.engine.dispose()

if __name__ == '__main__':
    unittest.main()
