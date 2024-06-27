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

    # def go_to_top(self):
    #     return self.driver.execute_script("window.scrollTo(0, 0);")

    def find_and_click_on_element(self, type_of_locator, locator):
        element = self.get_element(type_of_locator, locator)
        self.click_element(element)

    def go_to_bottom(self):
        return self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def login(self):
        element = self.get_element(By.LINK_TEXT, "Войти")
        self.click_element(element)

        self.get_element(By.ID, "username").send_keys(self.default_username)
        self.get_element(By.ID, "password").send_keys(self.default_password)
        element = self.get_element(By.NAME, "login")
        self.click_element(element)

        WebDriverWait(self.driver, 10).until(EC.title_contains("Мой аккаунт"))

        return self.driver

    def login_with_data(self, username, password):
        element = self.get_element(By.LINK_TEXT, "Войти")
        self.click_element(element)

        self.get_element(By.ID, "username").send_keys(username)
        self.get_element(By.ID, "password").send_keys(password)
        element = self.get_element(By.NAME, "login")
        self.click_element(element)

        WebDriverWait(self.driver, 10).until(EC.title_contains("Мой аккаунт"))

        return self.driver

    def logout(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

        time.sleep(2)
        try:
            logout_link = self.get_element(By.LINK_TEXT, "Выйти")
            # print("logout_link -", logout_link.text)
            self.click_element(logout_link)
        except TimeoutException:
            login_link = self.get_element(By.LINK_TEXT, "Войти")

            if login_link:
                return login_link
