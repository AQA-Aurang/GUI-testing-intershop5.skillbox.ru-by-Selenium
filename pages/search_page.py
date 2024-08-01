from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException


class SearchPage(BasePage):
    SEARCHING_PRODUCTS_IN_PAGE = (By.XPATH, "//div[@id='primary']/div[1]/div[3]/ul[1]/li")
    NOTHING_WAS_FOUND = (By.CLASS_NAME, "woocommerce-info")

    def __init__(self, driver, searching_product):
        super().__init__(driver)
        self.searching_product = searching_product

        if self.driver.title != f"Search Results for “{searching_product}” — Skillbox":
            raise Exception(f"This is not searching page")

    def searching_product_is_available(self):
        try:
            self.wait_for_element(self.NOTHING_WAS_FOUND)
            return False
        except TimeoutException:
            return True

    def get_products(self):
        return self.wait_for_elements(self.SEARCHING_PRODUCTS_IN_PAGE)
