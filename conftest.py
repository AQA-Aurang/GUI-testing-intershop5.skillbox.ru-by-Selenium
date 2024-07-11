import configparser
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.my_acc_page import MyAccountPage
from pages.catalog_and_subcatalog_page import CatalogAndSubCatalogPage
from pages.product_card_page import ProductCardPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture(scope="module")
def chrome_browser():
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)

    yield wd

    wd.quit()


def get_config():
    config = configparser.ConfigParser()
    config.read('./../config.ini')

    return config


def get_username_password():
    conf = get_config()
    for user, passwrd in conf["users"].items():
        if user == "ferdinand":
            return user.capitalize(), passwrd

username, password = get_username_password()


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

    # time.sleep(2)
    logout_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Выйти")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(logout_link))
    logout_link.click()


# Preparation work function for my_acc_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_account_page(driver):
    acc_page = MyAccountPage(driver)
    acc_page.open_page()

    return acc_page


# Preparation work function for main_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_main_page(driver):
    main_page = MainPage(driver)
    main_page.open_page()

    return main_page


# Preparation work function for catalog_and_subcatalog_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_catalog_and_subcatalog_page(driver):
    catalog_and_sub_catalog_page = CatalogAndSubCatalogPage(driver)
    catalog_and_sub_catalog_page.open_page()

    return catalog_and_sub_catalog_page


# Preparation work function for product_card_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_product_card_page(driver):
    product_card_page = ProductCardPage(driver)
    product_card_page.open_page()

    return product_card_page


# Preparation work function for cart_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_cart_page(driver):
    cart_page = CartPage(driver)
    cart_page.open_page()

    return cart_page


# Preparation work function for checkout_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_checkout_page(driver):
    checkout_page = CheckoutPage(driver)
    checkout_page.additional_setting()
    checkout_page.open_page()

    return checkout_page
