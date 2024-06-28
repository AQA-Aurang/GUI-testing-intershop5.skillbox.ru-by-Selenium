import time

from selenium.webdriver.common.by import By

from .base_page import BasePage
from .base_page import get_element_in_another_element, get_elements_in_another_element
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MyAccountPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def login_with_data(self, username, password):
        element = self.get_element(By.LINK_TEXT, "Войти")
        self.click_element(element)

        self.get_element(By.ID, "username").send_keys(username)
        self.get_element(By.ID, "password").send_keys(password)
        element = self.get_element(By.NAME, "login")
        self.click_element(element)

        WebDriverWait(self.driver, 10).until(EC.title_contains("Мой аккаунт"))

        return self.driver

    def wait_account_title(self, title_page):
        WebDriverWait(self.driver, 10).until(EC.title_contains(title_page))

    def verify_account_title(self, account, title):
        self.click_element(account)
        self.wait_account_title(title)

        return self.driver

    def text_match_with_header(self, type_of_locator, locator, text, err_description):
        page_header = self.get_element(type_of_locator, locator)
        assert text in page_header.text, err_description

    def searching_specific_order_or_receiving_text_about_no_orders(self, type_of_locator, locator):
        element = self.get_element(type_of_locator, locator)

        try:
            assert element.is_displayed() and element.text.split("\n")[1] == "Заказов еще нет.", \
                "Orders have been placed"
        except IndexError:
            table_body = self.get_element(By.TAG_NAME, "tbody")
            table_body_rows = get_elements_in_another_element(table_body, By.TAG_NAME, "tr")

            if len(table_body_rows) > 0:
                first_row = get_element_in_another_element(table_body_rows[0], By.LINK_TEXT, "Подробнее")
                self.click_element(first_row)
                self.text_match_with_header(By.CLASS_NAME, "post-title", "Order",
                                            "Cannot get more data about order")

    def navigation_to_personal_details(self):
        personal_data_block = self.get_element(By.LINK_TEXT, "Данные аккаунта")
        self.click_element(personal_data_block)

        return self.driver

    def print_in_field(self, type_of_locator, locator, new_value):
        field = self.get_element(type_of_locator, locator)
        field.clear()
        field.send_keys(new_value)

        return self.driver

    def modify_one_of_the_field_and_check(self, locator, new_value):
        self.driver = self.navigation_to_personal_details()
        self.driver = self.print_in_field(By.ID, locator, new_value)

        # save modification
        self.find_and_click_on_element(By.NAME, "save_account_details")

        # getting field data and check
        self.find_and_click_on_element(By.LINK_TEXT, "Данные аккаунта")
        updated_field = self.get_element(By.ID, locator).get_attribute("value")

        assert updated_field == new_value, f"Expected updated name: {new_value}, Actual updated name: {updated_field}"

    def change_password_fields(self, current_pass, new_pass, repeat_new_pass):
        self.print_in_field(By.ID, "password_current", current_pass)
        self.print_in_field(By.ID, "password_1", new_pass)
        self.print_in_field(By.ID, "password_2", repeat_new_pass)
        self.find_and_click_on_element(By.NAME, "save_account_details")

        return self.driver

    def revert_password(self, current_password):
        self.driver = self.login_with_data(self.default_username, current_password)
        self.find_and_click_on_element(By.LINK_TEXT, "Данные аккаунта")
        self.wait_account_title("Мой аккаунт — Skillbox")
        self.change_password_fields(current_password, self.default_password, self.default_password)
        self.get_element(By.CLASS_NAME, "woocommerce-message")

    def logout_and_login(self):
        # logout the account
        self.driver.execute_script("window.scrollTo(0, 0);")

        time.sleep(2)
        logout_link = self.get_element(By.LINK_TEXT, "Выйти")
        self.click_element(logout_link)

        # login the account
        element = self.get_element(By.LINK_TEXT, "Войти")
        self.click_element(element)
        self.get_element(By.ID, "username").send_keys(self.default_username)
        self.get_element(By.ID, "password").send_keys(self.default_password)
        element = self.get_element(By.NAME, "login")
        self.click_element(element)

        WebDriverWait(self.driver, 10).until(EC.title_contains("Мой аккаунт"))

        return self.driver
