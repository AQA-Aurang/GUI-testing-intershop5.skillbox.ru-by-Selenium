import pytest
from conftest import chrome_browser as driver
from interhsop5skillbox.pages.my_acc_page import MyAccountPage


# Preparation work function
@pytest.fixture(scope="module")
def get_webdriver_instance_and_open_account_page(driver):
    acc_page = MyAccountPage(driver)
    acc_page.open_page()

    yield acc_page
