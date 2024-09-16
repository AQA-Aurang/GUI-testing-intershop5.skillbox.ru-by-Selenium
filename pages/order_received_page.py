from typing import Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OrderReceivedPage(BasePage):
    ORDER_RECEIVED: tuple[str, str] = (By.XPATH, "//h2[text()='Заказ получен']")
    PAYMENT_METHOD: tuple[str, str] = (By.XPATH, "//li[@class='woocommerce-order-overview__payment-method method']")

    def __int__(self, driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]):
        super().__init__(driver)

        if self.get_title() != "Заказ получен":
            raise Exception(f"This is not order received page, url current page is: {self.driver.current_url}")

    def get_title(self) -> str:
        return self.get_text_of_element(self.ORDER_RECEIVED)

    def get_payment_method(self) -> str:
        return self.get_text_of_element(self.PAYMENT_METHOD)
