import random

import pytest
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.my_account_page import MyAccountPage
from pages.catalog_and_category_page import CatalogAndCategoryPage
from pages.product_card_page import ProductPage
from pages.product_card_page import get_any_product_from_catalog, get_ordering_product
from pages.shopping_cart_page import CartPage


@pytest.mark.usefixtures('browsers')
class TestsProductCard:

    @pytest.mark.parametrize("count_of_products", [0, 11])
    def test_change_count_buying_product(self, catalog_and_sub_catalog_page: CatalogAndCategoryPage, count_of_products: int):
        driver, product_title = get_any_product_from_catalog(catalog_and_sub_catalog_page, count_of_products)

        if len(product_title) > 0:
            product_page: ProductPage = ProductPage(driver, product_title)

            if product_page.is_quantity_field_available() and product_page.is_available_in_stock():
                product_page.change_count_buying_product(count_of_products)
            else:
                product_page.logger.error("Product out of stock or cannot define quantity of products in stock")

    def test_add_product_to_cart(self, product_page: ProductPage):
        product, product_title = product_page

        if product.is_available_in_stock():
            product.add_product_to_cart()
            success_message: str = product.get_text_of_element(product.SUCCESS_MESSAGE_AFTER_ADD_TO_CART)
            success_message: str = success_message.split("\n")[1]

            assert product_title in success_message, product_page.logger.error("Couldn't add product to cart")
        else:
            product_page.logger.error("Product was finished in stock")

    def test_zoom_product_with_magnifying_glass_on_product_card(self, product_page: ProductPage):
        product, product_title = product_page

        if product.is_magnifying_glass_available():
            product.click_to_magnifying_glass()

            img_title: str = product.get_text_of_element((By.XPATH, "//div[@class='pswp__caption']//div[1]"))
            assert ".jpg" in img_title or \
                   ".jpeg" in img_title or \
                   ".png" in img_title, product.logger.error("Couldn't open image")

    @pytest.mark.parametrize("mark, comment", [
        (1, "Не советую, мне не понравилось"),
        (2, "Так себе, можно найти и по лучше за такую цену"),
        (3, "В целом всё норм, ничего плохого не могу сказать, получил то что заказывал и пожалуй могу посоветовать"),
        (4, "Не плохая вешь, мне понравилось, однозначно могу посоветовать, берите"),
        (5, "Берите не пожалейте, меня устраивает, уже несколько лет пользуюсь пользуюсь")
    ])
    @pytest.mark.xfail
    def test_leave_feedback_for_product(self, account_page_with_auth: MyAccountPage, mark: int, comment: str):
        product_title: str = get_ordering_product(account_page_with_auth, '', '', random.randint(0, 9))
        product: ProductPage = ProductPage(account_page_with_auth.driver, product_title)
        product.switch_to_feedback_tab()

        if product.is_comment_field_available():
            if product.is_exist_feedback(comment):
                while True:
                    fake_ru = Faker('ru-RU')
                    comment = fake_ru.sentence(random.randint(1, 100))

                    if not product.is_exist_feedback(comment):
                        break

            product.leave_feedback(mark, comment)

            if product.driver.current_url == product.BASE_URL + "wp-comments-post.php":
                product.go_back_in_detect_duplicate_feedback()
                # print("Couldn't add feedback cause of duplicate")
                product.logger.error("Couldn't add feedback cause of duplicate'", exc_info=True)

            assert product.is_exist_feedback(comment), product.logger.error(f"Comment is not equal - {comment}")
        else:
            product.logger.error("Feedback block is unavailable")

        product.logout_by_link()

    # Блок "Категория товаров"
    def test_go_to_catalog_or_sub_catalog_in_side_block_on_product_page(self, product_page: ProductPage):
        product, product_title = product_page

        categories: list[WebElement] = product.get_categories_from_goods_category_block()
        category_link: WebElement = product.get_element_from_another_element(categories[0], By.TAG_NAME, "a")
        title_category: str = category_link.text.capitalize()
        product.click_by(category_link)
        category_page: CatalogAndCategoryPage = CatalogAndCategoryPage(product.driver, title_category)

        assert title_category == category_page.get_title(), category_page.logger.error("Couldn't go to category page")

    # Блок "Сопутствующие товары"
    def test_go_to_product_from_related_products(self, product_page: ProductPage):
        product, product_title = product_page
        wd, related_product_title = product.go_to_related_product()
        related_product_in_new_page: ProductPage = ProductPage(wd, related_product_title)

        assert related_product_title.capitalize() in related_product_in_new_page.get_title(), \
            related_product_in_new_page.logger.error("Couldn't go to related product")

    def test_add_related_product_to_cart(self, catalog_and_sub_catalog_page: CatalogAndCategoryPage):
        driver, product_title = get_any_product_from_catalog(catalog_and_sub_catalog_page, 6)
        product_page: ProductPage = ProductPage(driver, product_title)

        product_page.driver, related_product_title = product_page.add_related_product_to_cart()
        product_page.go_to_cart_after_add_related_product()
        shopping_cart: CartPage = CartPage(driver)

        assert related_product_title in shopping_cart.get_product_title_by(related_product_title), \
            shopping_cart.logger.error("Couldn't add related product in cart")

    # Блок "Товары"
    @pytest.mark.parametrize("index", [0, 2])
    @pytest.mark.xfail(reason="every day someone adding some products and that product in product page can having crazy, not equal title")
    def test_go_to_product_from_products_sidebar_on_product_page(self, product_page: ProductPage, index: int):
        product_p, product_title = product_page
        products_in_goods_block: list[WebElement] = product_p.get_all_products_from_goods_block()
        product: WebElement = products_in_goods_block[index]
        product_title: str = product.text
        product.click()
        product_card: ProductPage = ProductPage(product_p.driver, product_title)

        assert product_card.get_title() == product_title.capitalize(), product_card.logger.error("Couldn't find product and go to product page")
