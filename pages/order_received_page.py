from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class OrderReceivedPage(BasePage):
    ORDER_RECEIVED = (By.XPATH, "//h2[text()='Заказ получен']")

    def __int__(self, driver):
        super().__init__(driver)

        if self.get_title() != "Заказ получен":
            raise Exception(f"This is not order received page, url current page is: {self.driver.current_url}")

    def get_title(self):
        return self.get_text_of_element(self.ORDER_RECEIVED)
