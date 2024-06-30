from .base_types import BaseType
from .base_page import BasePage
from selenium.webdriver.common.by import By
from interhsop5skillbox.pages.base_page import get_element_in_another_element
from selenium.common.exceptions import TimeoutException
import interhsop5skillbox.data.locators as locator
import interhsop5skillbox.data.test_data as test_data


class CartPage(BasePage):
    def __init__(self, driver: BaseType):
        super().__init__(driver)

    def remove_product_added_in_cart(self):
        title_product = self.add_item_to_cart_from_related_products_on_product_card()

        removed_link_product = self.get_element(By.LINK_TEXT, title_product)
        parent_tr_element = get_element_in_another_element(
            get_element_in_another_element(removed_link_product, By.XPATH, "./.."), By.XPATH, "./..")

        remove_icon = get_element_in_another_element(
            get_element_in_another_element(parent_tr_element, By.TAG_NAME, "td"), By.TAG_NAME, "a")
        self.click_element(remove_icon)

        return title_product

    def apply_promo_code(self):
        try:
            alert_of_apply_coupon = self.apply_coupon(test_data.promo_code, locator.notification_element)

            if len(alert_of_apply_coupon) > 0:
                self.get_element(By.XPATH, locator.overlay_block2)

                return alert_of_apply_coupon
        except TimeoutException:
            return self.get_element(By.XPATH, locator.not_success_alert).text
