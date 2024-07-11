from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import data.locators as locator
import data.test_data as test_data


class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def additional_setting(self):
        self.driver.set_page_load_timeout(40)
        self.driver.set_script_timeout(20)

    def prepare_checkout_page(self):
        self.add_item_to_cart_from_related_products_on_product_card()
        self.find_and_click_on_element(By.LINK_TEXT, locator.order_link)

        try:
            self.removing_applied_coupons()
        except TimeoutException:
            self.find_and_click_on_element(By.LINK_TEXT, locator.link_for_coupon_block_in_order_page)
            alert_of_apply_coupon = self.apply_coupon(test_data.promo_code, locator.coupon_success_applied)  # SERT500

            if len(alert_of_apply_coupon) > 0:
                print("\n" + alert_of_apply_coupon)

                # Wait when block overlay finishes his work
                self.get_element(By.XPATH, locator.overlay_block)

        return self.driver

    def remove_added_coupon(self):
        self.move_down_in_altitude_by(2.2)
        self.find_and_click_on_element(By.LINK_TEXT, locator.link_to_remove_coupon)

        return self.driver

    def add_product_to_cart_and_go_to_order_page(self):
        self.add_item_to_cart_from_related_products_on_product_card()
        self.find_and_click_on_element(By.LINK_TEXT, locator.order_link)

        return self.driver

    # Its method needs recovery data (name, last_anme and city fields) which can be empty
    # def overfilling_of_fields(self):
    #     name = self.get_element(By.ID, "billing_first_name")
    #     if len(name.text) == 0:
    #         name.send_keys("Faridun")
    #
    #     last_name = self.get_element(By.ID, "billing_last_name")
    #     if len(last_name.text) == 0:
    #         last_name.send_keys("Hushang-Mirzo")
    #
    #     city = self.get_element(By.ID, "billing_city")
    #     if len(city.text) == 0:
    #         city.send_keys("Tashkent")
    #
    #     self.find_and_submit_on_button(By.ID, "place_order")
