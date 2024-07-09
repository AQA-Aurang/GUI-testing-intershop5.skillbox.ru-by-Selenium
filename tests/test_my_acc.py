from selenium.webdriver.common.by import By
from conftest import chrome_browser as driver, login, logout
from conftest2 import get_webdriver_instance_and_open_account_page as preparation_work
import data.test_data as test_data
import data.locators as locator


# Информация на стр. Мой аккаунт
def test_go_to_my_account_from_link_navbar(preparation_work):
    acc_page = preparation_work
    account = acc_page.get_element(By.LINK_TEXT, locator.my_account_link_in_my_account)
    acc_page.verify_account_title(account, test_data.title_in_account_page)
    acc_page.element_should_have_text(By.CLASS_NAME, locator.title_in_my_account, test_data.main_header_in_account_page,
                                     test_data.assertion_error_in_test_go_to_my_account_from_link_navbar)


def test_go_to_my_account_from_login_link(preparation_work):
    acc_page = preparation_work
    account = acc_page.get_element(By.LINK_TEXT, locator.login_link_in_my_account)
    acc_page.verify_account_title(account, test_data.title_in_account_page)
    acc_page.element_should_have_text(By.CLASS_NAME, locator.title_in_my_account, test_data.main_header_in_account_page,
                                     test_data.assertion_error_in_test_go_to_my_account_from_login_link)


def test_go_to_my_account_from_footer_link(preparation_work):
    acc_page = preparation_work
    acc_page.go_to_bottom()
    account = acc_page.get_element(By.LINK_TEXT, locator.my_account_link_in_my_account)
    acc_page.verify_account_title(account, test_data.title_in_account_page)
    acc_page.element_should_have_text(By.CLASS_NAME, locator.title_in_my_account, test_data.main_header_in_account_page,
                                     test_data.assertion_error_in_test_go_to_my_account_from_footer_link)


# Заказы на стр. Мой аккаунт
def test_go_to_orders_from_info_block_after_auth(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    link_to_orders = acc_page.get_element(By.LINK_TEXT, locator.my_orders_link_in_my_account)
    acc_page.driver = acc_page.verify_account_title(link_to_orders, test_data.title_in_account_page)
    acc_page.element_should_have_text(By.CLASS_NAME, locator.title_in_my_account, test_data.orders_text_for_assertion,
                                     test_data.assertion_error_in_test_go_to_orders_from_info_block_after_auth)
    logout


def test_go_to_orders_after_auth(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    link_to_orders = acc_page.get_element(By.LINK_TEXT, locator.link_to_orders_block_in_my_account)
    acc_page.click_element(link_to_orders)
    acc_page.element_should_have_text(By.CLASS_NAME, locator.title_in_my_account, test_data.orders_text_for_assertion,
                                     test_data.assertion_error_in_test_go_to_orders_after_auth)
    logout


# Страница заказанного товара
def test_go_to_order_details(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    link_to_orders = acc_page.get_element(By.LINK_TEXT, locator.link_to_orders_block_in_my_account)
    acc_page.driver = acc_page.verify_account_title(link_to_orders, test_data.title_in_account_page)
    acc_page.searching_specific_order_or_receiving_text_about_no_orders(By.XPATH, locator.link_to_order_detail_in_order_page)

    logout


# Данные аккаунта на стр. Мой аккаунт
def test_modify_name_field(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    acc_page.modify_one_of_the_field_and_check(locator.name_field_in_personal_block_in_my_account, test_data.name)

    logout


def test_modify_second_name_field(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    acc_page.modify_one_of_the_field_and_check(locator.last_name_field_in_personal_block_in_my_account, test_data.last_name)

    logout


def test_modify_displaying_name_field(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    acc_page.modify_one_of_the_field_and_check(locator.display_name_field_in_personal_block_in_my_account, test_data.display_name)

    logout


def test_modify_email_field(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    acc_page.modify_one_of_the_field_and_check(locator.email_field_in_personal_block_in_my_account, test_data.email)

    logout


def test_modify_password_fields(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    acc_page.driver = acc_page.navigation_to_personal_details()
    acc_page.driver = acc_page.change_password_fields(acc_page.default_password, test_data.new_password, test_data.new_password)
    acc_page.element_should_have_text(By.CLASS_NAME, locator.alert_notification_in_personal_block_in_my_account,
                                     test_data.success_change_personal_data_for_assertion,
                                     test_data.assertion_error_in_test_modify_password_fields)

    # we have to check, need logout and try login with old password
    acc_page.driver = acc_page.logout_and_login()

    acc_page.element_should_have_text(By.XPATH, locator.not_success_alert,
                                     test_data.failure_text_in_change_password_for_assertion,
                                     test_data.assertion_error_in_test_modify_password_fields)
    acc_page.revert_password(test_data.new_password)

    logout


def test_modify_password_without_current_pass(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    acc_page.driver = acc_page.navigation_to_personal_details()
    acc_page.driver = acc_page.change_password_fields("", test_data.new_password, test_data.new_password)
    acc_page.element_should_have_text(By.XPATH, locator.not_success_alert, test_data.alert_text_for_assertion,
                                     test_data.assertion_error_in_test_modify_password_without_current_pass)
    logout


def test_mismatched_new_pass_with_repeat_new_pass_fields(preparation_work, login, logout):
    acc_page = preparation_work
    acc_page.driver = login
    acc_page.driver = acc_page.navigation_to_personal_details()
    acc_page.driver = acc_page.change_password_fields(acc_page.default_password, test_data.new_password, test_data.repeat_new_password)
    acc_page.element_should_have_text(By.XPATH, locator.not_success_alert,
                                     test_data.password_not_match_for_assertion,
                                     test_data.assertion_error_in_test_mismatched_new_pass_with_repeat_new_pass_fields)
    logout


def test_logout_by_link_in_account(preparation_work, login):
    acc_page = preparation_work
    acc_page.driver = login
    acc_page.driver = acc_page.navigation_to_personal_details()
    acc_page.find_and_click_on_element(By.XPATH, locator.logout_link_in_personal_block_in_my_account)
    acc_page.element_should_have_text(By.LINK_TEXT, locator.login_link_in_my_account, test_data.isLogin,
                                     test_data.assertion_error_test_logout_by_link_in_account)
