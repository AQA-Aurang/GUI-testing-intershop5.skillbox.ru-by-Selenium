from faker import Faker


def test_go_to_register_new_user(browser, registration_page) -> None:
    fake = Faker()

    while True:
        name, email, password = fake.name_male(), fake.email(), fake.password()

        if len(name) > 20 or len(email) > 20 or len(password) > 20:
            continue
        else:
            break

    registration_page.registration(fake.name_male(), fake.email(), fake.password())
    registration_txt: str = registration_page.wait_for_element(registration_page.REGISTRATION_FINISHED).text

    assert registration_txt == "Регистрация завершена", registration_page.logger.error("Registration was not successfully")
