import pytest

from pages.product_card_page import ProductPage
from pages.shopping_cart_page import CartPage
from pages.shopping_cart_page import PRODUCT_IMG_LINKS_IN_CART, PRODUCT_LINKS_IN_CART


@pytest.mark.usefixtures('chrome_browser')
class TestsShoppingCart:

    # Страница корзины
    @pytest.mark.parametrize("locator", [PRODUCT_IMG_LINKS_IN_CART, PRODUCT_LINKS_IN_CART])
    def test_go_to_product_from_cart(self, cart_page: CartPage, locator: tuple[str, str]):
        product_title: str = cart_page.get_product_text_by(0)
        cart_page.go_to_product(locator)

        product: ProductPage = ProductPage(cart_page.driver, product_title)
        product_title: str = product_title.capitalize()
        assert product_title == product.get_title(), "Couldn't go to selected product"

    @pytest.mark.parametrize("direction", ["increase", "decrease"])
    def test_modify_count_of_product_in_cart(self, cart_page: CartPage, direction: str):
        quantity: int = cart_page.get_quantity_of_product()
        cart_page.modify_quantity_of_product(quantity, direction)
        updated_notification: str = cart_page.get_updated_notification()
        assert updated_notification == "Cart updated.", "Couldn't update cart"

    def test_remove_product_added_in_cart(self, cart_page: CartPage):
        cart_page.remove_product()
        assert cart_page.is_cart_empty(), "Couldn't remove product from cart"

    def test_recovery_product_after_removing(self, cart_page: CartPage):
        cart_page.remove_product()

        if cart_page.is_cart_empty():
            cart_page.recovery_product()

            assert cart_page.get_quantity_products_in_cart() > 0, "Couldn't recovery removed product"
            return

        assert False, "Couldn't recovery removed product"

    @pytest.mark.parametrize("coupon", ["GIVEMEHALYAVA", "SERT500", "Pedro-pedro pedro Peee"])
    def test_apply_coupon(self, cart_page: CartPage, coupon: str):
        if cart_page.check_coupon():
            cart_page.remove_coupon()

        cart_page.apply_coupon(coupon)
        message: str = cart_page.get_discount_text_or_error_message()

        if "Неверный купон" in message:
            cart_page.logger.error("Invalid coupon")
            return

        assert coupon in message.upper(), "Couldn't apply coupon"
        cart_page.remove_coupon()

    @pytest.mark.parametrize("coupon", ["GIVEMEHALYAVA", "SERT500"])
    def test_remove_applied_coupon(self, cart_page: CartPage, coupon: str):
        cart_page.apply_coupon(coupon)
        message: str = cart_page.get_discount_text_or_error_message()

        if coupon in message:
            cart_page.remove_coupon()

            assert cart_page.is_coupon_removed(), "Couldn't remove coupon"
