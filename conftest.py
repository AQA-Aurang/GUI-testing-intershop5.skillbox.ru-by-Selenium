import configparser
import pytest
from selenium import webdriver
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage
from pages.my_account_page import MyAccountPage
from pages.catalog_and_category_page import CatalogAndCategoryPage


@pytest.fixture(scope="class")
def chrome_browser(request):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    request.cls.driver = driver

    yield driver

    driver.quit()


def get_config():
    config = configparser.ConfigParser()
    config.read('./../config.ini')

    return config


def get_username_password():
    conf = get_config()
    for user, passwrd in conf["users"].items():
        if user == "ferdinand":
            return user.capitalize(), passwrd


# Preparation work function for main_page
@pytest.fixture(scope="class")
def prepare_main_page(request):
    request.cls.driver.get("https://intershop5.skillbox.ru")
    main_page = MainPage(request.cls.driver)

    return main_page


# Preparation work function for registration_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_registration_page(driver):
    driver.get("http://intershop5.skillbox.ru/register/")
    registration_page = RegistrationPage(driver)

    return registration_page


# Preparation work function for my_acc_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_my_account_page(driver):
    driver.get("https://intershop5.skillbox.ru/my-account/")
    my_acc_page = MyAccountPage(driver)

    return my_acc_page


# Preparation work function for catalog_and_sub_catalog_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_catalog_and_sub_catalog_page(driver):
    driver.get("https://intershop5.skillbox.ru/product-category/catalog/")
    catalog_and_sub_catalog_page = CatalogAndCategoryPage(driver)

    return catalog_and_sub_catalog_page
