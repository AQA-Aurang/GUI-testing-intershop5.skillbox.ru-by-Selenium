import time
import interhsop5skillbox.data.locators as locator
import interhsop5skillbox.data.test_data as test_data
from selenium.webdriver.common.by import By
from .base_page import BasePage
from .base_page import BaseType
from .base_page import get_element_in_another_element, get_elements_in_another_element
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyAccountPage(BasePage):

    def __init__(self, driver: BaseType):
        super().__init__(driver)

    def login_with_data(self, username, password):
        self.find_and_click_on_element(By.LINK_TEXT, locator.login_link_in_my_account)
        self.print_in_field(By.ID, locator.username_id, username)
        self.print_in_field(By.ID, locator.password_id, password)
        self.find_and_click_on_element(By.NAME, locator.login_button)
        self.wait_account_title(test_data.main_header_in_account_page)

        return self.driver

    def wait_account_title(self, title_page):
        WebDriverWait(self.driver, 10).until(EC.title_contains(title_page))

    def verify_account_title(self, account, title):
        self.click_element(account)
        self.wait_account_title(title)

        return self.driver

    # def text_match_with_header(self, type_of_locator, locator, text, err_description):
    #     page_header = self.get_element(type_of_locator, locator)
    #     assert text in page_header.text, err_description

    def searching_specific_order_or_receiving_text_about_no_orders(self, type_of_locator, locator_elem):
        element = self.get_element(type_of_locator, locator_elem)

        try:
            assert element.is_displayed() and element.text.split("\n")[1] == test_data.no_orders_yet, \
                test_data.orders_been_placed
        except IndexError:
            table_body = self.get_element(By.TAG_NAME, "tbody")
            table_body_rows = get_elements_in_another_element(table_body, By.TAG_NAME, "tr")

            if len(table_body_rows) > 0:
                first_row = get_element_in_another_element(table_body_rows[0], By.LINK_TEXT, locator.order_detail)
                self.click_element(first_row)
                self.expected_text_consist_in_searching_element(By.CLASS_NAME, locator.title_in_my_account,
                                                test_data.order, test_data.assertion_error_cannot_get_detail_for_order)

    def navigation_to_personal_details(self):
        personal_data_block = self.get_element(By.LINK_TEXT, locator.account_data)
        self.click_element(personal_data_block)

        return self.driver

    def modify_one_of_the_field_and_check(self, locator_elem, new_value):
        self.driver = self.navigation_to_personal_details()
        self.driver = self.print_in_field(By.ID, locator_elem, new_value)

        # save modification
        self.find_and_click_on_element(By.NAME, locator.save_button_for_changed_data)

        # getting field data and check
        self.find_and_click_on_element(By.LINK_TEXT, locator.account_data)
        updated_field = self.get_element(By.ID, locator_elem).get_attribute("value")

        assert updated_field == new_value, f"Expected updated name: {new_value}, Actual updated name: {updated_field}"

    def change_password_fields(self, current_pass, new_pass, repeat_new_pass):
        self.print_in_field(By.ID, locator.current_password, current_pass)
        self.print_in_field(By.ID, locator.new_password, new_pass)
        self.print_in_field(By.ID, locator.repeat_new_password, repeat_new_pass)
        self.find_and_click_on_element(By.NAME, locator.save_button_for_changed_data)

        return self.driver

    def revert_password(self, current_password):
        self.driver = self.login_with_data(self.default_username, current_password)
        self.find_and_click_on_element(By.LINK_TEXT, locator.account_data)
        self.wait_account_title(test_data.title_in_account_page)
        self.change_password_fields(current_password, self.default_password, self.default_password)
        self.get_element(By.CLASS_NAME, locator.alert_notification_in_personal_block_in_my_account)

    def logout_and_login(self):
        # logout the account
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        self.find_and_click_on_element(By.LINK_TEXT, locator.logout_link)

        # login the account
        self.find_and_click_on_element(By.LINK_TEXT, locator.login_link_in_my_account)
        self.print_in_field(By.ID, locator.username_id, self.default_username)
        self.print_in_field(By.ID, locator.password_id, self.default_password)
        self.find_and_click_on_element(By.NAME, locator.login_button)
        self.wait_account_title(locator.my_account_link_in_my_account)

        return self.driver
