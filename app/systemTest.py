import multiprocessing
import unittest
from selenium import webdriver

# Uncomment the following line if you need to use ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from app.config import TestConfig
from app import create_app, db
from app.models import User, Entry  # add more models as needed

localhost = "http://localhost:5000"


class SeleniumTests(unittest.TestCase):
    def setUp(self):
        # Create and configure the test app
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()

        # Set up database
        db.create_all()

        # Add Chrome configurations

        # Start the Flask server in a separate process
        self.server_thread = multiprocessing.Process(target=self.testApp.run)
        self.server_thread.start()

        # Initialize Chrome driver
        self.driver = webdriver.Chrome()
        self.driver.get(localhost)
        return super().setUp()

    def tearDown(self):
        # Clean up resources
        self.server_thread.terminate()
        self.driver.close()

        # Clear the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        return super().tearDown()
