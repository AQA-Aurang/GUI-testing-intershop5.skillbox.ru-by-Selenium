from typing import Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

NAME_FIELD: tuple[str, str] = (By.ID, "account_first_name")
SECOND_NAME_FIELD: tuple[str, str] = (By.ID, "account_last_name")
DISPLAY_FIELD: tuple[str, str] = (By.ID, "account_display_name")
EMAIL_FIELD: tuple[str, str] = (By.ID, "account_email")


class AccountEditDataPage(BasePage):
    PAGE_HEADER: tuple[str, str] = (By.CLASS_NAME, "post-title")
    CURRENT_PASSWORD_FIELD: tuple[str, str] = (By.ID, "password_current")
    NEW_PASSWORD_FIELD: tuple[str, str] = (By.ID, "password_1")
    REPEAT_NEW_PASSWORD_FIELD: tuple[str, str] = (By.ID, "password_2")
    SAVE_BUTTON: tuple[str, str] = (By.NAME, "save_account_details")

    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]):
        super().__init__(driver)

        if self.wait_for_element(self.PAGE_HEADER).text != "Данные учетной записи":
            raise Exception(
                f"This is not account edit data page, current page is: {self.driver.title} - {self.driver.current_url}")

    def modify_field(self, locator: tuple[str, str], new_value: str) -> None:
        """
        The function modify_field save after updated field
        :param locator: give a selector and his value
        :param new_value: new value fo found field
        """
        self.type(locator, new_value)
        self.click(self.SAVE_BUTTON)

    def change_password(self, current_password: str, new_password: str, repeat_new_password: str) -> None:
        """
        :param current_password: str, not more 20 characters
        :param new_password: str, not more 20 characters
        :param repeat_new_password: str, not more 20 characters
        """
        self.type(self.CURRENT_PASSWORD_FIELD, current_password)
        self.type(self.NEW_PASSWORD_FIELD, new_password)
        self.modify_field(self.REPEAT_NEW_PASSWORD_FIELD, repeat_new_password)
