from conftest import chrome_browser as driver
from conftest import get_webdriver_instance_and_open_registration_page as preparation_work


def test_go_to_register_new_user(preparation_work):
    register_page = preparation_work
    register_page.registration("Fredie", "FredieKrug@Bkii.tj", "secret_password123")
    registration_txt = register_page.wait_for_element(register_page.REGISTRATION_FINISHED).text

    assert registration_txt == "Регистрация завершена", "Registration was not successfully"
