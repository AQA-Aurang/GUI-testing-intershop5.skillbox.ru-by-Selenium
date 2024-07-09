import configparser
import data.locators as locator
import data.test_data as test_data
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pages.base_types import BaseType


def get_element_in_another_element(element, type_of_locator, locator):
    return element.find_element(type_of_locator, locator)


def get_elements_in_another_element(element, type_of_locator, locator):
    return element.find_elements(type_of_locator, locator)


def is_visibility(type_of_locator, locator):
    return EC.visibility_of_element_located((type_of_locator, locator))


class BasePage:
    def __init__(self, chrome: BaseType):
        self.driver = chrome.get_driver

        config = configparser.ConfigParser()
        config.read('./../config.ini')

        for username, password in config["users"].items():
            if username == "ferdinand":
                self.default_username = username.capitalize()
                self.default_password = password

    def open_page(self, url="https://intershop5.skillbox.ru"):
        self.driver.get(url)

    def get_element(self, type_of_locator, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((type_of_locator, locator)))

    # def get_element_with_te(self, type_of_locator, locator):
    #     try:
    #         element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((type_of_locator, locator)))
    #         return element
    #
    #     except TimeoutException as t:
    #         print(f"TimeoutException in getting element - {t.args}")
    #         return self.driver

    def get_element_lt(self, type_of_locator, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((type_of_locator, locator)))

    def get_element_and_text(self, type_of_locator, locator):
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((type_of_locator, locator)))
        return element, element.text

    def click_element(self, element):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))
        element.click()

    def get_elements(self, type_of_locator, locator):
        return WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((type_of_locator, locator)))

    # def get_elements_with_te(self, type_of_locator, locator):
    #     try:
    #         elements = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((type_of_locator, locator)))
    #         return elements
    #
    #     except TimeoutException as t:
    #         print(f"TimeoutException in getting elements - {t.args}")
    #         return WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((type_of_locator, locator)))

    def get_elements_lt(self, type_of_locator, locator):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((type_of_locator, locator)))

    def find_and_click_on_element(self, type_of_locator, locator):
        element = self.get_element(type_of_locator, locator)
        self.click_element(element)

    def find_and_submit_on_button(self, type_of_locator, locator):
        element = self.get_element(type_of_locator, locator)
        element.submit()

    def go_to_bottom(self):
        return self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def element_should_have_text(self, type_of_locator, locator, text, err_description):
        element = self.get_element(type_of_locator, locator)
        assert element.text == text, err_description

    def expected_text_consist_in_searching_element(self, type_of_locator, locator, text, err_description):
        element = self.get_element(type_of_locator, locator)
        assert text in element.text, err_description

    def move_down_in_altitude_by(self, point):
        height = self.driver.execute_script("return window.innerHeight;")
        self.driver.execute_script(f"window.scrollTo(0, {height * point});")

    def find_and_clear_field(self, type_of_locator, locator):
        field = self.get_element(type_of_locator, locator)
        field.clear()

        return field

    def print_in_field(self, type_of_locator, locator, new_value):
        field = self.find_and_clear_field(type_of_locator, locator)
        field.send_keys(new_value)

        return self.driver

    def go_to_product(self):
        self.find_and_click_on_element(By.XPATH, locator.product_in_sale_block_on_main_page)

    def get_product_and_his_title_on_product_card(self):
        if is_visibility(By.XPATH, locator.product_card_footers):
            products_card_footers = self.get_elements(By.XPATH, locator.product_card_footers)
        else:
            return "Element not visible", 0

        for i in range(len(products_card_footers)):
            product_card_footer = products_card_footers[i]
            title_product = get_element_in_another_element(product_card_footer, By.XPATH, "//a/h3").text
            button_to_add_cart = self.get_element(By.XPATH, locator.button_in_product_footer)

            if button_to_add_cart.text.capitalize() == "В корзину":
                return title_product, i

        return "To cart not found", 0

    def add_item_to_cart_from_related_products_on_product_card(self):
        self.open_page()
        self.go_to_product()

        while True:
            title_product, item_number = self.get_product_and_his_title_on_product_card()
            if title_product != "Element not visible" and title_product != "To cart not found":
                break

            self.driver.refresh()

        self.find_and_click_on_element(By.XPATH, f"//ul[@class='products columns-4']//li/div[2]/div/a[{item_number + 1}]")
        self.find_and_click_on_element(By.XPATH, locator.detail_link)

        return title_product

    def apply_coupon(self, coupon, locator_elem):
        self.print_in_field(By.ID, locator.field_for_coupon_input, coupon)
        self.find_and_click_on_element(By.NAME, locator.apply_coupon_on_cart_page)
        alert_element = self.get_element(By.XPATH, locator_elem)

        return alert_element.text

    def removing_applied_coupons(self):
        coupon = self.get_element(By.XPATH, locator.discount_row)

        if test_data.promo_code in coupon.text:
            row = get_element_in_another_element(coupon, By.XPATH, "./..")
            link_in_column = get_element_in_another_element(row, By.CSS_SELECTOR, "td a")
            self.click_element(link_in_column)
