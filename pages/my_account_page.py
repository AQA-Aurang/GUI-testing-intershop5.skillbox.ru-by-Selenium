from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.order_page import OrderPage
from pages.account_edit_data_page import AccountEditDataPage
from typing import Union


class MyAccountPage(BasePage):
    USER_NAME_OR_EMAIL_FIELD: tuple[str, str] = (By.NAME, "username")
    PASSWORD_FIELD: tuple[str, str] = (By.NAME, "password")
    LOGIN_BUTTON: tuple[str, str] = (By.NAME, "login")
    MY_ORDERS_FROM_INFO_BLOCK: tuple[str, str] = (By.LINK_TEXT, "свои заказы")
    ORDER_BLOCK: tuple[str, str] = (By.LINK_TEXT, "Заказы")
    CHANGE_DATA_FROM_INFO_BLOCK: tuple[str, str] = (By.LINK_TEXT, "изменить данные")
    ACCOUNT_DATA_BLOCK: tuple[str, str] = (By.LINK_TEXT, "Данные аккаунта")
    LOGOUT_FROM_INFO_BLOCK: tuple[str, str] = (By.XPATH, "(//div[@class='woocommerce-MyAccount-content']//a)[1]")
    LOGOUT_BLOCK: tuple[str, str] = (By.XPATH, "//li[@class='woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--customer-logout']//a[1]")
    SUCCESS_CHANGED_DATA: tuple[str, str] = (By.CLASS_NAME, "woocommerce-message")
    ERROR_NOTIFICATION: tuple[str, str] = (By.XPATH, "//ul[@role='alert']//li[1]")

    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]):
        super().__init__(driver)

        if self.driver.title != "Мой аккаунт — Skillbox":
            raise Exception(
                f"This is not my account page, current page is: {self.driver.title} - {self.driver.current_url}")

    def authorisation(self, user_name_or_mail: str, password: str) -> Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]:
        """
        :param user_name_or_mail: str, not more 20 characters
        :param password: str, not more 20 characters
        :return: one of 3 type of webdriver - chrome, firefox, edge
        """
        self.type(self.USER_NAME_OR_EMAIL_FIELD, user_name_or_mail)
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

        return self.driver

    def go_to_orders_from_info_block(self) -> OrderPage:
        """
        The function go_to_orders_from_info need to go order list by link from info block in account page
        :return: order page
        """
        self.click(self.MY_ORDERS_FROM_INFO_BLOCK)

        return OrderPage(self.driver)

    def go_to_order_block(self) -> OrderPage:
        """
        The function go_to_order_block need to go order list from order block in main page
        :return: order page
        """
        self.click(self.ORDER_BLOCK)

        return OrderPage(self.driver)

    def go_to_account_data_block(self) -> AccountEditDataPage:
        self.click(self.ACCOUNT_DATA_BLOCK)

        return AccountEditDataPage(self.driver)

    def get_success_notif_after_update_data(self) -> str:
        """
        :return: str, success notification about updated account data
        """
        return self.wait_for_element(self.SUCCESS_CHANGED_DATA).text

    def get_error_notif_after_update_data(self) -> str:
        """
        :return: str, error notification when updating account data
        """
        return self.wait_for_element(self.ERROR_NOTIFICATION).text

    def logout_from_logout_block(self) -> None:
        self.click(self.LOGOUT_BLOCK)
