import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.tables.places import Place, Base

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

    def tearDown(self):
        self.engine.dispose()

if __name__ == '__main__':
    unittest.main()
