import unittest
from app import create_app, db
from app.models import User, Entry
from app.config import TestConfig
from datetime import datetime

class TestUpload(unittest.TestCase):
    def setUp(self):
        """ Called before every test method"""
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        """ Called after every test method """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_add_entry_to_form(self):
        """ 
        Test entry creation with sleep and wake time 
        To run test: python -m unittest tests.tests_upload.TestUpload.test_add_entry_to_form
        """
        user = User(user_id="1", name="Skipper", username="skipper", age="35", gender="Male", email="skipper@example.com")
        user.password = "penguins_are_cool"
        db.session.add(user)
        
        other_user = User(user_id="2", name="Private", username="private", age="14", gender="Male", email="private@example.com")
        other_user.password = "lets_go_private"
        db.session.add(other_user)
        
        # Combine date + time for the Entry model
        sleep_datetime = datetime.strptime("2025-05-01 22:00", "%Y-%m-%d %H:%M")
        wake_datetime = datetime.strptime("2025-05-02 06:00", "%Y-%m-%d %H:%M")

        # reate and insert Entry
        entry = Entry(
            user_id=user.user_id,
            sleep_datetime=sleep_datetime,
            wake_datetime=wake_datetime,
            mood = 4
        )
        db.session.add(entry)
        db.session.commit()
        
        # Create and insert Entry - Optional Mood entry
        entry2 = Entry(
            user_id=other_user.user_id,
            sleep_datetime=sleep_datetime,
            wake_datetime=wake_datetime,
        )
        db.session.add(entry2)
        db.session.commit()

        # 4. Verify Both Entries
        retrieved = Entry.query.filter_by(user_id=user.user_id).first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.sleep_datetime, sleep_datetime)
        self.assertEqual(retrieved.wake_datetime, wake_datetime)
        self.assertEqual(retrieved.mood, 4)
        
        retrieved_again = Entry.query.filter_by(user_id=other_user.user_id).first()
        self.assertIsNotNone(retrieved_again)
        self.assertEqual(retrieved_again.sleep_datetime, sleep_datetime)
        self.assertEqual(retrieved_again.wake_datetime, wake_datetime)
        self.assertIsNone(retrieved_again.mood)                                         # Mood should be None since it was not provided
