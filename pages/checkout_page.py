from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
from pages.shopping_cart_page import CartPage
from pages.product_card_page import get_any_product_from_catalog_light_version, ProductPage
from pages.catalog_and_category_page import CatalogAndCategoryPage
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


def adding_anyone_product_in_cart_and_go_to_checkout(catalog_and_category_page: CatalogAndCategoryPage):
    driver, product_title = get_any_product_from_catalog_light_version(catalog_and_category_page, 6)
    product_page = ProductPage(driver, product_title)
    product_page.driver, related_product_title = product_page.add_related_product_to_cart()
    product_page.go_to_cart_after_add_related_product()
    cart_page = CartPage(product_page.driver)
    cart_page.click(cart_page.PLACE_ORDER)

    checkout_page = CheckoutPage(cart_page.driver)

    return checkout_page


NAME_FIELD: tuple[str, str] = (By.ID, "billing_first_name")
LAST_NAME_FIELD: tuple[str, str] = (By.ID, "billing_last_name")
ADDRESS_FIELD: tuple[str, str] = (By.ID, "billing_address_1")
CITY_FIELD: tuple[str, str] = (By.ID, "billing_city")
STATE_FIELD: tuple[str, str] = (By.ID, "billing_state")


class CheckoutPage(BasePage):
    COUPON_FIELD: tuple[str, str] = (By.ID, "coupon_code")
    COUPON_BUTTON: tuple[str, str] = (By.NAME, "apply_coupon")
    LINK_TO_TURN_ON_COUPON_BLOCK: tuple[str, str] = (By.CLASS_NAME, "showcoupon")
    COUPON_SUCCESS_APPLIED: tuple[str, str] = (By.CLASS_NAME, "woocommerce-message")
    DISCOUNT_TEXT: tuple[str, str] = (By.XPATH, "//th[contains(text(), 'Скидка:')]")
    COUPON_REMOVE_LINK: tuple[str, str] = (By.LINK_TEXT, "[Удалить]")
    ALERT_ABOUT_REMOVED_COUPON: tuple[str, str] = (By.XPATH, "//div[@role='alert']")
    ORDER_BUTTON: tuple[str, str] = (By.ID, "place_order")
    ERROR_ALERT: tuple[str, str] = (By.XPATH, "//ul[@role='alert']/li")
    ERROR_ALERTS: tuple[str, str] = (By.XPATH, "//ul[@class='woocommerce-error']/li")
    PAYMENT_METHODS: tuple[str, str] = (By.XPATH, "//ul[contains(@class,'wc_payment_methods payment_methods')]//li")
    PAYMENT_BY_BANK_TRANSFER: tuple[str, str] = (By.XPATH, "//div[@id='payment']/ul[1]/li[1]/input")
    PAYMENT_ON_DELIVERY_METHOD: tuple[str, str] = (By.XPATH, "//div[@id='payment']/ul[1]/li[2]/input")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Оформление заказа — Skillbox":
            raise Exception(f"This is not Оформление заказа — Skillbox, current product name is: {self.driver.title} "
                            f"on page is: {self.driver.current_url}")

    def is_coupon_already_applied(self) -> bool:
        try:
            self.wait_for_element(self.DISCOUNT_TEXT)
            return True
        except TimeoutException:
            return False

    def apply_coupon(self, coupon: str) -> None:
        self.click(self.LINK_TO_TURN_ON_COUPON_BLOCK)
        sleep(.3)
        self.type(self.COUPON_FIELD, coupon)
        self.click(self.COUPON_BUTTON)
        sleep(.5)

    def removed_applied_coupon(self) -> None:
        element: WebElement = self.wait_for_element(self.COUPON_REMOVE_LINK)
        self.scroll_to_element(element)

        try:
            self.click_by(element)
        except StaleElementReferenceException:
            self.click(self.COUPON_REMOVE_LINK)
        finally:
            sleep(.5)

    def get_success_message_by_apply_coupon(self) -> str:
        return self.get_text_of_element(self.COUPON_SUCCESS_APPLIED)

    def is_coupon_removed(self) -> bool:
        try:
            self.wait_for_element(self.ALERT_ABOUT_REMOVED_COUPON)
            return True
        except TimeoutException:
            return False

    def clear_fields(self, *locators: [str, str]) -> None:
        for locator in locators:
            self.wait_for_element(locator).clear()

    def filling_fields(self, **locators: [str, str]) -> None:
        for value, tupl in locators.items():
            self.type(tupl, value)
            sleep(4)

        self.ordering_products()

    def ordering_products(self):
        try:
            self.click(self.ORDER_BUTTON)
        except StaleElementReferenceException:
            self.click(self.ORDER_BUTTON)
        finally:
            sleep(.5)

    def get_payment_variants(self):
        return self.wait_for_elements(self.PAYMENT_METHODS)

    def select_payment_method(self, method: str):
        payment_method = (By.XPATH, f"//label[text()[normalize-space()='{method}']]")
        payment_method_label = self.wait_for_element(payment_method)

        try:
            self.click_by(payment_method_label)
        except StaleElementReferenceException as er:
            # print('StaleElementReferenceException msg -', er.msg)
            self.logger.error(f'StaleElementReferenceException msg - {er.msg}')
            self.click(payment_method)
