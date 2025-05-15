import os
import time
import threading
import unittest
from werkzeug.security import generate_password_hash
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Uncomment the following line if you need to use ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from app.config import TestConfig
from app import create_app, db
from app.models import User, Entry  # add more models as needed

localhost = "http://127.0.0.1:5000"


class SeleniumTests(unittest.TestCase):
    def _run_app(self):
        self.testApp.run(debug=False, use_reloader=False)
        
    def setUp(self):
        # Create and configure the test app
        self.testApp = create_app(True)
        self.app_context = self.testApp.app_context()
        self.app_context.push()

        # Set up database
        db.create_all()
        
        # Add User, only when testing login functionality
        if self._testMethodName == "test_login_functionality":
            user = User(
                name="Pingu",
                username="pingu",
                age=4,
                gender="male",
                email="pingu@test.com"
            )
            user.password_hash = generate_password_hash("test123")
            db.session.add(user)
            db.session.commit()

        # Add Chrome configurations
        
        # 🔁 Use Thread instead of Process
        self.server_thread = threading.Thread(target=self._run_app)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Wait for server to boot
        time.sleep(2)

        # Initialize Chrome driver
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:5000"
        self.driver.get(localhost)
        return super().setUp()
    
    def tearDown(self):
        # Clean up resources
        self.driver.close()

        # Clear the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        return super().tearDown()
    
    def test_server_running_homepage_loads(self):
        self.driver.get(self.base_url)
        self.assertIn("127.0.0.1:5000", self.driver.current_url)

    def test_login_page(self):
        self.driver.get(self.base_url)  # Go to welcome page

        # Wait and click the button that links to /login
        login_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "login-button")) 
        )
        login_button.click()

        # Confirm redirected to /login
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/login")
        )
        self.assertIn("/login", self.driver.current_url)
    

    def test_signup_page_loads(self):
        self.driver.get(self.base_url)  # Go to welcome page

        # Wait and click the button that links to /signup
        signup_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "signup-button"))
        )
        signup_button.click()

        # Confirm redirected to /signup
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/signup")
        )
        self.assertIn("/signup", self.driver.current_url)
    
    # Testing Signup Functionality
    # This test will create a new user and check if the user is redirected to the login page
    def test_signup_functionality(self):
        # Go to signup page
        self.driver.get(f"{self.base_url}/signup")
        # Fill in the Form
        name_input = self.driver.find_element(By.ID, "name")
        username_input = self.driver.find_element(By.ID, "username")
        age_input = self.driver.find_element(By.ID, "age")
        select = Select(self.driver.find_element(By.ID, "gender"))
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        confirm_password_input = self.driver.find_element(By.ID, "confirm_password")
        submit_button = self.driver.find_element(By.ID, "submit")
        
        name_input.send_keys("Test User")
        username_input.send_keys("testuser")
        age_input.send_keys(25)
        select.select_by_value("male")
        email_input.send_keys("test@test.com")
        password_input.send_keys("test123")
        confirm_password_input.send_keys("test123")
        submit_button.click()
        
        time.sleep(2)
        
        # Check that user is now redirected to login page.
        self.assertIn("/login", self.driver.current_url)
    
    # Testing Login Functionality
    # This test will login and check if the user is redirected to the sleep page.
    def test_login_functionality(self):
        # Go to login page
        self.driver.get(f"{self.base_url}/login")
        
        # Fill in the Form - Using the account "admin"
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "submit")

        email_input.send_keys("pingu@test.com")
        password_input.send_keys("test123")
        submit_button.click()
        
        time.sleep(2)

        # Check that user is now inside sleep page.
        self.assertIn("/sleep", self.driver.current_url)
    
    def test_upload_form_functionality(self):
        pass

if __name__ == "__main__":
    unittest.main()

