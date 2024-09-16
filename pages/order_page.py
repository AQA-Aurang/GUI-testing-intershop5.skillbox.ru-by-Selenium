from typing import Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
from pages.order_detail_page import OrderDetailPage


class OrderPage(BasePage):
    TITLE = (By.CLASS_NAME, "post-title")
    ORDERS = (By.XPATH, "//tr[contains(@class, 'woocommerce-orders-table__row')]")

    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]):
        super().__init__(driver)

        if self.driver.title != "Мой аккаунт — Skillbox":
            raise Exception(
                f"This is not order page, current page is: {self.driver.title} - {self.driver.current_url}")

    def get_title(self) -> str:
        return self.wait_for_element(self.TITLE).text

    def get_orders(self) -> list[WebElement]:
        """
        :return: list of WebElement
        """
        return self.wait_for_elements(self.ORDERS)

    def get_title_and_link(self, element: WebElement, index: int = 0) -> tuple[str, WebElement]:
        """
        :param element: WebElement
        :param index: int, item from list of items
        :return: str, title of product; WebElement, link element
        """
        title: str = self.get_element_from_another_element(element, By.XPATH, "//a[contains(text(), '№')]").text
        title: str = title.replace("№", "")
        link: WebElement = self.get_element_from_another_element(element, By.XPATH, f"(//td[@data-title='Действия']//a)[{index+1}]")
        return title, link

    def go_to_order_detail_page_after_click_to(self, element: WebElement) -> OrderDetailPage:
        """
        :param element: WebElement, often its link
        :return: object order detail page
        """
        self.click_by(element)

        return OrderDetailPage(self.driver)
