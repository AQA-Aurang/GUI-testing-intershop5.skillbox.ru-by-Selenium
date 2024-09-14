from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class OrderDetailPage(BasePage):
    TITLE: tuple[str, str] = (By.CLASS_NAME, "post-title")
    PRODUCT: tuple[str, str] = (By.XPATH, "//td[@class='woocommerce-table__product-name product-name']//a[1]")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Мой аккаунт — Skillbox":
            raise Exception(
                f"This is not order detail page, current page is: {self.driver.title} - {self.driver.current_url}")

    def get_title(self) -> str:
        return self.wait_for_element(self.TITLE).text

    def get_product(self) -> WebElement:
        return self.wait_for_element(self.PRODUCT)
