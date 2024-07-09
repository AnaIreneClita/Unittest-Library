import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class Test(unittest.TestCase):
    LOGIN_LINK = "https://the-internet.herokuapp.com/login"
    BUTTON_LOGIN = (By.CLASS_NAME, "fa-sign-in")
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.LOGIN_LINK)
        self.driver.maximize_window()
        time.sleep(1)

    def tearDown(self):
        self.driver.quit()


    # TEST 1
    # - Verify that the page URL is correct

    def test_url(self):
        actual_url = self.driver.current_url
        self.assertEqual(self.LOGIN_LINK, actual_url, "Unexpected URL ")


    # TEST 2
    # - Verify that the title is displayed correctly

    def test_title(self):
        expected_title = "The Internet"
        actual_title = self.driver.title

        self.assertEqual(expected_title, actual_title, "Unexpected title")


    # TEST 3
    # - Verify that the text on the element xpath=//h2 is correct

    def test_h2_text(self):
        text_h2 = self.driver.find_element(By.XPATH, "//h2").text
        expected_text = "Login Page"

        self.assertEqual(expected_text, text_h2, "The h2 text is incorrect")


    # TEST 4
    # - Verify that the login button is displayed

    def test_buton_login_displayed(self):
        login_button = self.driver.find_element(*self.BUTTON_LOGIN)
        assert login_button.is_displayed(), "Login button is not displayed"


    # TEST 5
    # - Verify that the attribute href of this link "Elemental Selenium" is correct

    def test_atribut_href(self):
        expected_href = "http://elementalselenium.com/"

        actual_href = self.driver.find_element(By.XPATH, "//a[text()='Elemental Selenium']").get_attribute("href")

        self.assertEqual(expected_href, actual_href, "The'href' link is incorrect")


    # TEST 6
    # - User and pass fields are left empty;
    # - Click login;
    # - Verify that the error is displayed;

    def test_blank_login(self):
        self.driver.find_element(*self.BUTTON_LOGIN).click()
        eroare = self.driver.find_element(By.ID, "flash")
        assert eroare.is_displayed(), "Error is not displayed after leaving Username/Password fields empty"


    # TEST 7
    # - Complete the user and pass fields with invalid data;
    # - Click login;
    # - Verify that the error message is correct;

    def test_invalid_login(self):
        username = self.driver.find_element(*self.USERNAME)
        username.send_keys("wrong_user")
        password = self.driver.find_element(*self.PASSWORD)
        password.send_keys("wrong_password")
        self.driver.find_element(*self.BUTTON_LOGIN).click()
        expected_message = "Your username is invalid!"
        actual_message = self.driver.find_element(By.ID, "flash").text

        self.assertTrue(expected_message in actual_message, "Error message is incorrect!")

    def wait_for_element_to_disappear(self, element_locator, seconds_to_wait):
        wait = WebDriverWait(self.driver, seconds_to_wait)
        return wait.until(EC.none_of(EC.presence_of_element_located(element_locator)))

    def is_element_present(self, locator):
        return len(self.driver.find_elements(*locator)) > 0

    # TEST 8
    # - User and pass fields are left empty;
    # - Click login;
    # - Press x on the error;
    # - Verify that the error disappeared;

    def test_error_message_disappears_on_click(self):
        self.driver.find_element(*self.BUTTON_LOGIN).click()
        self.driver.find_element(By.CLASS_NAME, "close").click()
        self.wait_for_element_to_disappear((By.ID, "flash"), 5) 

        self.assertTrue(not self.is_element_present((By.ID, "flash")), "The error message didn't disappear")