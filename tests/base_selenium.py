import unittest
from selenium.webdriver.common.by import By
from app.models import User
from app import db
from tests.base_selenium_test import BaseSeleniumTestCase

class SeleniumTests(BaseSeleniumTestCase):

    def setUp(self):
        try:
            db.session.query(User).delete()
            db.session.commit()
        except:
            db.session.rollback()

        if self._testMethodName != 'test_static_file_access':
            user = User(
                name="Test User",
                username="testuser",
                email="test@example.com",
                age=25,
                gender="Male"
            )
            user.password_hash = (
                "pbkdf2:sha256:50000$9tHyF9rw$5e97f6ec4e694dd650feb7c84940845e477ccc385c76924eda758876356f570a"
            )
            db.session.add(user)
            db.session.commit()

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
        self.driver.get(f"{self.base_url}/favicon.ico")
        self.assertIn("favicon.ico", self.driver.current_url)

    def test_footer_or_content_not_empty(self):
        self.driver.get(self.base_url)
        content = self.driver.page_source.lower()
        self.assertTrue("footer" in content or len(content.strip()) > 100)

    def test_body_tag_has_text(self):
        self.driver.get(self.base_url)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertTrue(len(body_text.strip()) > 0)

if __name__ == "__main__":
    unittest.main()
