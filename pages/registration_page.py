from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    USER_NAME_FIELD: tuple[str, str] = (By.NAME, "username")
    USER_EMAIL_FIELD: tuple[str, str] = (By.NAME, "email")
    PASSWORD_FIELD: tuple[str, str] = (By.NAME, "password")
    REGISTRATION_BUTTON: tuple[str, str] = (By.NAME, "register")
    REGISTRATION_FINISHED: tuple[str, str] = (By.XPATH, "//div[@class='content-page']//div[1]")

    def __init__(self, driver):
        super().__init__(driver)

        if self.driver.title != "Регистрация — Skillbox":
            raise Exception(f"This is not registration page, current page is: {self.driver.title} - {self.driver.current_url}")

    def registration(self, user_name: str, user_email: str, password: str) -> None:
        self.type(self.USER_NAME_FIELD, user_name)
        self.type(self.USER_EMAIL_FIELD, user_email)
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.REGISTRATION_BUTTON)
