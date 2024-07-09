import pytest
from pages.base_types import PageWithChromeBrowser, PageWithChromeBrowserLongTimeout
from .conftest import chrome_browser as driver
from .conftest import chrome_browser_long_timeout as driver_lt
from pages.my_acc_page import MyAccountPage
from pages.main_page import MainPage
from pages.catalog_and_subcatalog_page import CatalogAndSubCatalogPage
from pages.product_card_page import ProductCardPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


# Preparation work function for my_acc_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_account_page(driver):
    instance = PageWithChromeBrowser(driver)
    acc_page = MyAccountPage(instance)
    acc_page.open_page()

    return acc_page


# Preparation work function for main_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_main_page(driver):
    instance = PageWithChromeBrowser(driver)
    main_page = MainPage(instance)
    main_page.open_page()

    return main_page


# Preparation work function for catalog_and_subcatalog_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_catalog_and_subcatalog_page(driver):
    instance = PageWithChromeBrowser(driver)
    catalog_and_sub_catalog_page = CatalogAndSubCatalogPage(instance)
    catalog_and_sub_catalog_page.open_page()

    return catalog_and_sub_catalog_page


# Preparation work function for product_card_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_product_card_page(driver):
    instance = PageWithChromeBrowser(driver)
    product_card_page = ProductCardPage(instance)
    product_card_page.open_page()

    return product_card_page


# Preparation work function for cart_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_cart_page(driver):
    instance = PageWithChromeBrowser(driver)
    cart_page = CartPage(instance)
    cart_page.open_page()

    return cart_page


# Preparation work function for checkout_page
@pytest.fixture(scope="function")
def get_webdriver_instance_and_open_checkout_page(driver_lt):
    instance = PageWithChromeBrowserLongTimeout(driver_lt)
    checkout_page = CheckoutPage(instance)
    checkout_page.open_page()

    return checkout_page
