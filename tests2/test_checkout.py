import time

import pytest

from conftest2 import chrome_browser as driver
from conftest2 import get_webdriver_instance_and_open_my_account_page as preparation_work_to_auth
from pages2.checkout_page import authorisation, adding_anyone_product_in_cart_and_go_to_checkout
from pages2.catalog_and_category_page import CatalogAndCategoryPage
from pages2.order_received_page import OrderReceivedPage


# -------------------------------------------------
# Страница оформления заказа
def test_apply_coupon(preparation_work_to_auth):
    account_page = authorisation(preparation_work_to_auth)
    account_page.go_to_catalog_page_from_navbar()

    catalog_and_category_page = CatalogAndCategoryPage(account_page.driver)

    checkout_page = adding_anyone_product_in_cart_and_go_to_checkout(catalog_and_category_page)

    if checkout_page.is_coupon_already_applied():
        checkout_page.removed_applied_coupon()

    checkout_page.apply_coupon("GIVEMEHALYAVA")
    success_message = checkout_page.get_success_message_by_apply_coupon()

    assert success_message == "Купон успешно добавлен.", "Couldn't apply coupon"


def test_remove_added_coupon(preparation_work_to_auth):
    account_page = authorisation(preparation_work_to_auth)
    account_page.go_to_catalog_page_from_navbar()

    catalog_and_category_page = CatalogAndCategoryPage(account_page.driver)

    checkout_page = adding_anyone_product_in_cart_and_go_to_checkout(catalog_and_category_page)

    if checkout_page.is_coupon_already_applied():
        checkout_page.removed_applied_coupon()
    else:
        checkout_page.apply_coupon("GIVEMEHALYAVA")
        _ = checkout_page.get_success_message_by_apply_coupon()
        checkout_page.removed_applied_coupon()

    assert checkout_page.is_coupon_removed(), "Couldn't removed coupon on checkout page"


def test_place_order_with_empty_mandatory_field(preparation_work_to_auth):
    account_page = authorisation(preparation_work_to_auth)
    account_page.go_to_catalog_page_from_navbar()

    catalog_and_category_page = CatalogAndCategoryPage(account_page.driver)

    checkout_page = adding_anyone_product_in_cart_and_go_to_checkout(catalog_and_category_page)
    checkout_page.clear_fields(checkout_page.NAME_FIELD)
    checkout_page.ordering_products()

    assert "обязательное поле" in checkout_page.get_text_of_element(checkout_page.ERROR_ALERT), \
        "Client can manage to place an order with an empty field that was mandatory"

    checkout_page.filling_fields(**{"Faridun": checkout_page.NAME_FIELD})


def test_place_order_with_some_empty_mandatory_fields(preparation_work_to_auth):
    account_page = authorisation(preparation_work_to_auth)
    account_page.go_to_catalog_page_from_navbar()

    catalog_and_category_page = CatalogAndCategoryPage(account_page.driver)

    checkout_page = adding_anyone_product_in_cart_and_go_to_checkout(catalog_and_category_page)
    checkout_page.clear_fields(checkout_page.LAST_NAME_FIELD,
                               checkout_page.ADDRESS_FIELD,
                               checkout_page.CITY_FIELD)
    checkout_page.ordering_products()

    for element in checkout_page.wait_for_elements(checkout_page.ERROR_ALERTS):
        assert "обязательное поле" in element.text

    checkout_page.filling_fields(**{"Hushang-Mirzo": checkout_page.LAST_NAME_FIELD,
                                    "Tashkent, Bobojon Gafurov str.": checkout_page.ADDRESS_FIELD,
                                    "Tashkent": checkout_page.CITY_FIELD})


@pytest.mark.parametrize("payment_method", ["Прямой банковский перевод", "Оплата при доставке"])
def test_place_order_via_direct_bank_transfer(preparation_work_to_auth, payment_method):
    account_page = authorisation(preparation_work_to_auth)
    account_page.go_to_catalog_page_from_navbar()

    catalog_and_category_page = CatalogAndCategoryPage(account_page.driver)

    checkout_page = adding_anyone_product_in_cart_and_go_to_checkout(catalog_and_category_page)

    payment_variants = checkout_page.get_payment_variants()
    checkout_page.scroll_to_element(payment_variants[0])
    for payment_variant in payment_variants:
        title_variant = checkout_page.get_title_by(payment_variant)
        if payment_method == title_variant:
            if not checkout_page.is_selected(payment_variant):
                checkout_page.payment_on_delivery()

        checkout_page.ordering_products()

        order_received_page = OrderReceivedPage(checkout_page.driver)

        assert order_received_page, "Could not ordering product"
        break
