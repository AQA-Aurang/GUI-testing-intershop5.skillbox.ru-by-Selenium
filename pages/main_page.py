from typing import Tuple

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
from pages.product_card_page import ProductPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MainPage(BasePage):
    CATALOGS = (By.XPATH, "(//div[contains(@class,'caption wow')])")
    PRODUCTS_FROM_SALES_SECTION = (By.CSS_SELECTOR, "aside#accesspress_store_product-2>ul>div>div>li")
    PRODUCTS_FROM_NEW_ARRIVALS_SECTION = (By.CSS_SELECTOR, "aside#accesspress_store_product-3>ul>div>div>li")
    PRODUCT_FROM_POSTER_SECTION = (By.ID, "accesspress_store_full_promo-2")
    # PRODUCTS_FROM_VIEWED_PRODUCTS_SECTION = (By.ID, "woocommerce_recently_viewed_products-2")
    PRODUCTS_FROM_VIEWED_PRODUCTS_SECTION = (By.XPATH, "//aside[@id='woocommerce_recently_viewed_products-2']//li")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Skillbox — Интернет магазин":
            raise Exception(f"This is not main page, current page is: {self.driver.current_url}")

    def check_and_go_back_in_main_page(self):
        with allure.step('Check main page'):
            if self.get_title() != "Skillbox — Интернет магазин":
                # self.driver.get("https://intershop5.skillbox.ru")
                self.load()

    def get_catalog_and_title(self, item: int) -> tuple[WebElement, str]:
        with allure.step('Get catalogs'):
            catalogs: list[WebElement] = self.wait_for_elements(self.CATALOGS)

        with allure.step('Choose one of catalog'):
            catalog: WebElement = catalogs[item]

        with allure.step('Get title of choosen catalog'):
            catalog_title: str = self.get_element_from_another_element(catalog, By.TAG_NAME, "h4").text.capitalize()

        return catalog, catalog_title

    def go_to_product_from_sales_section(self, item: int) -> tuple[ProductPage, str]:
        with allure.step('Get products from sales section'):
            products: list[WebElement] = self.wait_for_elements(self.PRODUCTS_FROM_SALES_SECTION)

        with allure.step('Get one of the product and scroll to it'):
            product: WebElement = products[item]
            self.scroll_to_element(product)

        with allure.step('Get product title'):
            header: str = self.get_element_from_another_element(product, By.TAG_NAME, "a").get_attribute("title")

        with allure.step('Click on product'):
            product.click()

        return ProductPage(self.driver, header), header

    def go_to_product_from_new_arrivals_section(self, item: int) -> tuple[ProductPage, str]:
        with allure.step('Get products from arrivals section'):
            products: list[WebElement] = self.wait_for_elements(self.PRODUCTS_FROM_NEW_ARRIVALS_SECTION)

        with allure.step('Get one of the product and scroll to it'):
            product: WebElement = products[item]
            self.scroll_to_element(product)

        with allure.step('Get product title'):
            header: str = self.get_element_from_another_element(product, By.TAG_NAME, "a").get_attribute("title")

        with allure.step('Click on product'):
            product.click()

        return ProductPage(self.driver, header), header

    def get_product_and_title_from_poster_section(self) -> tuple[ProductPage, str]:
        with allure.step('Get poster and scroll to it'):
            poster: WebElement = self.wait_for_element(self.PRODUCT_FROM_POSTER_SECTION)
            self.scroll_to_element(poster)

        with allure.step('Get product title and button'):
            product_title: str = self.get_element_from_another_element(poster, By.CLASS_NAME, "promo-desc-title").text
            product_button: WebElement = self.wait_for_element((By.XPATH, "(//span[@class='btn promo-link-btn'])[4]"))

        with allure.step('Wait for the button to appear and click on it'):
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

    def go_to_viewed_product(self, item: int) -> tuple[ProductPage, str]:
        header = ""
        try:
            with allure.step('Get products from viewed section'):
                products: list[WebElement] = self.wait_for_elements(self.PRODUCTS_FROM_VIEWED_PRODUCTS_SECTION)

            with allure.step('Get one of the product and scroll to it'):
                product: WebElement = products[item]
                self.scroll_to_element(product)

            with allure.step('Get product title'):
                header: str = product.find_element(By.TAG_NAME, "span").text

            # with allure.step('Check product title for text - "Холодец-4"'):
                # if '"Холодец-4"' in header:
                #     header: str = self.replace_quotes(header)

            with allure.step('Get product link and go to it'):
                product_link: WebElement = product.find_element(By.TAG_NAME, "a")
                self.click_by(product_link)

        except TimeoutException:
            print("Cannot find viewed product block")

        return ProductPage(self.driver, header), header

    # def replace_quotes(self, text: str) -> str:
    #     """Replaces double quotes with herringbones in the given text."""
    #
    #     with allure.step('Replace one type of quotes `""` to another type `«»`'):
    #         new_txt = text.replace('"', '«')
    #         last_index = new_txt.rfind('«')
    #
    #         if last_index != -1:
    #             return new_txt[:last_index] + '»' + new_txt[last_index + 1:]
    #
    #         return new_txt
