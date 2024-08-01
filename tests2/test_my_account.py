import pytest
from selenium.webdriver.common.by import By
from conftest2 import chrome_browser as driver
from conftest2 import get_webdriver_instance_and_open_main_page as preparation_work_for_main_page
from conftest2 import get_webdriver_instance_and_open_my_account_page as preparation_work
from conftest2 import get_username_password
from pages2.base_page import LOGIN_LINK_IN_HEADER, LINK_TO_MY_ACCOUNT_PAGE_FROM_NAVBAR, \
    LINK_TO_MY_ACCOUNT_PAGE_FROM_FOOTER
from pages2.my_account_page import MyAccountPage
from pages2.account_edit_data_page import NAME_FIELD, SECOND_NAME_FIELD, DISPLAY_FIELD, EMAIL_FIELD


# Информация на стр. Мой аккаунт
@pytest.mark.parametrize('link_to_my_acc_page', [LOGIN_LINK_IN_HEADER, LINK_TO_MY_ACCOUNT_PAGE_FROM_NAVBAR,
                                                 LINK_TO_MY_ACCOUNT_PAGE_FROM_FOOTER])
def test_go_to_my_account(preparation_work_for_main_page, link_to_my_acc_page):
    main_page = preparation_work_for_main_page
    main_page.click(link_to_my_acc_page)
    my_account_page = MyAccountPage(main_page.driver)

    assert my_account_page.get_title() == "Мой аккаунт — Skillbox", "Cannot go to my account page"


# Заказы на стр. Мой аккаунт
def test_go_to_orders_from_info_block(preparation_work):
    my_account_page = preparation_work
    username, password = get_username_password()
    my_account_page.authorisation(username, password)
    my_orders = my_account_page.go_to_my_orders_from_info_block()

    assert my_orders.get_title() == "Заказы", "Cannot go to orders page"


def test_go_to_orders_from_order_block(preparation_work):
    my_account_page = preparation_work
    username, password = get_username_password()
    my_account_page.authorisation(username, password)
    my_orders = my_account_page.go_to_order_block()

    assert my_orders.get_title() == "Заказы", "Cannot go to orders page"


# Страница заказанного товара
def test_go_to_order_details(preparation_work):
    my_account_page = preparation_work
    username, password = get_username_password()
    my_account_page.authorisation(username, password)

    order_page = my_account_page.go_to_order_block()
    orders = order_page.get_orders()
    title, link = order_page.get_title_and_link(orders[0])
    order_detail_page = order_page.click_by_this(link)

    assert title in order_detail_page.get_title(), "Cannot go to order detail page"


# Данные аккаунта на стр. Мой аккаунт
@pytest.mark.parametrize('locator, test_data', [(NAME_FIELD, "Faridun"), (SECOND_NAME_FIELD, "Hushang-Mirzo"),
                                                (DISPLAY_FIELD, "Faridun the King of Vyzanty"),
                                                (EMAIL_FIELD, "ValayBalay@mail.ru")])
def test_modify_field(preparation_work, locator, test_data):
    my_account_page = preparation_work
    username, password = get_username_password()
    my_account_page.authorisation(username, password)

    account_edit_data_page = my_account_page.go_to_account_data_block()
    account_edit_data_page.modify_field(locator, test_data)
    my_account_page = MyAccountPage(account_edit_data_page.driver)

    success_message = my_account_page.get_text_after_action()
    assert success_message == "Account details changed successfully.", "Cannot edit account data"


def test_modify_password_fields(preparation_work):
    my_account_page = preparation_work
    username, password = get_username_password()
    my_account_page.authorisation(username, password)

    account_edit_data_page = my_account_page.go_to_account_data_block()
    account_edit_data_page.change_password("ValaVala123'", "ValaVala123", "ValaVala123")
    my_account_page = MyAccountPage(account_edit_data_page.driver)

    success_message = my_account_page.get_text_after_action()
    assert success_message == "Account details changed successfully.", "Cannot edit account password"

    account_edit_data_page = my_account_page.go_to_account_data_block()
    account_edit_data_page.change_password("ValaVala123", "ValaVala123'", "ValaVala123'")


@pytest.mark.parametrize("current_password, new_password, repeat_new_password, expected", [("", "ValaVala123", "ValaVala123", "Введите пароль."),
                                    ("ValaVala123'", "ValaVala123", "ValaVala1234", "Введенные пароли не совпадают.")])
def test_modify_password(preparation_work, current_password, new_password, repeat_new_password, expected):
    my_account_page = preparation_work
    username, password = get_username_password()
    my_account_page.authorisation(username, password)

    account_edit_data_page = my_account_page.go_to_account_data_block()
    account_edit_data_page.change_password(current_password, new_password, repeat_new_password)

    error_message = my_account_page.get_error_notification()
    assert error_message == expected, "Cannot edit account password"


def test_logout_by_link_in_account(preparation_work):
    my_account_page = preparation_work
    username, password = get_username_password()
    my_account_page.authorisation(username, password)
    my_account_page.logout_from_logout_block()
    login_button = my_account_page.get_text_of_element((By.NAME, "login")).capitalize()

    assert login_button == "Войти", "Cannot logout from logout block"
