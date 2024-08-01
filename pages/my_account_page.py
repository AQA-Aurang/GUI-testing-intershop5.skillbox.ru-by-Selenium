from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from .order_page import OrderPage
from .account_edit_data_page import AccountEditDataPage


class MyAccountPage(BasePage):
    USER_NAME_OR_EMAIL_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.NAME, "login")
    MY_ORDERS_FROM_INFO_BLOCK = (By.LINK_TEXT, "свои заказы")
    ORDER_BLOCK = (By.LINK_TEXT, "Заказы")
    CHANGE_DATA_FROM_INFO_BLOCK = (By.LINK_TEXT, "изменить данные")
    ACCOUNT_DATA_BLOCK = (By.LINK_TEXT, "Данные аккаунта")
    LOGOUT_FROM_INFO_BLOCK = (By.XPATH, "(//div[@class='woocommerce-MyAccount-content']//a)[1]")
    LOGOUT_BLOCK = (By.XPATH, "//li[@class='woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--customer-logout']//a[1]")
    SUCCESS_CHANGED_DATA = (By.CLASS_NAME, "woocommerce-message")
    ERROR_NOTIFICATION = (By.XPATH, "//ul[@role='alert']//li[1]")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Мой аккаунт — Skillbox":
            raise Exception(
                f"This is not my account page, current page is: {self.driver.title} - {self.driver.current_url}")

    def authorisation(self, user_name_or_mail, password):
        self.type(self.USER_NAME_OR_EMAIL_FIELD, user_name_or_mail)
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

        return self.driver

    def go_to_my_orders_from_info_block(self):
        self.click(self.MY_ORDERS_FROM_INFO_BLOCK)

        return OrderPage(self.driver)

    def go_to_order_block(self):
        self.click(self.ORDER_BLOCK)

        return OrderPage(self.driver)

    def go_to_edit_my_account_data_from_info_block(self):
        self.click(self.CHANGE_DATA_FROM_INFO_BLOCK)

        return AccountEditDataPage(self.driver)

    def go_to_account_data_block(self):
        self.click(self.ACCOUNT_DATA_BLOCK)

        return AccountEditDataPage(self.driver)

    def get_text_after_action(self):
        return self.wait_for_element(self.SUCCESS_CHANGED_DATA).text

    def get_error_notification(self):
        return self.wait_for_element(self.ERROR_NOTIFICATION).text

    def logout_by_link_from_info_block(self):
        self.click(self.LOGOUT_FROM_INFO_BLOCK)

    def logout_from_logout_block(self):
        self.click(self.LOGOUT_BLOCK)
