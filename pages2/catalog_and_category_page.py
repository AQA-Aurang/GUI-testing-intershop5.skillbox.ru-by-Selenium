from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from .base_page import BasePage


class CatalogAndCategoryPage(BasePage):
    CATALOG_AND_CATEGORY_TITLE = (By.XPATH, "//h1[@class='entry-title ak-container']")
    SORT_ELEMENT = (By.NAME, "orderby")
    CATEGORIES = (By.XPATH, "//ul[@class='product-categories']//li")
    FILTER_ELEMENT = (By.ID, "woocommerce_price_filter-2")
    SLIDER_IN_FILTER = "(//span[contains(@class,'ui-slider-handle ui-state-default')])"
    BUTTON_IN_FILTER = (By.XPATH, "(//button[@type='submit'])[2]")
    PRODUCTS_FROM_GOODS_BLOCK = (By.XPATH, "//ul[@class='product_list_widget']/li/a")
    PRODUCTS_IN_PAGE = (By.XPATH, "//div[@id='primary']/div[1]/div[3]/ul[1]/li")
    PRODUCT_TITLE = (By.XPATH, "//a[@class='collection_title']")
    PRODUCT_BUTTON = (By.XPATH, "//div[@class='price-cart']/a")
    PAGINATION_ITEMS = (By.XPATH, "//ul[@class='page-numbers']/li")
    MIN_PRICE = (By.XPATH, "//div[@class='price_label']//span[1]")
    MAX_PRICE = (By.XPATH, "//div[@class='price_label']//span[2]")

    def __init__(self, driver, catalog_name="Каталог"):
        super().__init__(driver)
        self.catalog_name = catalog_name

        if self.driver.title != f"{self.catalog_name} — Skillbox":
            raise Exception(f"This is not {self.catalog_name}, current page is: {self.driver.current_url}")

    def get_title(self):
        return self.wait_for_element(self.CATALOG_AND_CATEGORY_TITLE).text.capitalize()

    def select_item_from_sort_element(self, value):
        select = Select(self.wait_for_element(self.SORT_ELEMENT))
        select.select_by_value(value)

    def get_all_categories(self):
        return self.wait_for_elements(self.CATEGORIES)

    def use_price_filter(self, left_pixel_offset, right_pixel_offset):
        filter = self.wait_for_element(self.FILTER_ELEMENT)
        self.scroll_to_element(filter)
        left_slider_element = self.get_element_from_another_element(filter, By.XPATH,  self.SLIDER_IN_FILTER + "[1]")
        right_slider_element = self.get_element_from_another_element(filter, By.XPATH, self.SLIDER_IN_FILTER + "[2]")

        min_fixed_price = None
        if left_pixel_offset > 0:
            action = ActionChains(self.driver)
            action.drag_and_drop_by_offset(left_slider_element, left_pixel_offset, 0).perform()

        max_fixed_price = None
        if right_pixel_offset > 0:
            action = ActionChains(self.driver)
            action.drag_and_drop_by_offset(right_slider_element, right_pixel_offset, 0).perform()

        fixed_price_str = self.get_text_of_element(self.MIN_PRICE)
        min_fixed_price = int(fixed_price_str[:-1])
        fixed_price_str = self.get_text_of_element(self.MAX_PRICE)
        max_fixed_price = int(fixed_price_str[:-1])

        self.click(self.BUTTON_IN_FILTER)
        return min_fixed_price, max_fixed_price

    def get_all_products_from_goods_block(self):
        return self.wait_for_elements(self.PRODUCTS_FROM_GOODS_BLOCK)

    def get_products(self):
        return self.wait_for_elements(self.PRODUCTS_IN_PAGE)

    def get_pagination_items(self):
        return self.wait_for_elements(self.PAGINATION_ITEMS)
