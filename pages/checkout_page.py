import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
from pages.shopping_cart_page import CartPage
from conftest import get_username_password
from pages.product_card_page import get_any_product_from_catalog_light_version, ProductPage
from pages.catalog_and_category_page import CatalogAndCategoryPage
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC


def authorisation(preparation_work):
    my_account_page = preparation_work
    username, password = get_username_password()
    my_account_page.authorisation(username, password)

    return my_account_page


def adding_anyone_product_in_cart_and_go_to_checkout(catalog_and_category_page: CatalogAndCategoryPage):
    driver, product_title = get_any_product_from_catalog_light_version(catalog_and_category_page, 6)
    product_page = ProductPage(driver, product_title)
    product_page.driver, related_product_title = product_page.add_related_product_to_cart()
    product_page.go_to_cart_after_add_related_product()
    cart_page = CartPage(product_page.driver)
    cart_page.click(cart_page.PLACE_ORDER)

    checkout_page = CheckoutPage(cart_page.driver)

    return checkout_page


class CheckoutPage(BasePage):
    COUPON_FIELD = (By.ID, "coupon_code")
    COUPON_BUTTON = (By.NAME, "apply_coupon")
    LINK_TO_TURN_ON_COUPON_BLOCK = (By.CLASS_NAME, "showcoupon")
    COUPON_SUCCESS_APPLIED = (By.CLASS_NAME, "woocommerce-message")
    DISCOUNT_TEXT = (By.XPATH, "//th[contains(text(), 'Скидка:')]")
    COUPON_REMOVE_LINK = (By.LINK_TEXT, "[Удалить]")
    ALERT_ABOUT_REMOVED_COUPON = (By.XPATH, "//div[@role='alert']")
    NAME_FIELD = (By.ID, "billing_first_name")
    LAST_NAME_FIELD = (By.ID, "billing_last_name")
    ADDRESS_FIELD = (By.ID, "billing_address_1")
    CITY_FIELD = (By.ID, "billing_city")
    STATE_FIELD = (By.ID, "billing_state")
    ORDER_BUTTON = (By.ID, "place_order")
    ERROR_ALERT = (By.XPATH, "//ul[@role='alert']/li")
    ERROR_ALERTS = (By.XPATH, "//ul[@class='woocommerce-error']/li")
    PAYMENT_METHODS = (By.XPATH, "//div[@id='payment']/ul[1]/li")
    PAYMENT_ON_DELIVERY_METHOD = (By.XPATH, "//div[@id='payment']/ul[1]/li[2]/input")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Оформление заказа — Skillbox":
            raise Exception(f"This is not Оформление заказа — Skillbox, current product name is: {self.driver.title} "
                            f"on page is: {self.driver.current_url}")

    def is_coupon_already_applied(self):
        try:
            self.wait_for_element(self.DISCOUNT_TEXT)
            return True
        except TimeoutException:
            return False

    def apply_coupon(self, coupon: str):
        self.click(self.LINK_TO_TURN_ON_COUPON_BLOCK)
        time.sleep(.3)
        self.type(self.COUPON_FIELD, coupon)
        self.click(self.COUPON_BUTTON)
        time.sleep(.5)

    def removed_applied_coupon(self):
        element = self.wait_for_element(self.COUPON_REMOVE_LINK)
        self.scroll_to_element(element)

        try:
            self.click_by(element)
        except StaleElementReferenceException:
            self.click(self.COUPON_REMOVE_LINK)
        finally:
            time.sleep(.5)

    def get_success_message_by_apply_coupon(self):
        return self.get_text_of_element(self.COUPON_SUCCESS_APPLIED)

    def is_coupon_removed(self):
        try:
            self.wait_for_element(self.ALERT_ABOUT_REMOVED_COUPON)
            return True
        except TimeoutException:
            return False

    def clear_fields(self, *locators: [str, str]):
        for locator in locators:
            self.wait_for_element(locator).clear()

    def filling_fields(self, **locators: [str, str]):
        for value, tuple in locators.items():
            self.type(tuple, value)
            time.sleep(4)

        self.ordering_products()

    def clean_field_and_click_button(self, locator):
        self.wait_for_element(locator).clear()

        try:
            self.click(self.ORDER_BUTTON)
        except StaleElementReferenceException:
            self.click(self.ORDER_BUTTON)
        finally:
            time.sleep(.5)

    def ordering_products(self):
        try:
            self.click(self.ORDER_BUTTON)
        except StaleElementReferenceException:
            self.click(self.ORDER_BUTTON)
        finally:
            time.sleep(.5)

    def get_payment_variants(self):
        return self.wait_for_elements(self.PAYMENT_METHODS)

    def get_title_by(self, payment_variant: WebElement):
        label = self.get_element_from_another_element(payment_variant, By.TAG_NAME, "label")
        return label.text

    def is_selected(self, element: WebElement):
        radio_button = self.get_element_from_another_element(element, By.TAG_NAME, "input")

        if radio_button.is_selected():
            return True

        return False

    def payment_on_delivery(self):
        element = self.wait_for_element(self.PAYMENT_ON_DELIVERY_METHOD)

        try:
            self.click_by(element)
        except StaleElementReferenceException:
            self.click(self.PAYMENT_ON_DELIVERY_METHOD)
