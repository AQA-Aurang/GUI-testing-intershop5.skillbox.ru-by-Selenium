import time

from selenium.webdriver.common.by import By
from pages2.product_card_page import get_any_product_from_catalog
from pages2.product_card_page import ProductPage
from pages2.base_page import BasePage
from selenium.common.exceptions import TimeoutException

PRODUCT_LINKS_IN_CART = (By.XPATH, "//td[@data-title='Товар']//a")
PRODUCT_IMG_LINKS_IN_CART = (By.XPATH, "//td[@class='product-thumbnail']//a")


def adding_anyone_product_in_cart(preparation_work):
    driver, product_title = get_any_product_from_catalog(preparation_work, 6)
    product_page = ProductPage(driver, product_title)
    product_page.driver, related_product_title = product_page.add_related_product_to_cart()
    product_page.go_to_cart_after_add_related_product()

    return product_page.driver


class CartPage(BasePage):
    QUANTITY_OF_PRODUCT = (By.XPATH, "//input[contains(@class,'input-text qty')]")
    MODIFY_CART_NOTIFICATION = (By.XPATH, "//div[@role='alert']")
    CART_EMPTY_MESSAGE = (By.XPATH, "//p[@class='cart-empty woocommerce-info']")
    REMOVE_ICON = (By.CLASS_NAME, "remove")
    RECOVERY_LINK = (By.CLASS_NAME, "restore-item")
    COUPON_FIELD = (By.ID, "coupon_code")
    COUPON_BUTTON = (By.NAME, "apply_coupon")
    DISCOUNT_TEXT = (By.XPATH, "//th[contains(text(), 'Скидка: ')]")
    ERROR_MESSAGE_ABOUT_WRONG_COUPON = (By.XPATH, "//ul[@role='alert']//li")
    COUPON_REMOVE_LINK = (By.LINK_TEXT, "[Удалить]")
    SUCCESS_MESSAGE_ABOUT_REMOVED_COUPON = (By.XPATH, "//div[@role='alert']")
    PLACE_ORDER = (By.XPATH, "//a[contains(@class,'checkout-button button')]")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Корзина — Skillbox":
            raise Exception(f"This is not Корзина — Skillbox, current product name is: {self.driver.title} on page is: {self.driver.current_url}")

    def get_product_title_by(self, related_title):
        return self.get_text_of_element((By.XPATH, f"//td[@data-title='Товар']//a[contains(text(), '{related_title}')]"))

    def get_product_text_by(self, index):
        return self.get_text_of_element((By.XPATH, f"//td[@data-title='Товар']//a[{index+1}]"))

    def go_to_product(self, locator):
        products = self.wait_for_elements(locator)
        product = products[0]
        self.click_by(product)

    def get_quantity_of_product(self):
        quantity_field = self.wait_for_element(self.QUANTITY_OF_PRODUCT)
        # print("quantity_field value -", quantity_field.get_attribute("value"))
        # self.driver.save_screenshot("C:/Users/Farid/Desktop/cart_page.png")

        return int(quantity_field.get_attribute("value"))

    def modify_quantity_of_product(self, current_quantity: int, direction):
        if direction == "increase":
            self.type(self.QUANTITY_OF_PRODUCT, current_quantity+1)
        else:
            self.type(self.QUANTITY_OF_PRODUCT, current_quantity-1)

    def get_updated_notification(self):
        return self.get_text_of_element(self.MODIFY_CART_NOTIFICATION)

    def remove_product(self):
        self.click(self.REMOVE_ICON)

    def is_cart_empty(self):
        try:
            self.wait_for_element(self.CART_EMPTY_MESSAGE)
            return True
        except TimeoutException:
            return False

    def recovery_product(self):
        self.click(self.RECOVERY_LINK)
        time.sleep(.5)

    def apply_coupon(self, coupon):
        self.type(self.COUPON_FIELD, coupon)
        self.click(self.COUPON_BUTTON)
        time.sleep(.5)

    def get_discount_text_or_error_message(self):
        try:
            return self.get_text_of_element(self.DISCOUNT_TEXT)
        except TimeoutException:
            return self.get_text_of_element(self.ERROR_MESSAGE_ABOUT_WRONG_COUPON)

    def remove_coupon(self):
        self.click(self.COUPON_REMOVE_LINK)
        time.sleep(1.5)

    def is_coupon_removed(self):
        try:
            self.wait_for_element(self.SUCCESS_MESSAGE_ABOUT_REMOVED_COUPON)
            return True
        except TimeoutException:
            return False
