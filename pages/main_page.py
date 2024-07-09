from .base_page import BasePage, get_element_in_another_element
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_sub_catalog_title(self, element_text):
        while True:
            element = self.get_element(By.XPATH, f"//h4[text()='{element_text}']")

            if element.is_displayed():
                return element.text

    def go_to_sub_catalog_from_main_page(self, locator, subcatalog_title, another_expected_result=""):
        # Checking sub catalog
        sub_catalog = self.get_element(By.ID, locator)
        sub_catalog_title = another_expected_result.upper() if another_expected_result != "" \
            else self.get_sub_catalog_title(subcatalog_title)

        link_in_subcatalog = get_element_in_another_element(sub_catalog, By.TAG_NAME, "a")
        self.click_element(link_in_subcatalog)

        element_on_page = another_expected_result if another_expected_result != "" else subcatalog_title
        self.element_should_have_text(By.XPATH, f"//h1[text()='{element_on_page}']", sub_catalog_title,
                                     f"Cannot redirect to '{element_on_page}' sub catalog from main page")
