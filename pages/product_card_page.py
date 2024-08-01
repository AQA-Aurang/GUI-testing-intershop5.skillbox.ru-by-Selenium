import random
import time

from selenium.webdriver.support.wait import WebDriverWait

# from conftest2 import chrome_browser as driver
# from conftest2 import get_username_password
# from conftest2 import get_webdriver_instance_and_open_catalog_and_sub_catalog_page as preparation_work_catalog_page
from .base_page import BasePage
from pages.catalog_and_category_page import CatalogAndCategoryPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSelectorException


def get_ordering_product(my_account_page, username, password, order_num=0):
    my_account_page.authorisation(username, password)

    order_page = my_account_page.go_to_order_block()
    orders = order_page.get_orders()
    title, link = order_page.get_title_and_link(orders[order_num], order_num)
    order_detail_page = order_page.click_by_this(link)
    product = order_detail_page.get_product()
    product_title = product.text

    order_detail_page.click_by(product)
    return product_title


def get_any_product_from_catalog(preparation_work, item):
    catalog_and_category_page = preparation_work
    products = catalog_and_category_page.get_products()
    product = products[item]

    product_txt = product.text.split("\n")[0]
    if "₽" not in product_txt:
        product_title = product.text.split("\n")[1] if product_txt == "Скидка!" else product_txt
    else:
        product_title = ""

    product_link = catalog_and_category_page.get_element_from_another_element(product, By.TAG_NAME, "a")
    product_link.click()

    return catalog_and_category_page.driver, product_title


def get_any_product_from_catalog_light_version(catalog_and_category_page, item):
    products = catalog_and_category_page.get_products()
    product = products[item]
    product_title = product.text.split("\n")[1]

    product_link = catalog_and_category_page.get_element_from_another_element(product, By.TAG_NAME, "a")
    product_link.click()

    return catalog_and_category_page.driver, product_title


class ProductPage(BasePage):
    PRODUCT_TITLE = (By.XPATH, "//h1[@class='product_title entry-title']")
    MAGNIFYING_GLASS = (By.CLASS_NAME, "woocommerce-product-gallery__trigger")
    IN_STOCK_OR_NOT = (By.XPATH, "//p[@class='stock out-of-stock']")
    CART_BUTTON = (By.NAME, "add-to-cart")
    FEEDBACK_TAB = (By.XPATH, "//a[@href='#tab-reviews']")
    FEEDBACK_MARKS = (By.XPATH, "//p[@class='stars']//a")
    FEEDBACK_COMMENT = (By.ID, "comment")
    FEEDBACK_BUTTON = (By.ID, "submit")
    PRODUCTS_FROM_RELATED_BLOCK = (By.XPATH, "//ul[@class='products columns-4']/li")
    CATEGORY_FROM_CATEGORIES_BLOCK = (By.XPATH, "//ul[@class='product-categories']//li")
    PRODUCTS_FROM_GOODS_BLOCK = (By.XPATH, "//ul[@class='product_list_widget']/li/a")
    PRODUCT_QUANTITY = (By.XPATH, "//input[@type='number']")
    PRODUCT_COUNT_IN_STOCK = (By.XPATH, "//p[@class='stock in-stock']")
    SUCCESS_MESSAGE_AFTER_ADD_TO_CART = (By.XPATH, "//div[@role='alert']")
    COME_BACK_LINK = (By.LINK_TEXT, "« Back")
    DUPLICATE_WARNING = (By.XPATH, "//div[@class='wp-die-message']//p[1]")

    def __init__(self, driver, product_name):
        super().__init__(driver)
        self.product_name = product_name

        if self.driver.title != f"{product_name} — Skillbox":
            raise Exception(f"This is not {product_name}, current product name is: {self.driver.title} on page is: {self.driver.current_url}")

    def get_title(self):
        return self.wait_for_element(self.PRODUCT_TITLE).text.capitalize()

    def is_quantity_field_available(self):
        try:
            self.wait_for_element(self.PRODUCT_QUANTITY)
            return True
        except TimeoutException:
            return False

    def change_count_buying_product(self, count):
        if self.is_available_in_stock():
            self.type(self.PRODUCT_QUANTITY, count)

    def is_magnifying_glass_available(self):
        try:
            self.element_is_clickable(self.MAGNIFYING_GLASS)
            return True
        except TimeoutException:
            return False

    def click_to_magnifying_glass(self):
        self.click(self.MAGNIFYING_GLASS)

    def is_available_in_stock(self):
        try:
            self.wait_for_element(self.IN_STOCK_OR_NOT)
            return False
        except TimeoutException:
            return True

    def how_many_product_in_stock(self):
        if self.is_available_in_stock():
            try:
                product_count_in_stock = self.get_text_of_element(self.PRODUCT_COUNT_IN_STOCK)
                return int(product_count_in_stock.split(" ")[0])
            except TimeoutException:
                return 0

    def add_product_to_cart(self):
        self.click(self.CART_BUTTON)

    def switch_to_feedback_tab(self):
        add_to_card_button = self.wait_for_element(self.CART_BUTTON)
        self.scroll_to_element(add_to_card_button) # scroll to button to add product in cart for see feedback tab and click one
        self.click(self.FEEDBACK_TAB)

    def is_comment_field_available(self):
        try:
            self.wait_for_element(self.FEEDBACK_COMMENT)
            return True
        except TimeoutException:
            return False

    def leave_feedback(self, star, comment):
        marks = self.wait_for_elements(self.FEEDBACK_MARKS)
        mark = marks[star-1]
        mark.click()

        self.type(self.FEEDBACK_COMMENT, comment)
        self.click(self.FEEDBACK_BUTTON)

    def get_products_from_related_products(self):
        return self.wait_for_elements(self.PRODUCTS_FROM_RELATED_BLOCK)

    def go_to_related_product(self, secret_word="Read more"):
        products = self.get_products_from_related_products()
        product_title = ""

        for product in products:
            if secret_word in product.text:
                try:
                    product_link = self.get_element_from_another_element(product, By.CLASS_NAME, "button.product_type_simple")
                    product_title = product.text.split("\n")[0] if "₽" in product.text.split("\n")[1] \
                                                                else product.text.split("\n")[1]
                    self.scroll_to_element(product)
                    self.click_by(product_link)
                    break

                except TimeoutException:
                    self.driver.refresh()
                    self.go_to_related_product()
                except InvalidSelectorException:
                    self.driver.refresh()
                    self.go_to_related_product()
                except Exception:
                    print("current url -", self.driver.current_url)

        return self.driver, product_title

    def add_related_product_to_cart(self):
        return self.go_to_related_product("В корзину".upper())

    def go_to_cart_after_add_related_product(self):
        detail_link = self.wait_for_element((By.XPATH, "//a[@class='added_to_cart wc-forward']"))
        self.click_by(detail_link)

    def get_categories_from_goods_category_block(self):
        return self.wait_for_elements(self.CATEGORY_FROM_CATEGORIES_BLOCK)

    def get_products_from_goods_block(self):
        return self.wait_for_elements(self.PRODUCTS_FROM_GOODS_BLOCK)

    def is_exist_feedback(self, comment, timeout=10):
        self.driver.implicitly_wait(0)
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//p[text()='{comment}']")))
            return True
        except TimeoutException as te:
            print("error -", te.msg)
            return False

    def go_back_when_detect_duplicate_feedback(self):
        if "Duplicate comment detected;" in self.wait_for_element(self.DUPLICATE_WARNING).text:
            self.click(self.COME_BACK_LINK)

    def get_all_products_from_goods_block(self):
        return self.wait_for_elements(self.PRODUCTS_FROM_GOODS_BLOCK)
