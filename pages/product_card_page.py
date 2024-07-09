import random
from .base_types import BaseType
from .base_page import BasePage


class ProductCardPage(BasePage):
    def __init__(self, driver: BaseType):
        super().__init__(driver)

    def element_should_have_text(self, type_of_locator, locator, text, err_description):
        element, title_of_element = self.get_element_and_text(type_of_locator, locator)

        if "‘" in title_of_element and "’" in title_of_element:
            title_of_element = element.text.replace("‘", "'").replace("’", "'")

        assert title_of_element == text, err_description

    def write_review_for_product(self, review_field, old_review):
        review_txt = ""

        match random.randint(0, 4):
            case 0:
                review_txt = "Не советую, мне не понравилось"
            case 1:
                review_txt = "Так себе, можно найти по лучше за такую цену"
            case 2:
                review_txt = "В целом всё норм, ничего плохого не могу сказать, получил то что заказывал"
            case 3:
                review_txt = "Не плохая вешь, мне понравилось, однозначно могу посоветовать"
            case 4:
                review_txt = "Берите не пожалейте, меня устраивает, уже который год пользуюсь"

        if review_txt == old_review:
            self.write_review_for_product(review_field, old_review)

        return review_txt
