import pytest
from conftest import chrome_browser as driver
from interhsop5skillbox.pages.my_acc_page import MyAccountPage
from interhsop5skillbox.pages.main_page import MainPage
from interhsop5skillbox.pages.catalog_and_subcatalog_page import CatalogAndSubCatalogPage


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
