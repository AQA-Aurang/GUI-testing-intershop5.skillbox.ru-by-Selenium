import pytest
from conftest import chrome_browser as driver
from pages.my_acc_page import MyAccountPage
from pages.main_page import MainPage
from pages.catalog_and_subcatalog_page import CatalogAndSubCatalogPage
from pages.product_card_page import ProductCardPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


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
