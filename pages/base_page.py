import logging

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import TypeVar, Union

LOGIN_LINK_IN_HEADER = (By.CLASS_NAME, "account")
LINK_TO_MY_ACCOUNT_PAGE_FROM_NAVBAR = (By.XPATH, "//li[@id='menu-item-30']//a[1]")
LINK_TO_MY_ACCOUNT_PAGE_FROM_FOOTER = (By.XPATH, "//aside[@id='pages-2']/ul[1]/li[4]/a[1]")


class BasePage:
    BASE_URL = "https://intershop5.skillbox.ru/"
    CATALOG_LINK_IN_NAVBAR = (By.XPATH, "//li[@id='menu-item-46']")
    CATALOG_ITEMS_IN_NAVBAR = (By.XPATH, "//li[@id='menu-item-46']/ul/li/a")
    SUB_CATALOG_ITEMS_IN_NAVBAR = (By.XPATH, "//li[@id='menu-item-46']/ul/li/ul/li/a")
    SEARCH_FIELD = (By.CLASS_NAME, "search-field")
    SEARCH_BUTTON = (By.CLASS_NAME, "searchsubmit")
    CHECKOUT_ITEM_IN_NAVBAR = (By.XPATH, "//li[@id='menu-item-31']/a")
    CHECKOUT_ITEM_IN_FOOTER = (By.XPATH, "//aside[@id='pages-2']/ul[1]/li[5]/a")
    LOGOUT_LINK = (By.CLASS_NAME, "logout")

    T = TypeVar("T")

    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]):
        self.driver = driver

        logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')
        self.logger = logging.getLogger()

    def load(self) -> None:
        self.driver.get(self.BASE_URL)

    def get_title(self) -> str:
        return self.driver.title

    def wait_for_element(self, locator: tuple[str, str], timeout=10) -> T:
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def element_is_clickable(self, locator: tuple[str, str], timeout=10) -> T:
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def element_is_visible(self, locator: tuple[str, str], timeout=10) -> T:
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def get_text_of_element(self, locator: tuple[str, str]) -> str:
        return self.wait_for_element(locator).text

    def get_element_from_another_element(self, element: WebElement, selector_type: str, selector: str, timeout=10) -> WebElement:
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of(element))
        return element.find_element(selector_type, selector)

    def get_elements_from_another_element(self, element: WebElement, selector_type: str, selector: str, timeout=10) -> list[WebElement]:
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of(element))
        return element.find_elements(selector_type, selector)

    def wait_for_elements(self, locator: tuple[str, str], timeout=10) -> list[WebElement]:
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: tuple[str, str]) -> None:
        self.wait_for_element(locator).click()

    def click_by(self, element: WebElement, timeout=10) -> None:
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.element_to_be_clickable(element))
        element.click()

    def type(self, locator: tuple[str, str], text: str) -> None:
        element: WebElement = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def go_to_catalog_page_from_navbar(self) -> None:
        self.click(self.CATALOG_LINK_IN_NAVBAR)

    def go_to_another_catalogs_page_from_navbar(self, index: int = 0) -> str:
        general_catalog: WebElement = self.wait_for_element(self.CATALOG_LINK_IN_NAVBAR)

        action_chains: ActionChains = ActionChains(self.driver)
        action_chains.move_to_element(general_catalog).perform()

        catalog_items: list[WebElement] = self.wait_for_elements(self.CATALOG_ITEMS_IN_NAVBAR)
        catalog_item_text: str = catalog_items[index].text
        catalog_items[index].click()

        return catalog_item_text.capitalize()

    def go_to_sub_catalog_page_from_navbar(self, catalog_index: int = 0, sub_catalog_index: int = 0) -> str:
        general_catalog: WebElement = self.wait_for_element(self.CATALOG_LINK_IN_NAVBAR)
        action_chains: ActionChains = ActionChains(self.driver)
        action_chains.move_to_element(general_catalog).perform()

        catalog_items: list[WebElement] = self.wait_for_elements(self.CATALOG_ITEMS_IN_NAVBAR)
        catalog_item: WebElement = catalog_items[catalog_index]
        action_chains: ActionChains = ActionChains(self.driver)
        action_chains.move_to_element(catalog_item).perform()

        sub_catalog_items: list[WebElement] = self.wait_for_elements(self.SUB_CATALOG_ITEMS_IN_NAVBAR)
        sub_catalog_item: WebElement = sub_catalog_items[sub_catalog_index]
        sub_catalog_item_text: str = sub_catalog_item.text
        sub_catalog_item.click()

        return sub_catalog_item_text.capitalize()

    def go_to_checkout_page_from_navbar(self) -> None:
        self.click(self.CHECKOUT_ITEM_IN_NAVBAR)

    def go_to_search_page(self, search_text) -> None:
        self.type(self.SEARCH_FIELD, search_text)
        self.click(self.SEARCH_BUTTON)

    def logout_by_link(self) -> None:
        self.click(self.LOGOUT_LINK)

    def go_to_checkout_page_from_footer(self) -> None:
        self.click(self.CHECKOUT_ITEM_IN_FOOTER)

    def scroll_to_element(self, element) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
