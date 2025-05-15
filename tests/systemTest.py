import os
import time
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
    def _run_app(self):
        self.testApp.run(debug=False, use_reloader=False)
        
    def setUp(self):
        # Create and configure the test app
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()

        # Set up database
        db.create_all()

        # Add Chrome configurations
        
        # Start the Flask server safely in a subprocess (macOS safe)
        if os.name == 'posix':
            ctx = multiprocessing.get_context("fork")
            self.server_thread = ctx.Process(target=self._run_app, daemon=True)
        else:
            self.server_thread = multiprocessing.Process(target=self._run_app, daemon=True)
        self.server_thread.start()
        
        # Wait for server to boot
        time.sleep(2)

        # Initialize Chrome driver
        self.driver = webdriver.Chrome()
        self.base_url = "http://localhost:5000"
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
    
    def test_server_running(self):
        self.driver.get(self.base_url)
        self.assertIn("localhost:5000", self.driver.current_url)

    def test_server_running_no_auth(self):
        self.driver.get(f"{self.base_url}/")
        self.assertIn("http://localhost:5000", self.driver.current_url)

    def test_homepage_loads(self):
        self.driver.get(self.base_url)
        self.assertIn("localhost:5000", self.driver.current_url)

    def test_login_page(self):
        self.driver.get(f"{self.base_url}/login")
        self.assertIn("/login", self.driver.current_url)

    def test_signup_page_loads(self):
        self.driver.get(f"{self.base_url}/signup")
        self.assertIn("/signup", self.driver.current_url)

    def test_page_has_title(self):
        self.driver.get(f"{self.base_url}/")
        self.assertTrue(len(self.driver.title.strip()) > 0)

    def test_navbar_or_sidebar_present(self):
        self.driver.get(f"{self.base_url}/")
        page_source = self.driver.page_source.lower()
        self.assertTrue("nav" in page_source or "sidebar" in page_source)

    def test_favicon_loads(self):
        """Test if the favicon is accessible."""
        self.driver.get(f"{self.base_url}/favicon.ico")
        self.assertIn("favicon.ico", self.driver.current_url)

    def test_footer_or_content_not_empty(self):
        """Check for a footer tag or that the page isn't empty."""
        self.driver.get(self.base_url)
        content = self.driver.page_source.lower()
        self.assertTrue("footer" in content or len(content.strip()) > 100)

    def test_body_tag_has_text(self):
        """Ensure the <body> element has some visible content."""
        self.driver.get(self.base_url)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertTrue(len(body_text.strip()) > 0)
        
if __name__ == "__main__":
    unittest.main()

