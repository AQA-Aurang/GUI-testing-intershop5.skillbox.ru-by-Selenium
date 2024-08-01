from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


LOGIN_LINK_IN_HEADER = (By.CLASS_NAME, "account")
LINK_TO_MY_ACCOUNT_PAGE_FROM_NAVBAR = (By.XPATH, "//li[@id='menu-item-30']//a[1]")
LINK_TO_MY_ACCOUNT_PAGE_FROM_FOOTER = (By.XPATH, "//aside[@id='pages-2']/ul[1]/li[4]/a[1]")


class BasePage:
    CATALOG_LINK_IN_NAVBAR = (By.XPATH, "//li[@id='menu-item-46']")
    CATALOG_ITEMS_IN_NAVBAR = (By.XPATH, "//li[@id='menu-item-46']/ul/li/a")
    SUB_CATALOG_ITEMS_IN_NAVBAR = (By.XPATH, "//li[@id='menu-item-46']/ul/li/ul/li/a")
    SEARCH_FIELD = (By.CLASS_NAME, "search-field")
    SEARCH_BUTTON = (By.CLASS_NAME, "searchsubmit")
    CHECKOUT_ITEM_IN_NAVBAR = (By.XPATH, "//li[@id='menu-item-31']/a")
    CHECKOUT_ITEM_IN_FOOTER = (By.XPATH, "//aside[@id='pages-2']/ul[1]/li[5]/a")

    def __init__(self, driver):
        self.driver = driver

    def get_title(self):
        return self.driver.title

    def wait_for_element(self, locator, timeout=10):
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def element_is_clickable(self, locator, timeout=10):
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def element_is_visible(self, locator, timeout=10):
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def get_text_of_element(self, locator):
        return self.wait_for_element(locator).text

    def get_element_from_another_element(self, element: WebElement, selector_type, selector, timeout=10):
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of(element))
        return element.find_element(selector_type, selector)

    def get_elements_from_another_element(self, element, selector_type, selector, timeout=10):
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of(element))
        return element.find_elements(selector_type, selector)

    def wait_for_elements(self, locator, timeout=10):
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait_for_element(locator).click()

    def click_by(self, element: WebElement, timeout=10):
        self.driver.implicitly_wait(0)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.element_to_be_clickable(element))
        element.click()

    def type(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def go_to_main_page_from_navbar(self):
        pass

    def go_to_catalog_page_from_navbar(self):
        self.click(self.CATALOG_LINK_IN_NAVBAR)

    def go_to_another_catalogs_page_from_navbar(self, index=0):
        general_catalog = self.wait_for_element(self.CATALOG_LINK_IN_NAVBAR)

        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(general_catalog).perform()

        catalog_items = self.wait_for_elements(self.CATALOG_ITEMS_IN_NAVBAR)
        catalog_item_text = catalog_items[index].text
        catalog_items[index].click()

        return catalog_item_text.capitalize()

    def go_to_sub_catalog_page_from_navbar(self, catalog_index=0, sub_catalog_index=0):
        general_catalog = self.wait_for_element(self.CATALOG_LINK_IN_NAVBAR)
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(general_catalog).perform()

        catalog_items = self.wait_for_elements(self.CATALOG_ITEMS_IN_NAVBAR)
        catalog_item = catalog_items[catalog_index]
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(catalog_item).perform()

        sub_catalog_items = self.wait_for_elements(self.SUB_CATALOG_ITEMS_IN_NAVBAR)
        sub_catalog_item = sub_catalog_items[sub_catalog_index]
        sub_catalog_item_text = sub_catalog_item.text
        sub_catalog_item.click()

        return sub_catalog_item_text.capitalize()

    def go_to_cart_page_from_navbar(self):
        pass

    def go_to_checkout_page_from_navbar(self):
        self.click(self.CHECKOUT_ITEM_IN_NAVBAR)

    def go_to_search_page(self, search_text):
        self.type(self.SEARCH_FIELD, search_text)
        self.click(self.SEARCH_BUTTON)

    def go_to_all_products_from_footer(self):
        pass

    def go_to_main_page_from_footer(self):
        pass

    def go_to_cart_page_from_footer(self):
        pass

    def go_to_my_account_page_from_footer(self):
        pass

    def go_to_checkout_page_from_footer(self):
        self.click(self.CHECKOUT_ITEM_IN_FOOTER)

    def go_to_registration_page_from_footer(self):
        pass

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
