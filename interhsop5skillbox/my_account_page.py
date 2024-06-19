import pytest
import interhsop5skillbox.utilities as utilities
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)

    yield wd
    wd.quit()

# -------------------------------------------------

# Инофрмация на стр. Мой аккаунт
def test_go_to_my_account_from_link_navbar(driver):
    driver.get("http://intershop5.skillbox.ru")
    utilities.get_element(driver, By.LINK_TEXT, "Мой аккаунт").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))

    header_in_logging_page = utilities.get_element(driver, By.CLASS_NAME, "post-title")
    assert header_in_logging_page.text == "Мой аккаунт", "Cannot go to my account by link in navbar"


def test_go_to_my_account_from_login_link(driver):
    driver.get("http://intershop5.skillbox.ru")
    utilities.get_element(driver, By.LINK_TEXT, "Мой аккаунт").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))

    header_in_logging_page = utilities.get_element(driver, By.CLASS_NAME, "post-title")
    assert header_in_logging_page.text == "Мой аккаунт", "Cannot go to my account by login link"


def test_go_to_my_account_from_footer_link(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    utilities.get_element(driver, By.LINK_TEXT, "Мой аккаунт").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))

    header_in_logging_page = utilities.get_element(driver, By.CLASS_NAME, "post-title")
    assert header_in_logging_page.text == "Мой аккаунт", "Cannot go to my account by link in the footer"


# Заказы на стр. Мой аккаунт
def test_go_to_orders_from_info_block_after_auth(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver = utilities.login(driver)
    utilities.get_element(driver, By.LINK_TEXT, "свои заказы").click()
    header_in_logging_page = utilities.get_element(driver, By.CLASS_NAME, "post-title")

    assert header_in_logging_page.text == "Заказы", "Cannot go to orders by info block"

    utilities.logout(driver)


def test_go_to_orders_after_auth(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver = utilities.login(driver)
    utilities.get_element(driver, By.LINK_TEXT, "Заказы").click()
    header_in_logging_page = utilities.get_element(driver, By.CLASS_NAME, "post-title")

    assert header_in_logging_page.text == "Заказы", "Cannot go to orders by orders"

    utilities.logout(driver)


# Страница заказанного товара
def test_go_to_order_details(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver = utilities.login(driver)

    # User[0] doesn't have some orders. Below code need for test logic in try block
    # driver = utilities.login_with_data(driver, utilities.usernames[0], utilities.passwords[0])

    utilities.get_element(driver, By.LINK_TEXT, "Заказы").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))
    element = utilities.get_element(driver, By.XPATH, "//div[@class='woocommerce-MyAccount-content']/div[2]")

    try:
        assert element.is_displayed() and element.text.split("\n")[1] == "Заказов еще нет.", \
            "Orders have been placed"
    except IndexError:
        table_body_rows = utilities.get_element(driver, By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

        if len(table_body_rows) > 0:
            table_body_rows[0].find_element(By.LINK_TEXT, "Подробнее").click()
            header_in_order_page = utilities.get_element(driver, By.CLASS_NAME, "post-title").text

            assert "Order" in header_in_order_page, "Cannot get more data about order"

    utilities.logout(driver)


# Данные аккаунта на стр. Мой аккаунт
def navigation_to_personal_details(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver = utilities.login(driver)
    utilities.get_element(driver, By.LINK_TEXT, "Данные аккаунта").click()

    return driver

def modify_one_of_the_field_in_account(driver, field_id, new_value):
    driver = navigation_to_personal_details(driver)

    # modify field
    field = driver.find_element(By.ID, field_id)
    field.clear()
    field.send_keys(new_value)

    # save modification
    driver.find_element(By.NAME, "save_account_details").click()

    # getting field data and check
    driver.find_element(By.LINK_TEXT, "Данные аккаунта").click()
    updated_field = driver.find_element(By.ID, field_id).get_attribute("value")
    utilities.logout(driver)

    return updated_field


def test_modify_name_in_account(driver):
    new_name = "Faridun"
    updated_name = modify_one_of_the_field_in_account(driver, "account_first_name", new_name)

    assert updated_name == new_name, f"Expected updated name: {new_name}, Actual updated name: {updated_name}"


def test_modify_second_name_in_account(driver):
    new_second_name = "Hushang-Mirzo"
    updated_second_name = modify_one_of_the_field_in_account(driver, "account_last_name", new_second_name)

    assert updated_second_name == new_second_name, f"Expected updated second name: {new_second_name}, Actual updated second name: {updated_second_name}"


def test_modify_showing_name_in_account(driver):
    new_display_name = "Faridun is a Caesar Emperor of Rome"
    updated_display_name = modify_one_of_the_field_in_account(driver, "account_display_name", new_display_name)

    assert updated_display_name == new_display_name, f"Expected updated second name: {new_display_name}, Actual updated second name: {updated_display_name}"


def test_modify_email_in_account(driver):
    new_email = "ValayBalay@mail.ru"
    updated_email = modify_one_of_the_field_in_account(driver, "account_email", new_email)

    assert updated_email == new_email, f"Expected updated second name: {new_email}, Actual updated second name: {updated_email}"


def change_password_fields(driver, current_pass, new_pass, repeat_new_pass):
    utilities.get_element(driver, By.ID, "password_current").send_keys(current_pass)
    utilities.get_element(driver, By.ID, "password_1").send_keys(new_pass)
    utilities.get_element(driver, By.ID, "password_2").send_keys(repeat_new_pass)
    utilities.get_element(driver, By.NAME, "save_account_details").click()

    return driver

# revert old password
def revert_password(driver, current_password):
    driver = utilities.login_with_data(driver, utilities.usernames[1], current_password)

    utilities.get_element(driver, By.LINK_TEXT, "Данные аккаунта").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))
    driver = change_password_fields(driver, current_password, utilities.passwords[1], utilities.passwords[1])

    utilities.get_element(driver, By.CLASS_NAME, "woocommerce-message")
    utilities.logout(driver)


def test_modify_password_in_account(driver):
    new_password = "ValaVala123"
    driver = navigation_to_personal_details(driver)
    driver = change_password_fields(driver, utilities.passwords[1], new_password, new_password)

    success_message = utilities.get_element(driver, By.CLASS_NAME, "woocommerce-message")
    assert success_message.text == "Account details changed successfully.", "Password update failed"

    # cause after update pass, service don't redirect on main page
    utilities.logout(driver)

    # for check, auth with old pass
    utilities.login(driver)

    li_element = utilities.get_element(driver, By.XPATH, "//ul[@role='alert']//li[1]")
    # driver.find_element(By.XPATH, "//ul[@role='alert']//li[1]")

    assert li_element.text == "Веденный пароль для пользователя Ferdinand неверный. Забыли пароль?", "Password update failed"
    revert_password(driver, new_password)


def test_modify_password_without_current_pass(driver):
    driver = navigation_to_personal_details(driver)

    new_password = "ValaVala123"
    driver = change_password_fields(driver, "", new_password, new_password)

    error_message = utilities.get_element(driver, By.XPATH, "//ul[@role='alert']//li[1]")
    assert error_message.text == "Введите пароль.", "Modify password without current password field failed"
    utilities.logout(driver)


def test_mismatched_new_pass_with_repeat_new_pass_fields(driver):
    driver = navigation_to_personal_details(driver)

    new_password = "ValaVala123"
    repeat_new_password = "ValaVala1234"
    driver = change_password_fields(driver, utilities.passwords[1], new_password, repeat_new_password)

    error_message = utilities.get_element(driver, By.XPATH, "//ul[@role='alert']//li[1]")
    assert error_message.text == "Введенные пароли не совпадают.", "Cannot save new password"
    utilities.logout(driver)


def test_logout_by_link_in_account(driver):
    driver = navigation_to_personal_details(driver)
    utilities.get_element(driver, By.XPATH, "(//nav[@class='woocommerce-MyAccount-navigation']//li)[4]/a").click()

    login_link = utilities.get_element(driver, By.LINK_TEXT, "Войти")
    assert login_link.text == "Войти", "Cannot log out"