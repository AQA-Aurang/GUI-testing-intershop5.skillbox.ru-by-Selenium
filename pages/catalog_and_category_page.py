from typing import Union
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from pages.base_page import BasePage


class CatalogAndCategoryPage(BasePage):
    CATALOG_AND_CATEGORY_TITLE: tuple[str, str] = (By.XPATH, "//h1[@class='entry-title ak-container']")
    SORT_ELEMENT: tuple[str, str] = (By.NAME, "orderby")
    CATEGORIES: tuple[str, str] = (By.XPATH, "//ul[@class='product-categories']//li")
    FILTER_ELEMENT: tuple[str, str] = (By.ID, "woocommerce_price_filter-2")
    SLIDER_IN_FILTER: str = "(//span[contains(@class,'ui-slider-handle ui-state-default')])"
    BUTTON_IN_FILTER: tuple[str, str] = (By.XPATH, "(//button[@type='submit'])[2]")
    PRODUCTS_FROM_GOODS_BLOCK: tuple[str, str] = (By.XPATH, "//ul[@class='product_list_widget']/li/a")
    PRODUCTS_IN_PAGE: tuple[str, str] = (By.XPATH, "//div[@id='primary']/div[1]/div[3]/ul[1]/li")
    PRODUCT_TITLE: tuple[str, str] = (By.XPATH, "//a[@class='collection_title']")
    PRODUCT_BUTTON: tuple[str, str] = (By.XPATH, "//div[@class='price-cart']/a")
    PAGINATION_ITEMS: tuple[str, str] = (By.XPATH, "//ul[@class='page-numbers']/li")
    MIN_PRICE: tuple[str, str] = (By.XPATH, "//div[@class='price_label']//span[1]")
    MAX_PRICE: tuple[str, str] = (By.XPATH, "//div[@class='price_label']//span[2]")

    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge], catalog_name="Каталог"):
        super().__init__(driver)
        self.catalog_name = catalog_name

        if self.driver.title != f"{self.catalog_name} — Skillbox":
            raise Exception(f"This is not {self.catalog_name}, current page is: {self.driver.current_url}")

    def get_title(self) -> str:
        return self.wait_for_element(self.CATALOG_AND_CATEGORY_TITLE).text.capitalize()

    def select_item_from_sort_element(self, value: str) -> None:
        select = Select(self.wait_for_element(self.SORT_ELEMENT))
        select.select_by_value(value)

    def get_all_categories(self) -> list[WebElement]:
        return self.wait_for_elements(self.CATEGORIES)

    def use_price_filter(self, left_pixel_offset: int, right_pixel_offset: int) -> tuple[int, int]:
        """
        The function use_price_filter moving the left and right slider in filter element
        :param left_pixel_offset: int, pointed in pixels to be moved
        :param right_pixel_offset: int, pointed in pixels to be moved
        :return: int, int, getting fixed min and max prices
        """
        filter_element = self.wait_for_element(self.FILTER_ELEMENT)
        self.scroll_to(filter_element)
        left_slider_element = self.get_element_from_another_element(filter_element, By.XPATH, self.SLIDER_IN_FILTER + "[1]")
        right_slider_element = self.get_element_from_another_element(filter_element, By.XPATH, self.SLIDER_IN_FILTER + "[2]")

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

    def get_all_products_from_goods_block(self) -> list[WebElement]:
        return self.wait_for_elements(self.PRODUCTS_FROM_GOODS_BLOCK)

    def get_products(self) -> list[WebElement]:
        return self.wait_for_elements(self.PRODUCTS_IN_PAGE)

    def get_pagination_items(self) -> list[WebElement]:
        return self.wait_for_elements(self.PAGINATION_ITEMS)
