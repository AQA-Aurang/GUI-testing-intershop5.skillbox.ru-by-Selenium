from time import sleep

import pytest

from pages.product_card_page import ProductPage
from pages.shopping_cart_page import CartPage
from pages.shopping_cart_page import PRODUCT_IMG_LINKS_IN_CART, PRODUCT_LINKS_IN_CART


# @pytest.mark.usefixtures('chrome_browser')
# @pytest.mark.usefixtures('edge_browser')
# @pytest.mark.usefixtures('firefox_browser')
@pytest.mark.usefixtures('browsers')
class TestsShoppingCart:

    # Страница корзины
    @pytest.mark.parametrize("locator", [PRODUCT_IMG_LINKS_IN_CART, PRODUCT_LINKS_IN_CART])
    def test_go_to_product_from_cart(self, cart_page: CartPage, locator: tuple[str, str]):
        """
        :param cart_page: object
        :param locator: give a selector and his value
        """
        product_title: str = cart_page.get_product_text_by(0)
        cart_page.go_to_product(locator)

        product: ProductPage = ProductPage(cart_page.driver, product_title)
        assert product_title.capitalize() in product.get_title(), product.logger.log(30, "Couldn't go to selected product", exc_info=True)

    @pytest.mark.parametrize("direction", ["increase", "decrease"])
    def test_modify_count_of_product_in_cart(self, cart_page: CartPage, direction: str):
        """
        :param cart_page: object
        :param direction: str, can have 2 values - increase/decrease
        """
        quantity: int = cart_page.get_quantity_of_product()
        cart_page.modify_quantity_of_product(quantity, direction)
        updated_notification: str = cart_page.get_updated_notification()
        assert updated_notification == "Cart updated.", cart_page.logger.log(30, "Couldn't update cart", exc_info=True)

    def test_remove_product_added_in_cart(self, cart_page: CartPage):
        """
        :param cart_page: object
        """
        cart_page.remove_product()
        assert cart_page.is_product_deleted(), cart_page.logger.log(30, "Couldn't remove product from cart", exc_info=True)

    def test_recovery_product_after_removing(self, cart_page: CartPage):
        """
        :param cart_page: object
        """
        cart_page.remove_product()

        if cart_page.is_product_deleted():
            cart_page.recovery_product()

            assert cart_page.get_quantity_products_in_cart() > 0, cart_page.logger.log(30, "Couldn't recovery removed product", exc_info=True)
            return

        assert False, cart_page.logger.log(30, "Couldn't recovery removed product", exc_info=True)

    @pytest.mark.parametrize("coupon", ["GIVEMEHALYAVA", "SERT500", "Pedro-pedro pedro Peee"])
    def test_apply_coupon(self, cart_page: CartPage, coupon: str):
        """
        :param cart_page: object
        :param coupon: str
        """
        if cart_page.check_coupon():
            cart_page.remove_coupon()

        cart_page.apply_coupon(coupon)
        message: str = cart_page.get_discount_text_or_error_message()

        if "Неверный купон" in message:
            cart_page.logger.error("Invalid coupon")
            return

        assert coupon in message.upper(), cart_page.logger.log(30, "Couldn't apply coupon", exc_info=True)
        cart_page.remove_coupon()

    @pytest.mark.parametrize("coupon", ["GIVEMEHALYAVA", "SERT500"])
    def test_remove_applied_coupon(self, cart_page: CartPage, coupon: str):
        """
        :param cart_page: object
        :param coupon: str
        """
        cart_page.apply_coupon(coupon)
        message: str = cart_page.get_discount_text_or_error_message()

        if coupon in message:
            cart_page.remove_coupon()

            assert cart_page.is_coupon_removed(), cart_page.logger.log(30, "Couldn't remove coupon", exc_info=True)
