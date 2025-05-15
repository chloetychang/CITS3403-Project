import time
import threading
import unittest
from werkzeug.security import generate_password_hash
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app, db
from app.models import User

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
        
        # Add test data to the database
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
        
        # Use Thread instead of Process
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
    
    # Testing if the server is running and the homepage loads
    def test_server_running_homepage_loads(self):
        self.driver.get(self.base_url)
        self.assertIn("127.0.0.1:5000", self.driver.current_url)

    # Testing the button on the welcome page that links to /login
    def test_login_page(self):
        self.driver.get(self.base_url)

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
    
    # Testing the button on the welcome page that links to /signup
    def test_signup_page_loads(self):
        self.driver.get(self.base_url)

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
    
    # Testing Login Functionality
    ## This test will login and check if the user is redirected to the sleep page.
    def test_login_functionality_success(self):
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
        
    ## This test will login with an incorrect password. The user should not be redirected to the sleep page.
    def test_login_invalid_password(self):
        self.driver.get(f"{self.base_url}/login")
        
        self.driver.find_element(By.ID, "email").send_keys("pingu@test.com")
        self.driver.find_element(By.ID, "password").send_keys("wrongpass")          # wrong password
        self.driver.find_element(By.ID, "submit").click()

        time.sleep(1)
        self.assertIn("/login", self.driver.current_url)
        error_flash = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Invalid email or password.')]"))
        )
        self.assertIn("Invalid email or password.", error_flash.text)

    # This test will login with no credentials at all. The user should not be redirected to the sleep page.
    def test_login_missing_fields(self):
        self.driver.get(f"{self.base_url}/login")
        
        self.driver.find_element(By.ID, "email").send_keys("")  # leave blank
        self.driver.find_element(By.ID, "password").send_keys("")  # leave blank
        self.driver.find_element(By.ID, "submit").click()

        time.sleep(1)
        # Check that the URL hasn’t changed because form wasn’t submitted
        self.assertIn("/login", self.driver.current_url)
    
    
    # Testing Signup Functionality
    ## This test will create a new user and check if the user is redirected to the login page
    def test_signup_functionality_success(self):
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
        
     ## This test will not create a new user because the username is already taken. The user should not be redirected to the login page.
    def test_signup_functionality_duplicated_username(self):
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
        username_input.send_keys("pingu")
        age_input.send_keys(25)
        select.select_by_value("male")
        email_input.send_keys("test@test.com")
        password_input.send_keys("test123")
        confirm_password_input.send_keys("test123")
        submit_button.click()
        
        time.sleep(2)
        
        # Check that the URL hasn’t changed because form wasn’t submitted
        self.assertIn("/signup", self.driver.current_url)
        
        error_flash = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Username already taken')]"))
        )
        self.assertIn("Username already taken", error_flash.text)
        
    ## This test will not create a new user because the email is already taken. The user should not be redirected to the login page.
    def test_signup_functionality_duplicated_email(self):
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
        email_input.send_keys("pingu@test.com")
        password_input.send_keys("test123")
        confirm_password_input.send_keys("test123")
        submit_button.click()
        
        time.sleep(2)
        
        # Check that the URL hasn’t changed because form wasn’t submitted
        self.assertIn("/signup", self.driver.current_url)
        
        error_flash = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Email already registered')]"))
        )
        self.assertIn("Email already registered", error_flash.text)
        
    ## With no fields filled in, this test will not create a new user. The user should not be redirected to the login page.
    def test_signup_functionality(self):
        # Go to signup page
        self.driver.get(f"{self.base_url}/signup")
        
        # Form not filled in
        self.driver.find_element(By.ID, "name").send_keys("")
        self.driver.find_element(By.ID, "username").send_keys("")
        self.driver.find_element(By.ID, "age").send_keys("")
        self.driver.find_element(By.ID, "email").send_keys("")
        self.driver.find_element(By.ID, "password").send_keys("")
        self.driver.find_element(By.ID, "confirm_password").send_keys("")
        self.driver.find_element(By.ID, "submit").click()
        
        time.sleep(1)
        # Check that the URL hasn’t changed because form wasn’t submitted
        self.assertIn("/signup", self.driver.current_url)
        
    # Testing upload form functionality
    # This test will check if the upload form will load and submit correctly, when all information is provided.
    def test_upload_form_functionality(self):
        # First, user needs to login (logic as in the test_login_functionality)
        self.driver.get(f"{self.base_url}/login")
        
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "submit")

        email_input.send_keys("pingu@test.com")
        password_input.send_keys("test123")
        submit_button.click()
        
        time.sleep(2)
        
        # Now, go to the upload form
        # Wait and click the button that links to form
        upload_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "upload_button"))
        )
        upload_button.click()
        
        sleep_date_input = self.driver.find_element(By.ID, "entry_date_sleep")
        sleep_time_input = self.driver.find_element(By.ID, "sleep_time")
        wake_date_input = self.driver.find_element(By.ID, "entry_date_wake")
        wake_time_input = self.driver.find_element(By.ID, "wake_time")
        mood_input = self.driver.find_element(By.ID, "mood")
        submit_button = self.driver.find_element(By.ID, "submit")
        
        sleep_date_input.send_keys("30/04/2025")
        self.driver.execute_script("arguments[0].value = '23:00';", sleep_time_input)       # Inject time via JS - Selenium doesn't support time input
        wake_date_input.send_keys("01/05/2025")
        self.driver.execute_script("arguments[0].value = '08:00';", wake_time_input)        # Inject time via JS - Selenium doesn't support time input
        mood_input.send_keys(3)
        submit_button.click()
        
        # Wait for the flash message to appear
        success_flash = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sleep data recorded successfully!')]"))
        )

        # Check its content
        self.assertIn("Sleep data recorded successfully!", success_flash.text)
        
if __name__ == "__main__":
    unittest.main()