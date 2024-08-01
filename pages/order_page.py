from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.order_detail_page import OrderDetailPage


class OrderPage(BasePage):
    TITLE = (By.CLASS_NAME, "post-title")
    ORDERS = (By.XPATH, "//tr[contains(@class, 'woocommerce-orders-table__row')]")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Мой аккаунт — Skillbox":
            raise Exception(
                f"This is not order page, current page is: {self.driver.title} - {self.driver.current_url}")

    def get_title(self):
        return self.wait_for_element(self.TITLE).text

    def get_orders(self):
        return self.wait_for_elements(self.ORDERS)

    def get_title_and_link(self, element, index=0):
        title = self.get_element_from_another_element(element, By.XPATH, "//a[contains(text(), '№')]").text
        title = title.replace("№", "")
        link = self.get_element_from_another_element(element, By.XPATH, f"(//td[@data-title='Действия']//a)[{index+1}]")
        return title, link

    def click_by_this(self, element):
        self.click_by(element)

        return OrderDetailPage(self.driver)
