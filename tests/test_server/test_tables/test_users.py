import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.tables.users import User, Base

class TestUsersTable(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def test_user_creation(self):
        session = self.Session()
        user = User(username='test_user', password='test_password')
        session.add(user)
        session.commit()

        retrieved_user = session.query(User).filter_by(username='test_user').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.password, 'test_password')

    def tearDown(self):
        self.engine.dispose()

if __name__ == '__main__':
    unittest.main()
