from selenium.webdriver.common.by import By
from pages2.base_page import BasePage

NAME_FIELD = (By.ID, "account_first_name")
SECOND_NAME_FIELD = (By.ID, "account_last_name")
DISPLAY_FIELD = (By.ID, "account_display_name")
EMAIL_FIELD = (By.ID, "account_email")


class AccountEditDataPage(BasePage):
    PAGE_HEADER = (By.CLASS_NAME, "post-title")
    CURRENT_PASSWORD_FIELD = (By.ID, "password_current")
    NEW_PASSWORD_FIELD = (By.ID, "password_1")
    REPEAT_NEW_PASSWORD_FIELD = (By.ID, "password_2")
    SAVE_BUTTON = (By.NAME, "save_account_details")

    def __init__(self, driver):
        super().__init__(driver)

        if self.wait_for_element(self.PAGE_HEADER).text != "Данные учетной записи":
            raise Exception(
                f"This is not account edit data page, current page is: {self.driver.title} - {self.driver.current_url}")

    def modify_field(self, locator, new_value):
        self.type(locator, new_value)
        self.click(self.SAVE_BUTTON)

    def change_password(self, current_password, new_password, repeat_new_password):
        self.type(self.CURRENT_PASSWORD_FIELD, current_password)
        self.type(self.NEW_PASSWORD_FIELD, new_password)
        self.modify_field(self.REPEAT_NEW_PASSWORD_FIELD, repeat_new_password)
