import logging
from time import sleep
from selenium import webdriver
from selenium.common import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Union, Literal

LOGIN_LINK_IN_HEADER: tuple[str, str] = (By.CLASS_NAME, "account")
LINK_TO_MY_ACCOUNT_PAGE_FROM_NAVBAR: tuple[str, str] = (By.XPATH, "//li[@id='menu-item-30']//a[1]")
LINK_TO_MY_ACCOUNT_PAGE_FROM_FOOTER: tuple[str, str] = (By.XPATH, "//aside[@id='pages-2']/ul[1]/li[4]/a[1]")


class BasePage:
    BASE_URL = "https://intershop5.skillbox.ru/"
    CATALOG_LINK_IN_NAVBAR: tuple[str, str] = (By.XPATH, "//li[@id='menu-item-46']")
    CATALOG_ITEMS_IN_NAVBAR: tuple[str, str] = (By.XPATH, "//li[@id='menu-item-46']/ul/li/a")
    SUB_CATALOG_ITEMS_IN_NAVBAR: tuple[str, str] = (By.XPATH, "//li[@id='menu-item-46']/ul/li/ul/li/a")
    SEARCH_FIELD: tuple[str, str] = (By.CLASS_NAME, "search-field")
    SEARCH_BUTTON: tuple[str, str] = (By.CLASS_NAME, "searchsubmit")
    CHECKOUT_ITEM_IN_NAVBAR: tuple[str, str] = (By.XPATH, "//li[@id='menu-item-31']/a")
    CHECKOUT_ITEM_IN_FOOTER: tuple[str, str] = (By.XPATH, "//aside[@id='pages-2']/ul[1]/li[5]/a")
    LOGOUT_LINK: tuple[str, str] = (By.CLASS_NAME, "logout")

    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox, webdriver.Edge]):
        self.driver = driver

        logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')
        self.logger = logging.getLogger()

    def load(self) -> None:
        self.driver.get(self.BASE_URL)

    def get_title(self) -> str:
        """
        :return: str in capitalize format
        """
        return self.driver.title.capitalize()

    def wait_for_element(self, locator: tuple[str, str], timeout: int = 10) -> WebElement:
        """
        Function wait_for_element waiting for getting element by pointed locator and return one

        :param locator: give a selector and his value
        :param timeout: int, default 10 sec.
        :return: found element
        """
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def element_is_clickable(self, locator: tuple[str, str], timeout: int = 10) -> Union[Literal[False], WebElement]:
        """
        Function element_is_clickable check element is available to click or not
        :param locator: give a selector and his value
        :param timeout: int, default 10 sec.
        :return: found element
        """
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def get_text_of_element(self, locator: tuple[str, str]) -> str:
        """
        :param locator: give a selector and his value
        :return: text of the element
        """
        return self.wait_for_element(locator).text

    def get_element_from_another_element(self, element: WebElement, selector_type: str, selector: str, timeout: int = 10) -> WebElement:
        """
        :param element: WebElement
        :param selector_type: example By.ID (CLASS, SCC_SELECTOR, NAME, XPATH and others)
        :param selector: a value that could be used to find the desired element
        :param timeout: int, default 10 sec.
        :return: found element
        """
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of(element))
        return element.find_element(selector_type, selector)

    def wait_for_elements(self, locator: tuple[str, str], timeout=10) -> list[WebElement]:
        """
        :param locator: give a selector and his value
        :param timeout: int, default 10 sec.
        :return: found elements
        """
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def get_elements_from_another_element(self, element: WebElement, selector_type: str, selector: str, timeout: int = 10) -> list[WebElement]:
        """
        :param element: WebElement
        :param selector_type: example By.ID (CLASS, SCC_SELECTOR, NAME, XPATH and others)
        :param selector: a value that could be used to find the desired elements
        :param timeout: int, default 10 sec.
        :return: found elements
        """
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of(element))
        return element.find_elements(selector_type, selector)

    def click(self, locator: tuple[str, str], timeout: int = 10) -> None:
        """
        The function click, firstly finds an element, then checks it for clickability, visibility and then clicks on it.
        :param locator: give a selector and his value
        :param timeout: int, default 10 sec.
        """
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)

        try:
            wait.until(EC.element_to_be_clickable(locator))
            wait.until(EC.visibility_of_element_located(locator))
            self.wait_for_element(locator).click()
        except StaleElementReferenceException as sere:
            self.logger.log(30, f"We get an StaleElementReferenceException - {sere.msg}")
            element = self.wait_for_element(locator)
            element.click()
        except ElementClickInterceptedException as ecie:
            self.logger.log(30, f"We get an ElementClickInterceptedException - {ecie.msg}")
            element = self.wait_for_element(locator)
            self.scroll_to(element)
            element.click()

    def click_by(self, element: WebElement, timeout: int = 10) -> None:
        """
        The function click_by, checks element for clickability, visibility and then clicks on it.
        :param element: WebElement
        :param timeout: int, default 10 sec.
        """
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.element_to_be_clickable(element))
        wait.until(EC.visibility_of(element))
        element.click()

    def type(self, locator: tuple[str, str], text: str) -> None:
        """
        :param locator: give a selector and his value
        :param text: your txt value
        """
        element: WebElement = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def go_to_catalog_page_from_navbar(self) -> None:
        self.click(self.CATALOG_LINK_IN_NAVBAR)

    def go_to_another_catalogs_page_from_navbar(self, index: int = 0) -> str:
        """
        The function go_to_another_catalogs_page_from_navbar allows you to select the desired menu item by specifying a numeric item.
        :param index: need point menu item which need choice
        :return: str, catalog title in capitalize format
        """
        general_catalog: WebElement = self.wait_for_element(self.CATALOG_LINK_IN_NAVBAR)

        action_chains: ActionChains = ActionChains(self.driver)
        action_chains.move_to_element(general_catalog).perform()

        catalog_items: list[WebElement] = self.wait_for_elements(self.CATALOG_ITEMS_IN_NAVBAR)
        catalog_item_text: str = catalog_items[index].text
        catalog_items[index].click()

        return catalog_item_text.capitalize()

    def go_to_sub_catalog_page_from_navbar(self, catalog_index: int = 0, sub_catalog_index: int = 0) -> str:
        """
        The function go_to_sub_catalog_page_from_navbar allows you to select the desired sub menu item by specifying a numeric item.
        :param catalog_index: need point menu item which need choice
        :param sub_catalog_index: need point sub menu item which need choice
        :return: str, sub catalog title in capitalize format
        """
        general_catalog: WebElement = self.wait_for_element(self.CATALOG_LINK_IN_NAVBAR)
        action_chains: ActionChains = ActionChains(self.driver)
        sleep(0.5)
        action_chains.move_to_element(general_catalog).perform()

        catalog_items: list[WebElement] = self.wait_for_elements(self.CATALOG_ITEMS_IN_NAVBAR)
        catalog_item: WebElement = catalog_items[catalog_index]
        action_chains: ActionChains = ActionChains(self.driver)
        sleep(0.3)
        action_chains.move_to_element(catalog_item).perform()

        sub_catalog_items: list[WebElement] = self.wait_for_elements(self.SUB_CATALOG_ITEMS_IN_NAVBAR)
        sub_catalog_item: WebElement = sub_catalog_items[sub_catalog_index]
        sub_catalog_item_text: str = sub_catalog_item.text

        try:
            sub_catalog_item.click()
        except Exception as e:
            self.logger.error(f"Exception - {e.args}")
            self.click_by(sub_catalog_item)

        return sub_catalog_item_text.capitalize()

    def go_to_checkout_page_from_navbar(self) -> None:
        self.click(self.CHECKOUT_ITEM_IN_NAVBAR)

    def go_to_search_page(self, search_text: str) -> None:
        """
        The go_to_search_page function takes you to a search page by specifying the search text you would like to search for
        :param search_text: str
        """
        self.type(self.SEARCH_FIELD, search_text)
        self.click(self.SEARCH_BUTTON)

    def logout_by_link(self) -> None:
        self.click(self.LOGOUT_LINK)

    def go_to_checkout_page_from_footer(self) -> None:
        self.click(self.CHECKOUT_ITEM_IN_FOOTER)

    def scroll_by(self, locator: tuple[str, str]) -> None:
        """
        :param locator: give a selector and his value
        """
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to(self, element: WebElement) -> None:
        """
        :param element: WebElement
        """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
