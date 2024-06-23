import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

usernames = ["Faridun5", "Ferdinand"]
passwords = ["ValayBalay", "ValaVala123'"]


def get_element(driver, selector, prompt):
    return WebDriverWait(driver, 20).until(EC.presence_of_element_located((selector, prompt)))


def get_element_experimental(driver, selector, prompt):
    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((selector, prompt)))
        return element

    except TimeoutException as t:
        print(f"TimeoutException in getting element - {t.args[0]}")
        return driver


def get_element_lt(driver, selector, prompt):
    return WebDriverWait(driver, 30).until(EC.presence_of_element_located((selector, prompt)))


def get_elements(driver, selector, prompt):
    return WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((selector, prompt)))


def get_elements_experimental(driver, selector, prompt):
    try:
        elements = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((selector, prompt)))
        return elements

    except TimeoutException as t:
        print(f"TimeoutException in getting elements - {t.args}")
        return WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((selector, prompt)))


def get_elements_lt(driver, selector, prompt):
    return WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((selector, prompt)))


def login(driver):
    get_element(driver, By.LINK_TEXT, "Войти").click()
    get_element(driver, By.ID, "username").send_keys(usernames[1])
    get_element(driver, By.ID, "password").send_keys(passwords[1])
    get_element(driver, By.NAME, "login").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт"))

    return driver


def login_with_data(driver, username, password):
    get_element(driver, By.LINK_TEXT, "Войти").click()
    get_element(driver, By.ID, "username").send_keys(username)
    get_element(driver, By.ID, "password").send_keys(password)
    get_element(driver, By.NAME, "login").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт"))

    return driver


def logout(driver):
    get_element(driver, By.NAME, "Выйти").click()


def logout_experiment(driver):
    driver.execute_script("window.scrollTo(0, 0);")

    time.sleep(5)
    logout_link = get_element(driver, By.LINK_TEXT, "Выйти")
    # print("logout_link displayed -", logout_link.is_displayed())
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(logout_link))
    logout_link.click()


def go_to_product(driver):
    driver.get("https://intershop5.skillbox.ru")
    get_element(driver, By.XPATH, "(//li[@data-slick-index='0'])[1]/div/a").click()
