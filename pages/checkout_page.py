from time import sleep
from typing import Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from pages.base_page import BasePage
from pages.catalog_and_category_page import CatalogAndCategoryPage
from pages.product_card_page import get_any_product_from_catalog, ProductPage
from pages.shopping_cart_page import CartPage


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
    PAYMENT_METHOD_LOCATOR: str = "//label[text()[normalize-space()='%method']]"
    PAYMENT_BY_BANK_TRANSFER: tuple[str, str] = (By.XPATH, "//div[@id='payment']/ul[1]/li[1]/input")
    PAYMENT_ON_DELIVERY_METHOD: tuple[str, str] = (By.XPATH, "//div[@id='payment']/ul[1]/li[2]/input")
    LOAD_BLOCK: tuple[str, str] = (By.CLASS_NAME, "blockUI blockOverlay")

    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]):
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
        self.scroll_to(element)

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
        """
        :param locators: tuple[str, str], can receive multiple locators
        """
        for locator in locators:
            self.wait_for_element(locator).clear()

    def filling_fields(self, **locators: [str, str]) -> None:
        """
        :param locators: tuple[str, str], can receive multiple locators
        """
        for value, tupl in locators.items():
            self.type(tupl, value)
            sleep(.5)

        self.ordering_products()

    def waiting_load_block_invisible(self) -> None:
        sleep(.5)
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element(self.LOAD_BLOCK))

    def ordering_products(self) -> None:
        try:
            self.click(self.ORDER_BUTTON)
        except StaleElementReferenceException as sere:
            self.logger.log(30, f"We get StaleElementReferenceException - {sere.msg}")
            self.click(self.ORDER_BUTTON)
        except ElementClickInterceptedException as ecie:
            self.logger.log(30, f"We get ElementClickInterceptedException - {ecie.msg}")
            self.scroll_by(self.ORDER_BUTTON)
            self.click(self.ORDER_BUTTON)
        finally:
            sleep(.5)

    def get_payment_variants(self) -> list[WebElement]:
        return self.wait_for_elements(self.PAYMENT_METHODS)

    def select_payment_method(self, method: str) -> None:
        sleep(.5)
        # payment_method = (By.XPATH, f"//label[text()[normalize-space()='{method}']]")
        payment_method_locator = self.PAYMENT_METHOD_LOCATOR.replace('%method', method)
        payment_method = (By.XPATH, payment_method_locator)
        payment_method_label = self.wait_for_element(payment_method)

        try:
            self.click_by(payment_method_label)
        except StaleElementReferenceException as er:
            self.logger.error(f'We get StaleElementReferenceException - {er.msg}')
            self.click(payment_method)


def adding_anyone_product_in_cart_and_go_to_checkout(catalog_and_category_page: CatalogAndCategoryPage) -> CheckoutPage:
    """
    :param catalog_and_category_page: catalog and category page object
    :return: checkout page object
    """
    driver, product_title = get_any_product_from_catalog(catalog_and_category_page, 6)
    product_page: ProductPage = ProductPage(driver, product_title)
    product_page.driver, related_product_title = product_page.add_related_product_to_cart()
    product_page.go_to_cart_after_add_related_product()
    cart_page: CartPage = CartPage(product_page.driver)
    cart_page.click(cart_page.PLACE_ORDER)

    checkout_page: CheckoutPage = CheckoutPage(cart_page.driver)

    return checkout_page
