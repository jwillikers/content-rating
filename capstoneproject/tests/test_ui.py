from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from django.test import Client
from django.contrib.auth.models import User

import re


class TestUI(StaticLiveServerTestCase):


    @classmethod
    def setUpClass(cls):
        cls.user = User.objects._create_user('scott', 'scott@django.com', '1424%Zas')
        cls.c = Client()
        super().setUpClass()
        cls.selenium = WebDriver()  # choose a webdriver to utilize as an API to a browser
        cls.selenium.implicitly_wait(10)


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_login_successful(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name('login_username')
        username_input.send_keys('scott')
        password_input = self.selenium.find_element_by_name('login_password')
        password_input.send_keys('1424%Zas')
        login_button = self.selenium.find_element_by_xpath("//button[@value='login']")
        login_button.click()
        self.assertTrue(self.selenium.find_element_by_link_text("Sign Out"), "Login successful")


    def test_login_unsuccessful(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name('login_username')
        username_input.send_keys('scott')
        password_input = self.selenium.find_element_by_name('login_password')
        password_input.send_keys('1424%Za')
        login_button = self.selenium.find_element_by_xpath("//button[@value='login']")
        login_button.click()
        src = self.selenium.page_source
        text_found = re.search(r'Invalid username or password.', src)
        self.assertNotEqual(text_found, None, "Login unsuccessful")


    def test_signup_successful(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/login/'))
        self.selenium.find_element_by_link_text("Sign Up").click()
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('bill')
        password1_input = self.selenium.find_element_by_name('password1')
        password1_input.send_keys('1r39s4nxwa')
        password2_input = self.selenium.find_element_by_name('password2')
        password2_input.send_keys('1r39s4nxwa')
        signup_button = self.selenium.find_element_by_xpath("//button[@value='signup']")
        signup_button.click()
        self.assertTrue(self.selenium.find_element_by_link_text("Sign Out"), "Signup successful")


    def test_signup_unsuccessful(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/login/'))
        self.selenium.find_element_by_link_text("Sign Up").click()
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('bill')
        password1_input = self.selenium.find_element_by_name('password1')
        password1_input.send_keys('123456')
        password2_input = self.selenium.find_element_by_name('password2')
        password2_input.send_keys('123456')
        signup_button = self.selenium.find_element_by_xpath("//button[@value='signup']")
        signup_button.click()
        self.client.login()
        self.assertFalse(self.client.login(username='bill', password='123456'), "Signup unsuccessful")


    def test_nologin_homepage(self):
        self.selenium.get(self.live_server_url)
        src = self.selenium.page_source
        text_found = re.search(r'Log In or Sign Up', src)
        self.assertNotEqual(text_found, None)


    def test_nologin_profile(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/profile/'))
        src = self.selenium.page_source
        text_found = re.search(r'Log In or Sign Up', src)
        self.assertNotEqual(text_found, None)


    def test_nologin_search(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/search/'))
        src = self.selenium.page_source
        text_found = re.search(r'Log In or Sign Up', src)
        self.assertNotEqual(text_found, None)


    def test_nologin_upload(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/upload/'))
        src = self.selenium.page_source
        text_found = re.search(r'Log In or Sign Up', src)
        self.assertNotEqual(text_found, None)


    def test_nologin_copy(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/copy/'))
        src = self.selenium.page_source
        text_found = re.search(r'Log In or Sign Up', src)
        self.assertNotEqual(text_found, None)


    def test_nologin_words(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/words/'))
        src = self.selenium.page_source
        text_found = re.search(r'Log In or Sign Up', src)
        self.assertNotEqual(text_found, None)
