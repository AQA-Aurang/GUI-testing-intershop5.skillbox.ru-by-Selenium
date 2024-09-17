import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.order_detail_page import OrderDetailPage
from pages.order_page import OrderPage
from pages.account_edit_data_page import NAME_FIELD, SECOND_NAME_FIELD, DISPLAY_FIELD, EMAIL_FIELD, AccountEditDataPage
from pages.base_page import LOGIN_LINK_IN_HEADER, LINK_TO_MY_ACCOUNT_PAGE_FROM_NAVBAR, \
    LINK_TO_MY_ACCOUNT_PAGE_FROM_FOOTER
from pages.my_account_page import MyAccountPage
from pages.main_page import MainPage


# @pytest.mark.usefixtures('chrome_browser')
# @pytest.mark.usefixtures('edge_browser')
# @pytest.mark.usefixtures('firefox_browser')
@pytest.mark.usefixtures('browsers')
class TestsMyAccountPage:

    # Информация на стр. Мой аккаунт
    @pytest.mark.parametrize('link_to_my_acc_page', [LOGIN_LINK_IN_HEADER, LINK_TO_MY_ACCOUNT_PAGE_FROM_NAVBAR,
                                                     LINK_TO_MY_ACCOUNT_PAGE_FROM_FOOTER])
    def test_go_to_my_account(self, main_page: MainPage, link_to_my_acc_page: tuple[str, str]):
        """
        :param main_page: object
        :param link_to_my_acc_page: locator, give a selector and his value
        """
        main_page.click(link_to_my_acc_page)
        my_account_page: MyAccountPage = MyAccountPage(main_page.driver)

        assert my_account_page.get_title() == "Мой аккаунт — skillbox", my_account_page.logger.log(30, "Cannot go to my account page")

    # Заказы на стр. Мой аккаунт
    def test_go_to_orders_from_info_block(self, account_page_with_auth_and_logout: MyAccountPage):
        """
        :param account_page_with_auth_and_logout: object
        """
        my_orders: OrderPage = account_page_with_auth_and_logout.go_to_orders_from_info_block()

        assert my_orders.get_title() == "Заказы", my_orders.logger.error("Cannot go to orders page")

    def test_go_to_orders_from_order_block(self, account_page_with_auth_and_logout: MyAccountPage):
        """
        :param account_page_with_auth_and_logout: object
        """
        my_orders: OrderPage = account_page_with_auth_and_logout.go_to_order_block()

        assert my_orders.get_title() == "Заказы", my_orders.logger.error("Cannot go to orders page")

    # Страница заказанного товара
    def test_go_to_order_details(self, account_page_with_auth_and_logout: MyAccountPage):
        """
        :param account_page_with_auth_and_logout: object
        """
        order_page: OrderPage = account_page_with_auth_and_logout.go_to_order_block()
        orders:  list[WebElement] = order_page.get_orders()
        title, link = order_page.get_title_and_link(orders[0])
        order_detail_page: OrderDetailPage = order_page.go_to_order_detail_page_after_click_to(link)

        assert title in order_detail_page.get_title(), order_detail_page.logger.error("Cannot go to order detail page")

    # Данные аккаунта на стр. Мой аккаунт
    @pytest.mark.parametrize('locator, test_data', [(NAME_FIELD, "Faridun"), (SECOND_NAME_FIELD, "Hushang-Mirzo"),
                                                    (DISPLAY_FIELD, "Faridun the King of Vyzanty"),
                                                    (EMAIL_FIELD, "ValayBalay@mail.ru")])
    def test_modify_field(self, account_page_with_auth_and_logout: MyAccountPage, locator: tuple[str, str], test_data: str):
        """
        :param account_page_with_auth_and_logout: object
        :param locator: give a selector and his value
        :param test_data: str
        """
        account_edit_data_page: AccountEditDataPage = account_page_with_auth_and_logout.go_to_account_data_block()
        account_edit_data_page.modify_field(locator, test_data)
        my_account_page: MyAccountPage = MyAccountPage(account_edit_data_page.driver)

        success_message: str = my_account_page.get_success_notif_after_update_data()
        assert success_message == "Account details changed successfully.", my_account_page.logger.error("Cannot edit account data")

    def test_modify_password_fields(self, account_page_with_auth_and_logout: MyAccountPage):
        """
        :param account_page_with_auth_and_logout: object
        """
        account_edit_data_page: AccountEditDataPage = account_page_with_auth_and_logout.go_to_account_data_block()
        account_edit_data_page.change_password("ValaVala123'", "ValaVala123", "ValaVala123")
        my_account_page: MyAccountPage = MyAccountPage(account_edit_data_page.driver)

        success_message: str = my_account_page.get_success_notif_after_update_data()
        assert success_message == "Account details changed successfully.", my_account_page.logger.error("Cannot edit account password")

        account_edit_data_page: AccountEditDataPage = my_account_page.go_to_account_data_block()
        account_edit_data_page.change_password("ValaVala123", "ValaVala123'", "ValaVala123'")

    @pytest.mark.parametrize("current_password, new_password, repeat_new_password, expected", [
        ("", "ValaVala123", "ValaVala123", "Введите пароль."),
        ("ValaVala123'", "ValaVala123", "ValaVala1234", "Введенные пароли не совпадают.")])
    def test_modify_password(self, account_page_with_auth_and_logout: MyAccountPage, current_password: str, new_password: str, repeat_new_password: str, expected: str):
        """
        :param account_page_with_auth_and_logout: object
        :param current_password: str
        :param new_password: str
        :param repeat_new_password: str
        :param expected: str, expected result
        """
        account_edit_data_page: AccountEditDataPage = account_page_with_auth_and_logout.go_to_account_data_block()
        account_edit_data_page.change_password(current_password, new_password, repeat_new_password)

        error_message: str = account_page_with_auth_and_logout.get_error_notif_after_update_data()
        assert error_message == expected, account_page_with_auth_and_logout.logger.error("Cannot edit account password")

    def test_logout_by_link_in_account(self, account_page_with_auth: MyAccountPage):
        """
        :param account_page_with_auth: object
        """
        account_page_with_auth.logout_from_logout_block()
        login_button: str = account_page_with_auth.get_text_of_element((By.NAME, "login")).capitalize()

        assert login_button == "Войти", account_page_with_auth.logger.error("Cannot logout from logout block")
