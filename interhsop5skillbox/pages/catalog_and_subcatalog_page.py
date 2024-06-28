import time
from .base_page import BasePage
from .base_page import get_element_in_another_element, get_elements_in_another_element
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException


class CatalogAndSubCatalogPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def go_to_catalog_of_product(self):
        self.find_and_click_on_element(By.LINK_TEXT, "КАТАЛОГ")

    def point_move_and_click_on_element(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element).perform()
        self.find_and_click_on_element(By.XPATH, "//li[@id='menu-item-119']/a[1]")

        return self.driver

    def point_and_click(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element).click()

        return self.driver

    def get_selected_item_and_assert(self, expected_text, err_description):
        sort_element = self.get_element(By.NAME, "orderby")
        default_item_in_sort_element = get_element_in_another_element(sort_element, By.XPATH,
                                                                      "//option[@selected='selected']")
        assert default_item_in_sort_element.text == expected_text, err_description

    # def receiving_and_going_through_the_products_and_checking_out(self, fixed_price, err_description):
    #     products = self.get_elements(By.XPATH, "//ul[@class='products columns-4']/li")
    #     for product in products:
    #         price_element = get_element_in_another_element(product, By.XPATH,
    #                                                        "(//span[@class='woocommerce-Price-amount amount']//bdi)[1]")
    #         price_str = price_element.text[:-1].replace(",", ".")
    #         price = float(price_str)
    #         assert price >= fixed_price, err_description

    def change_slider(self, point, pixel_offset, slider_xpath, err_description):
        self.move_down_in_altitude_by(point)
        slider = self.get_element(By.XPATH, slider_xpath)

        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(slider, pixel_offset, 0).perform()
        fixed_price_str = self.get_element(By.XPATH, "//div[@class='price_label']//span[1]").text
        fixed_price = float(fixed_price_str[:-1])
        self.find_and_click_on_element(By.XPATH, "(//button[@type='submit'])[2]")

        products = self.get_elements(By.XPATH, "//ul[@class='products columns-4']/li")
        for product in products:
            price_element = get_element_in_another_element(product, By.XPATH,
                                                           "(//span[@class='woocommerce-Price-amount amount']//bdi)[1]")
            price_str = price_element.text[:-1].replace(",", ".")
            price = float(price_str)
            assert price >= fixed_price, err_description

    def get_price(self, slider_xpath, price_xpath, offset):
        slider = self.get_element(By.XPATH, slider_xpath)
        self.click_element(slider)

        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(slider, offset, 0).perform()
        fixed_price_str = self.get_element(By.XPATH, price_xpath).text
        return self.driver, float(fixed_price_str[:-1])

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def expected_text_consist_in_searching_element(self, type_of_locator, locator, text, err_description):
        element = self.get_element(type_of_locator, locator)
        assert text in element.text, err_description
