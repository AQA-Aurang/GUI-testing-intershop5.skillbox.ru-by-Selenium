import pytest
from faker import Faker


@pytest.mark.xfail(reason="In case when name, email and password have characters less than 20 symbols, but we still get an error")
def test_go_to_register_new_user(browser, registration_page) -> None:
    """
    :param browser: one of 3 type of webdriver - chrome, firefox, edge
    :param registration_page: object
    """
    fake = Faker()

    while True:
        name, email, password = fake.name_male(), fake.email(), fake.password()

        if len(name) > 20 or len(email) > 20 or len(password) > 20:
            continue
        else:
            registration_page.logger.error("Bug - name, email and password have a symbol less than 20 characters")
            registration_page.logger.error(f'name length - {len(name)}, email length - {len(email)} and password length - {len(password)}')
            break

    registration_page.registration(fake.name_male(), fake.email(), fake.password())
    registration_txt: str = registration_page.wait_for_element(registration_page.REGISTRATION_FINISHED).text

    assert registration_txt == "Регистрация завершена", registration_page.logger.error("Registration was not successfully")
