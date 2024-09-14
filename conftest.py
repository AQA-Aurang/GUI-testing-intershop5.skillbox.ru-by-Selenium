import pytest
from selenium import webdriver

from pages.checkout_page import CheckoutPage, adding_anyone_product_in_cart_and_go_to_checkout
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage
from pages.my_account_page import MyAccountPage
from pages.catalog_and_category_page import CatalogAndCategoryPage
from configparser import ConfigParser
from pages.product_card_page import get_any_product_from_catalog, ProductPage
from pages.shopping_cart_page import adding_anyone_product_in_cart, CartPage

BASE_URL = "https://intershop5.skillbox.ru/"


# def pytest_configure(config):
#     config.addinivalue_line("markers", "exp1: experimental mark")


# @pytest.fixture(scope="class", params=[webdriver.Chrome, webdriver.Firefox, webdriver.Edge])
@pytest.fixture(scope="class", params=[webdriver.Chrome])
def chrome_browser(request):
    driver = request.param()
    driver.implicitly_wait(10)
    driver.maximize_window()
    request.cls.driver = driver

    yield driver

    driver.quit()


# @pytest.fixture(scope="class", params=[webdriver.Chrome, webdriver.Firefox, webdriver.Edge])
@pytest.fixture(params=[webdriver.Chrome])
def browser(request):
    driver = request.param()
    driver.implicitly_wait(10)
    driver.maximize_window()
    request.driver = driver

    yield driver

    driver.quit()


def get_config() -> ConfigParser:
    config: ConfigParser = ConfigParser()
    config.read('config.ini')

    return config


def get_username_password() -> tuple[str, str]:
    conf: ConfigParser = get_config()
    for user, passwrd in conf["users"].items():
        if user == "ferdinand":
            return user.capitalize(), passwrd


# Preparation work function for main_page
@pytest.fixture
def main_page(request) -> MainPage:
    request.cls.driver.get(BASE_URL)
    main_page: MainPage = MainPage(request.cls.driver)
    main_page.check_and_go_back_in_main_page()

    return main_page


# Preparation work function for registration_page
@pytest.fixture()
def registration_page(browser) -> RegistrationPage:
    browser.get(BASE_URL + 'register/')
    registration_page: RegistrationPage = RegistrationPage(browser)

    return registration_page


# Preparation work function for my_acc_page
@pytest.fixture()
def my_account_page(request) -> MyAccountPage:
    request.cls.driver.get(BASE_URL + 'my-account/')
    my_acc_page: MyAccountPage = MyAccountPage(request.cls.driver)

    return my_acc_page


@pytest.fixture()
def account_page_with_auth(my_account_page: MyAccountPage) -> MyAccountPage:
    username, password = get_username_password()
    my_account_page.authorisation(username, password)

    return my_account_page


@pytest.fixture()
def account_page_with_auth_and_logout(account_page_with_auth: MyAccountPage) -> MyAccountPage:
    yield account_page_with_auth

    account_page_with_auth.logout_by_link()


# Preparation work function for catalog_and_sub_catalog_page
@pytest.fixture()
def catalog_and_sub_catalog_page(request) -> CatalogAndCategoryPage:
    request.cls.driver.get(BASE_URL + 'product-category/catalog/')
    catalog_and_sub_catalog_page: CatalogAndCategoryPage = CatalogAndCategoryPage(request.cls.driver)

    return catalog_and_sub_catalog_page


# Preparation work function for electronic_sub_catalog_page
@pytest.fixture()
def electronic_sub_catalog_page(request) -> CatalogAndCategoryPage:
    request.cls.driver.get(BASE_URL + 'product-category/catalog/electronics/')
    electronic_sub_catalog: CatalogAndCategoryPage = CatalogAndCategoryPage(request.cls.driver, 'Электроника')

    return electronic_sub_catalog


# Preparation work function for product page
@pytest.fixture()
def product_page(request) -> tuple[ProductPage, str]:
    request.cls.driver.get(BASE_URL + 'product-category/catalog/')
    catalog_and_sub_catalog_page: CatalogAndCategoryPage = CatalogAndCategoryPage(request.cls.driver)
    driver, product_title = get_any_product_from_catalog(catalog_and_sub_catalog_page, 10)
    product: ProductPage = ProductPage(driver, product_title)

    return product, product_title


@pytest.fixture()
def cart_page(catalog_and_sub_catalog_page) -> CartPage:
    driver = adding_anyone_product_in_cart(catalog_and_sub_catalog_page)
    cart_page: CartPage = CartPage(driver)

    return cart_page


@pytest.fixture()
def checkout_page(account_page_with_auth) -> CheckoutPage:
    account_page_with_auth.go_to_catalog_page_from_navbar()
    catalog_and_category_page: CatalogAndCategoryPage = CatalogAndCategoryPage(account_page_with_auth.driver)
    checkout_page: CheckoutPage = adding_anyone_product_in_cart_and_go_to_checkout(catalog_and_category_page)

    yield checkout_page

    checkout_page.logout_by_link()
