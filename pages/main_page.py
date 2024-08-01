import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from .product_card_page import ProductPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MainPage(BasePage):
    CATALOGS = (By.XPATH, "(//div[contains(@class,'caption wow')])")
    PRODUCTS_FROM_SALES_SECTION = (By.CSS_SELECTOR, "aside#accesspress_store_product-2>ul>div>div>li")
    PRODUCTS_FROM_NEW_ARRIVALS_SECTION = (By.CSS_SELECTOR, "aside#accesspress_store_product-3>ul>div>div>li")
    PRODUCT_FROM_POSTER_SECTION = (By.ID, "accesspress_store_full_promo-2")
    PRODUCTS_FROM_VIEWED_PRODUCTS_SECTION = (By.ID, "woocommerce_recently_viewed_products-2")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Skillbox — Интернет магазин":
            raise Exception(f"This is not main page, current page is: {self.driver.current_url}")

    def get_catalog_and_title(self, item):
        catalogs = self.wait_for_elements(self.CATALOGS)
        catalog = catalogs[item]
        catalog_title = self.get_element_from_another_element(catalog, By.TAG_NAME, "h4").text.capitalize()

        return catalog, catalog_title

    def go_to_product_from_sales_section(self, item):
        products = self.wait_for_elements(self.PRODUCTS_FROM_SALES_SECTION)
        product = products[item]
        self.scroll_to_element(product)
        header = self.get_element_from_another_element(product, By.TAG_NAME, "a").get_attribute("title")
        product.click()

        return ProductPage(self.driver, header), header

    def go_to_product_from_new_arrivals_section(self, item):
        products = self.wait_for_elements(self.PRODUCTS_FROM_NEW_ARRIVALS_SECTION)
        product = products[item]
        self.scroll_to_element(product)
        header = self.get_element_from_another_element(product, By.TAG_NAME, "a").get_attribute("title")
        product.click()

        return ProductPage(self.driver, header), header

    def get_product_and_title_from_poster_section(self):
        poster = self.wait_for_element(self.PRODUCT_FROM_POSTER_SECTION)
        self.scroll_to_element(poster)

        time.sleep(2)
        # url = self.get_element_from_another_element(poster, By.TAG_NAME, "a", 15).get_attribute("href")
        product_title = self.get_element_from_another_element(poster, By.CLASS_NAME, "promo-desc-title").text
        product_button = self.get_element_from_another_element(poster, By.XPATH, "(//span[@class='btn promo-link-btn'])[4]")

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(product_button))
        product_button.click()

        # def get_product_name_by(url):
        #     text = url.split('=')[-1]
        #     last_hyphen_index = text.rfind("-")
        #     # Replace all hyphen beside last
        #     modified_text = text[:last_hyphen_index].replace("-", " ") + text[last_hyphen_index:]
        #
        #     return modified_text

        # if "ipad air" in str(product_title).lower():
        #     product_title = get_product_name_by(url)
        #     product_title = product_title.replace("ipad", "iPad")
        #     # print("product_title -", product_title)

        return ProductPage(self.driver, product_title), product_title

    def go_to_viewed_product(self, item):
        header = ""
        try:
            products = self.wait_for_elements(self.PRODUCTS_FROM_VIEWED_PRODUCTS_SECTION)
            product = products[item]
            self.scroll_to_element(product)
            header = product.find_element(By.TAG_NAME, "span").text
        except TimeoutException:
            print("Cannot find viewed product block")

        return ProductPage(self.driver, header), header
