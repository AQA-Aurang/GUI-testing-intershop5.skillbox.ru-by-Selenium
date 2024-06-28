import os
import time
import configparser
from conftest import chrome_browser as driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


def get_element_in_another_element(element, type_of_locator, locator):
    return element.find_element(type_of_locator, locator)


def get_elements_in_another_element(element, type_of_locator, locator):
    return element.find_elements(type_of_locator, locator)


class BasePage:
    def __init__(self, driver):
        self.driver = driver

        config = configparser.ConfigParser()
        config.read('./../config.ini')

        for username, password in config["users"].items():
            if username == "ferdinand":
                self.default_username = username.capitalize()
                self.default_password = password

    def open_page(self, url="https://intershop5.skillbox.ru"):
        self.driver.get(url)

    def get_element(self, type_of_locator, locator):
        return WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((type_of_locator, locator)))

    def get_element_with_te(self, type_of_locator, locator):
        try:
            element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((type_of_locator, locator)))
            return element

        except TimeoutException as t:
            print(f"TimeoutException in getting element - {t.args[0]}")
            return self.driver

    def get_element_lt(self, type_of_locator, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((type_of_locator, locator)))

    def get_element_and_text(self, type_of_locator, locator):
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((type_of_locator, locator)))
        return element, element.text

    def click_element(self, element):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))
        element.click()

    def get_elements(self, type_of_locator, locator):
        return WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((type_of_locator, locator)))

    def get_elements_with_te(self, type_of_locator, locator):
        try:
            elements = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((type_of_locator, locator)))
            return elements

        except TimeoutException as t:
            print(f"TimeoutException in getting elements - {t.args}")
            return WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((type_of_locator, locator)))

    def get_elements_lt(self, type_of_locator, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((type_of_locator, locator)))

    def find_and_click_on_element(self, type_of_locator, locator):
        element = self.get_element(type_of_locator, locator)
        self.click_element(element)

    def go_to_bottom(self):
        return self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def element_should_have_text(self, type_of_locator, locator, text, err_description):
        page_header = self.get_element(type_of_locator, locator)
        print(f"page_header - {page_header.text}, text - {text}")
        assert page_header.text == text, err_description

    def move_down_in_altitude_by(self, point):
        height = self.driver.execute_script("return window.innerHeight;")
        self.driver.execute_script(f"window.scrollTo(0, {height * point});")

    def print_in_field(self, type_of_locator, locator, new_value):
        field = self.get_element(type_of_locator, locator)
        field.clear()
        field.send_keys(new_value)

        return self.driver