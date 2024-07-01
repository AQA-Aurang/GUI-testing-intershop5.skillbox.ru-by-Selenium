import interhsop5skillbox.data.locators as locator
from .base_page import BasePage
from .base_page import BaseType
from .base_page import get_element_in_another_element
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class CatalogAndSubCatalogPage(BasePage):

    def __init__(self, driver: BaseType):
        super().__init__(driver)

    def go_to_catalog_of_product(self):
        self.find_and_click_on_element(By.LINK_TEXT, locator.catalog_link)

    def point_move_and_click_on_element(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element).perform()
        self.find_and_click_on_element(By.XPATH, locator.element_in_dropdown)

        return self.driver

    def point_and_click(self, element):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element).click()

        return self.driver

    def get_selected_item_and_assert(self, expected_text, err_description):
        sort_element = self.get_element(By.NAME, locator.sorting_element)
        default_item_in_sort_element = get_element_in_another_element(sort_element, By.XPATH,
                                                                      locator.selected_element_in_sorting_block)
        assert default_item_in_sort_element.text == expected_text, err_description

    def change_slider(self, point, pixel_offset, slider_xpath, err_description):
        self.move_down_in_altitude_by(point)
        slider = self.get_element(By.XPATH, slider_xpath)

        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(slider, pixel_offset, 0).perform()
        fixed_price_str = self.get_element(By.XPATH, locator.price_xpath1).text
        fixed_price = float(fixed_price_str[:-1])
        self.find_and_click_on_element(By.XPATH, locator.apply_for_sliders)

        products = self.get_elements(By.XPATH, locator.products_after_sliders_apply)
        for product in products:
            price_element = get_element_in_another_element(product, By.XPATH, locator.product_price)
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
