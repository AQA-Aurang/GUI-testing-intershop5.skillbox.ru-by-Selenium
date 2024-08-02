import time

import pytest

from conftest import chrome_browser as driver
from conftest import get_webdriver_instance_and_open_catalog_and_sub_catalog_page as preparation_work
from pages.shopping_cart_page import adding_anyone_product_in_cart
from pages.product_card_page import ProductPage
from pages.shopping_cart_page import CartPage
from pages.shopping_cart_page import PRODUCT_IMG_LINKS_IN_CART, PRODUCT_LINKS_IN_CART


# Страница корзины
@pytest.mark.parametrize("locator", [PRODUCT_IMG_LINKS_IN_CART, PRODUCT_LINKS_IN_CART])
def test_go_to_product_from_cart(preparation_work, locator):
    driver = adding_anyone_product_in_cart(preparation_work)

    cart_page = CartPage(driver)
    product_title = cart_page.get_product_text_by(0)
    cart_page.go_to_product(locator)

    product = ProductPage(cart_page.driver, product_title)
    product_title = product_title.capitalize()
    assert product_title == product.get_title(), "Couldn't go to selected product"


@pytest.mark.parametrize("direction", ["increase", "decrease"])
def test_modify_count_of_product_in_cart(preparation_work, direction):
    driver = adding_anyone_product_in_cart(preparation_work)

    cart_page = CartPage(driver)
    quantity = cart_page.get_quantity_of_product()
    cart_page.modify_quantity_of_product(quantity, direction)
    updated_notification = cart_page.get_updated_notification()
    assert updated_notification == "Cart updated.", "Couldn't update cart"


def test_remove_product_added_in_cart(preparation_work):
    driver = adding_anyone_product_in_cart(preparation_work)

    cart_page = CartPage(driver)
    cart_page.remove_product()
    assert cart_page.is_cart_empty(), "Couldn't remove product from cart"


def test_recovery_product_after_removing(preparation_work):
    driver = adding_anyone_product_in_cart(preparation_work)

    cart_page = CartPage(driver)
    cart_page.remove_product()

    if cart_page.is_cart_empty():
        cart_page.recovery_product()

        assert cart_page.get_quantity_products_in_cart() > 0, "Couldn't recovery removed product"
        return

    assert False, "Couldn't recovery removed product"


@pytest.mark.parametrize("coupon", ["GIVEMEHALYAVA", "SERT500", "Pedro-pedro pedro Peee"])
def test_apply_coupon(preparation_work, coupon):
    driver = adding_anyone_product_in_cart(preparation_work)

    cart_page = CartPage(driver)
    cart_page.apply_coupon(coupon)
    message = cart_page.get_discount_text_or_error_message()

    if "Неверный купон" in message:
        assert True
        return

    assert coupon in message.upper(), "Couldn't apply coupon"


def test_remove_applied_coupon(preparation_work):
    driver = adding_anyone_product_in_cart(preparation_work)

    cart_page = CartPage(driver)
    cart_page.apply_coupon("GIVEMEHALYAVA")
    message = cart_page.get_discount_text_or_error_message()

    if "GIVEMEHALYAVA" in message:
        cart_page.remove_coupon()

        assert cart_page.is_coupon_removed(), "Couldn't remove coupon"
