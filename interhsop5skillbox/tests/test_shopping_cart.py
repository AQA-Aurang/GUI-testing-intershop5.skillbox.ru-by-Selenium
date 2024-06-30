import datetime

import interhsop5skillbox.data.locators as locator
import interhsop5skillbox.data.test_data as test_data
from conftest import chrome_browser as driver
from conftest2 import get_webdriver_instance_and_open_cart_page as preparation_work
from interhsop5skillbox.pages.base_page import get_element_in_another_element
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


# -------------------------------------------------
# Страница корзины
def test_go_to_product_from_cart1(preparation_work):
    cart_page = preparation_work

    title_product = cart_page.add_item_to_cart_from_related_products_on_product_card()
    cart_page.find_and_click_on_element(By.XPATH, locator.img_element)
    cart_page.element_should_have_text(By.XPATH, locator.product_title_in_new_page, title_product,
                                       test_data.assertion_error_not_equals_text_with_title_page)


def test_go_to_product_from_cart2(preparation_work):
    cart_page = preparation_work

    title_product = cart_page.add_item_to_cart_from_related_products_on_product_card()
    cart_page.find_and_click_on_element(By.XPATH, f"//td[@data-title='Товар']/a[contains(text(), '{title_product}')]")
    cart_page.element_should_have_text(By.XPATH, locator.product_title_in_new_page, title_product,
                                       test_data.assertion_error_not_equals_text_with_title_page)


def test_modify_count_of_prod_in_cart(preparation_work):
    cart_page = preparation_work

    cart_page.add_item_to_cart_from_related_products_on_product_card()
    cart_page.print_in_field(By.XPATH, locator.count_of_product_on_cart_page, "6")
    cart_page.find_and_click_on_element(By.NAME, locator.apply_coupon_on_cart_page)


def test_remove_product_added_in_cart(preparation_work):
    cart_page = preparation_work

    title_product = cart_page.remove_product_added_in_cart()
    cart_page.expected_text_consist_in_searching_element(By.XPATH, locator.notification_element,
                                        title_product, test_data.assertion_error_in_test_remove_product_added_in_cart)


def test_recovery_product_after_removing(preparation_work):
    cart_page = preparation_work

    removed_product = cart_page.remove_product_added_in_cart()
    cart_page.find_and_click_on_element(By.LINK_TEXT, locator.recovery_product)
    cart_page.element_should_have_text(By.XPATH, f"//td[@data-title='Товар']/a[contains(text(), '{removed_product}')]",
                                       removed_product, test_data.assertion_error_test_recovery_product_after_removing)


def test_apply_promo_code_on_cart_page(preparation_work):
    cart_page = preparation_work

    cart_page.add_item_to_cart_from_related_products_on_product_card()
    alert_of_apply_coupon = cart_page.apply_coupon(test_data.promo_code, locator.notification_element)

    if len(alert_of_apply_coupon) > 0:
        # print("\n" + alert_of_apply_coupon)
        cart_page.get_element_lt(By.XPATH, locator.overlay_block2)
        assert True


def test_apply_certificate_on_cart_page(preparation_work):
    cart_page = preparation_work

    cart_page.add_item_to_cart_from_related_products_on_product_card()
    alert_of_apply_coupon = cart_page.apply_coupon(test_data.certificate, locator.notification_element)

    if len(alert_of_apply_coupon) > 0:
        # print("\n" + alert_of_apply_coupon)
        cart_page.get_element_lt(By.XPATH, locator.overlay_block2)
        assert True


def test_apply_not_exist_coupon_on_cart_page(preparation_work):
    cart_page = preparation_work

    cart_page.add_item_to_cart_from_related_products_on_product_card()
    alert_of_apply_coupon = cart_page.apply_coupon(test_data.not_exist_coupon, locator.not_success_alert)

    assert len(alert_of_apply_coupon) > 0 and alert_of_apply_coupon == test_data.incorrect_coupon, \
        test_data.assertion_error_with_incorrect_coupon


def test_remove_applied_coupon(preparation_work):
    cart_page = preparation_work

    cart_page.add_item_to_cart_from_related_products_on_product_card()

    try:
        cart_page.removing_applied_coupons()
    except TimeoutException:
        cart_page.apply_promo_code()
        cart_page.find_and_click_on_element(By.LINK_TEXT, locator.link_to_remove_coupon)
        cart_page.element_should_have_text(By.XPATH, locator.notification_about_deleted_coupon,
                                       test_data.coupon_removed, test_data.assertion_error_cannot_remove_coupon)
