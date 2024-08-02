import random
import time

import pytest
from selenium.webdriver.common.by import By

from conftest import chrome_browser as driver
from conftest import get_webdriver_instance_and_open_my_account_page as preparation_work_account_page
from conftest import get_webdriver_instance_and_open_catalog_and_sub_catalog_page as preparation_work_catalog_page
from conftest import get_username_password
from pages.product_card_page import get_ordering_product
from pages.product_card_page import get_any_product_from_catalog
from pages.product_card_page import ProductPage
from pages.shopping_cart_page import CartPage
from pages.catalog_and_category_page import CatalogAndCategoryPage


@pytest.mark.parametrize("count_of_products", [0, 11])
@pytest.mark.xfail(reason="If product haven't in a stock then we could get error")
def test_change_count_buying_product(preparation_work_catalog_page, count_of_products):
    driver, product_title = get_any_product_from_catalog(preparation_work_catalog_page, count_of_products)

    if len(product_title) > 0:
        product_page = ProductPage(driver, product_title)

        if product_page.is_quantity_field_available() and product_page.is_available_in_stock():
            product_page.change_count_buying_product(count_of_products)
        else:
            print("Product out of stock or cannot define quantity of products in stock")


def test_add_product_to_cart(preparation_work_catalog_page):
    driver, product_title = get_any_product_from_catalog(preparation_work_catalog_page, 9)
    product = ProductPage(driver, product_title)

    if product.is_available_in_stock():
        product.add_product_to_cart()
        success_message = product.get_text_of_element(product.SUCCESS_MESSAGE_AFTER_ADD_TO_CART)
        success_message = success_message.split("\n")[1]

        assert product_title in success_message, "Couldn't add product to cart"
    else:
        print("Product was finished in stock")


def test_zoom_product_with_magnifying_glass_on_product_card(preparation_work_catalog_page):
    driver, product_title = get_any_product_from_catalog(preparation_work_catalog_page, 10)
    product = ProductPage(driver, product_title)

    if product.is_magnifying_glass_available():
        product.click_to_magnifying_glass()

        img_title = product.get_text_of_element((By.XPATH, "//div[@class='pswp__caption']//div[1]"))
        assert ".jpg" in img_title or\
               ".jpeg" in img_title or\
               ".png" in img_title, "Couldn't open image"


@pytest.mark.parametrize("mark, comment", [(1, "Не советую, мне не понравилось..."),
                                           (2, "Так себе, можно найти и по лучше за такую цену"),
                                           (3, "В целом всё норм, ничего плохого не могу сказать, получил то что заказывал и пожалуй могу посоветовать"),
                                           (4, "Не плохая вешь, мне понравилось, однозначно могу посоветовать, берите"),
                                           (5, "Берите не пожалейте, меня устраивает, уже несколько лет пользуюсь пользуюсь")])
@pytest.mark.xfail(reason="Only in duplicate case")
def test_leave_feedback_for_product(preparation_work_account_page, mark, comment):
    my_account_page = preparation_work_account_page
    username, password = get_username_password()
    product_title = get_ordering_product(my_account_page, username, password, 4)

    product = ProductPage(my_account_page.driver, product_title)
    product.switch_to_feedback_tab()
    if product.is_comment_field_available():
        product.leave_feedback(mark, comment)

        if product.driver.current_url == "https://intershop5.skillbox.ru/wp-comments-post.php":
            product.go_back_when_detect_duplicate_feedback()
            print("Couldn't add feedback cause of duplicate")
            assert False

        assert product.is_exist_feedback(comment), "Couldn't leave feedback"
    else:
        print("Feedback block is unavailable")


# Блок "Категория товаров"
def test_go_to_catalog_sub_catalog_in_side_block_on_product_page(preparation_work_catalog_page):
    driver, product_title = get_any_product_from_catalog(preparation_work_catalog_page, 10)
    product = ProductPage(driver, product_title)

    categories = product.get_categories_from_goods_category_block()
    category_link = product.get_element_from_another_element(categories[0], By.TAG_NAME, "a")
    title_category = category_link.text.capitalize()
    product.click_by(category_link)
    category_page = CatalogAndCategoryPage(product.driver, title_category)

    assert title_category == category_page.get_title(), "Couldn't go to category page"


# Блок "Сопутствующие товары"
def test_go_to_product_from_related_products(preparation_work_catalog_page):
    driver, product_title = get_any_product_from_catalog(preparation_work_catalog_page, 6)
    product = ProductPage(driver, product_title)
    wd, related_product_title = product.go_to_related_product()
    related_product_in_new_page = ProductPage(wd, related_product_title)

    assert related_product_title in related_product_in_new_page.get_title(), "Couldn't go to related product"


def test_add_related_product_to_cart(preparation_work_catalog_page):
    driver, product_title = get_any_product_from_catalog(preparation_work_catalog_page, 6)
    product_page = ProductPage(driver, product_title)
    product_page.driver, related_product_title = product_page.add_related_product_to_cart()
    product_page.go_to_cart_after_add_related_product()
    shopping_cart = CartPage(driver)

    assert related_product_title in shopping_cart.get_product_title_by(related_product_title),\
        "Couldn't add related product in cart"


# Блок "Товары"
@pytest.mark.parametrize("index", [0, 2])
def test_go_to_product_from_products_sidebar_on_product_page(preparation_work_catalog_page, index):
    driver, product_title = get_any_product_from_catalog(preparation_work_catalog_page, 6)
    product_page = ProductPage(driver, product_title)

    products_in_goods_block = product_page.get_all_products_from_goods_block()
    product = products_in_goods_block[index]
    product_title = product.text
    product.click()
    product_card = ProductPage(product_page.driver, product_title)

    assert product_card.get_title() == product_title, "Couldn't find product and go to product page"
