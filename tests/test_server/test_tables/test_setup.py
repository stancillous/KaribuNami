import unittest
from sqlalchemy import create_engine
from sqlalchemy import inspect
from server.tables.setup import engine

class TestSetupTable(unittest.TestCase):
    def test_users_table_exists(self):
        inspector = inspect(engine)
        self.assertIn("users", inspector.get_table_names())

    def test_places_table_exists(self):
        inspector = inspect(engine)
        self.assertIn("places", inspector.get_table_names())

    def test_bookmarks_table_exists(self):
        inspector = inspect(engine)
        self.assertIn("bookmarks", inspector.get_table_names())

if __name__ == '__main__':
    unittest.main()
