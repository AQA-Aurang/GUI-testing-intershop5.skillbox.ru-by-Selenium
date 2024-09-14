import time
from typing import Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.catalog_and_category_page import CatalogAndCategoryPage
from pages.product_card_page import get_any_product_from_catalog
from pages.product_card_page import ProductPage
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException

PRODUCT_LINKS_IN_CART: tuple[str, str] = (By.XPATH, "//td[@data-title='Товар']//a")
PRODUCT_IMG_LINKS_IN_CART: tuple[str, str] = (By.XPATH, "//td[@class='product-thumbnail']//a")


def adding_anyone_product_in_cart(catalog_and_sub_catalog_page: CatalogAndCategoryPage) -> Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]:
    driver, product_title = get_any_product_from_catalog(catalog_and_sub_catalog_page, 6)
    product_page: ProductPage = ProductPage(driver, product_title)
    product_page.driver, related_product_title = product_page.add_related_product_to_cart()
    product_page.go_to_cart_after_add_related_product()

    return product_page.driver


class CartPage(BasePage):
    QUANTITY_OF_PRODUCT: tuple[str, str] = (By.XPATH, "//input[contains(@class,'input-text qty')]")
    MODIFY_CART_NOTIFICATION: tuple[str, str] = (By.XPATH, "//div[@role='alert']")
    CART_EMPTY_MESSAGE: tuple[str, str] = (By.XPATH, "//p[@class='cart-empty woocommerce-info']")
    REMOVE_ICON: tuple[str, str] = (By.CLASS_NAME, "remove")
    RECOVERY_LINK: tuple[str, str] = (By.CLASS_NAME, "restore-item")
    COUPON_FIELD: tuple[str, str] = (By.ID, "coupon_code")
    COUPON_BUTTON: tuple[str, str] = (By.NAME, "apply_coupon")
    DISCOUNT_TEXT: tuple[str, str] = (By.XPATH, "//th[contains(text(), 'Скидка: ')]")
    ERROR_MESSAGE_ABOUT_WRONG_COUPON: tuple[str, str] = (By.XPATH, "//ul[@role='alert']//li")
    COUPON_REMOVE_LINK: tuple[str, str] = (By.LINK_TEXT, "[Удалить]")
    SUCCESS_MESSAGE_ABOUT_REMOVED_COUPON: tuple[str, str] = (By.XPATH, "//div[@role='alert']")
    PLACE_ORDER: tuple[str, str] = (By.XPATH, "//a[contains(@class,'checkout-button button')]")
    PRODUCTS_IN_CART: tuple[str, str] = (By.XPATH, "//td[@data-title='Товар']//a")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Корзина — Skillbox":
            raise Exception(f"This is not Корзина — Skillbox, current product name is: {self.driver.title} on page is: {self.driver.current_url}")

    def get_product_title_by(self, related_title) -> str:
        return self.get_text_of_element((By.XPATH, f"//td[@data-title='Товар']//a[contains(text(), '{related_title}')]"))

    def get_product_text_by(self, index) -> str:
        return self.get_text_of_element((By.XPATH, f"//td[@data-title='Товар']//a[{index+1}]"))

    def go_to_product(self, locator: tuple[str, str]) -> None:
        products: list[WebElement] = self.wait_for_elements(locator)
        product: WebElement = products[0]
        self.click_by(product)

    def get_quantity_of_product(self) -> int:
        quantity_field: WebElement = self.wait_for_element(self.QUANTITY_OF_PRODUCT)
        # self.driver.save_screenshot("C:/Users/Farid/Desktop/cart_page.png")

        return int(quantity_field.get_attribute("value"))

    def modify_quantity_of_product(self, current_quantity: int, direction: str):
        if direction == "increase":
            self.type(self.QUANTITY_OF_PRODUCT, str(current_quantity+1))
        else:
            self.type(self.QUANTITY_OF_PRODUCT, str(current_quantity-1))

    def get_updated_notification(self) -> str:
        return self.get_text_of_element(self.MODIFY_CART_NOTIFICATION)

    def remove_product(self) -> None:
        self.click(self.REMOVE_ICON)

    def is_cart_empty(self) -> bool:
        try:
            self.wait_for_element(self.CART_EMPTY_MESSAGE)
            return True
        except TimeoutException:
            return False

    def recovery_product(self) -> None:
        self.click(self.RECOVERY_LINK)
        time.sleep(.5)

    def check_coupon(self) -> bool:
        try:
            self.wait_for_element(self.DISCOUNT_TEXT)
            return True
        except TimeoutException:
            return False

    def apply_coupon(self, coupon: str) -> None:
        self.type(self.COUPON_FIELD, coupon)
        self.click(self.COUPON_BUTTON)
        time.sleep(.5)

    def get_discount_text_or_error_message(self) -> str:
        try:
            return self.get_text_of_element(self.DISCOUNT_TEXT)
        except TimeoutException:
            return self.get_text_of_element(self.ERROR_MESSAGE_ABOUT_WRONG_COUPON)

    def remove_coupon(self) -> None:
        self.click(self.COUPON_REMOVE_LINK)
        time.sleep(1.5)

    def is_coupon_removed(self) -> bool:
        try:
            self.wait_for_element(self.SUCCESS_MESSAGE_ABOUT_REMOVED_COUPON)
            return True
        except TimeoutException:
            return False

    def get_quantity_products_in_cart(self) -> int:
        try:
            products: list[WebElement] = self.wait_for_elements(self.PRODUCTS_IN_CART)

            return len(products)
        except TimeoutException:
            return 0
