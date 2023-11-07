import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.tables.users import User, Base
import logging
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)


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

    def test_user_update(self):
        session = self.Session()
        user = User(username='test_user', password='test_password')
        session.add(user)
        session.commit()
        
        # Update the user's password
        user.password = 'new_password'
        session.commit()
        
        retrieved_user = session.query(User).filter_by(username='test_user').first()
        self.assertEqual(retrieved_user.password, 'new_password')

    def test_user_deletion(self):
        session = self.Session()
        user = User(username='test_user', password='test_password')
        session.add(user)
        session.commit()
        
        # Delete the user
        session.delete(user)
        session.commit()
        
        deleted_user = session.query(User).filter_by(username='test_user').first()
        self.assertIsNone(deleted_user)

    
    # def test_username_uniqueness(self):
    #     session = self.Session()
    #     user1 = User(username='test_user', password='test_password')
    #     user2 = User(username='test_user', password='another_password')
    #     session.add(user1)
    #     session.commit()
        
    #     with self.assertRaises(Exception):  # Expect a constraint violation error
    #         session.add(user2)
    #         session.commit()

    # def test_invalid_user_creation(self):
    #     session = self.Session()
        
    #     # Create a user with an empty username
    #     with self.assertRaises(Exception):  # Expect an exception
    #         user = User(username='', password='test_password')
    #         session.add(user)
    #         session.commit()
        
    #     # Create a user with an empty password
    #     with self.assertRaises(Exception):  # Expect an exception
    #         user = User(username='test_user', password='')
    #         session.add(user)
    #         session.commit()

    # def test_user_retrieval(self):
    #     session = self.Session()
    #     user = User(username='test_user', password='test_password')
    #     session.add(user)
    #     session.commit()
        
    #     retrieved_user = session.query(User).filter_by(id=user.id).first()
    #     self.assertIsNotNone(retrieved_user)
    #     self.assertEqual(retrieved_user.username, 'test_user')

    def test_session_management(self):
        session = self.Session()
        
        # Create multiple users in a single session
        user1 = User(username='user1', password='password1')
        user2 = User(username='user2', password='password2')
        session.add(user1)
        session.add(user2)
        session.commit()
        
        # Verify the state of the database
        users = session.query(User).all()
        self.assertEqual(len(users), 2)
        
        # Close the session and open a new one
        session.close()
        session = self.Session()
        
        # Verify that the previous changes are still committed
        users = session.query(User).all()
        self.assertEqual(len(users), 2)

    # def test_user_validation(self):
    #     session = self.Session()
        
    #     # Create a user with an invalid username (empty)
    #     with self.assertRaises(Exception):  # Expect an exception
    #         user = User(username='', password='test_password')
    #         session.add(user)
    #         session.commit()
        
    #     # Create a user with an invalid password (empty)
    #     with self.assertRaises(Exception):  # Expect an exception
    #         user = User(username='test_user', password='')
    #         session.add(user)
    #         session.commit()

    # def test_unique_constraints(self):
    #     session = self.Session()
        
    #     # Create two users with the same username
    #     user1 = User(username='test_user', password='password1')
    #     user2 = User(username='test_user', password='password2')
    #     session.add(user1)
        
    #     with self.assertRaises(Exception):  # Expect a constraint violation error
    #         session.add(user2)
    #         session.commit()



    def tearDown(self):
        self.engine.dispose()

if __name__ == '__main__':
    unittest.main()
