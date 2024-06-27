import configparser
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def chrome_browser():
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)

    yield wd

    wd.quit()


# For ordering_page
@pytest.fixture(scope="module")
def chrome_browser_long_timeout():
    wd = webdriver.Chrome()
    wd.implicitly_wait(20)

    # Increase page load timeout to 40 seconds
    wd.set_page_load_timeout(40)

    # Increase JavaScript execution timeout to 20 seconds
    wd.set_script_timeout(20)

    yield wd

    wd.quit()


def get_username_password(config):
    for user, passwrd in config["users"].items():
        if user == "ferdinand":
            return user.capitalize(), passwrd


config = configparser.ConfigParser()
config.read('./../config.ini')
username, password = get_username_password(config)


@pytest.fixture(scope="function")
def login(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Войти"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "login"))).click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт"))

    return driver


@pytest.fixture(scope="function")
def logout(driver):
    yield
    driver.execute_script("window.scrollTo(0, 0);")

    time.sleep(2)
    logout_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Выйти")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(logout_link))
    logout_link.click()
