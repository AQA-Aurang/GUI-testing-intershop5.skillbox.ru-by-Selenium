import time

from selenium.webdriver.common.by import By
from conftest import chrome_browser_long_timeout as driver_lt, log_in, log_out
import interhsop5skillbox.data.test_data as test_data
import interhsop5skillbox.data.locators as locator
from conftest2 import get_webdriver_instance_and_open_checkout_page as preparation_work
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from interhsop5skillbox.pages.base_page import get_element_in_another_element


# -------------------------------------------------
# Страница оформления заказа
def test_apply_coupon(preparation_work, log_in, log_out):
    checkout_page = preparation_work
    checkout_page.driver = log_in

    checkout_page.add_item_to_cart_from_related_products_on_product_card()
    checkout_page.find_and_click_on_element(By.LINK_TEXT, locator.order_link)
    checkout_page.find_and_click_on_element(By.LINK_TEXT, locator.link_for_coupon_block_in_order_page)

    try:
        alert_of_apply_coupon = checkout_page.apply_coupon(test_data.promo_code, locator.coupon_success_applied)  # SERT500

        if len(alert_of_apply_coupon) > 0:
            print("\n" + alert_of_apply_coupon)

            # Wait when block overlay finishes his work
            checkout_page.get_element(By.XPATH, locator.overlay_block)

            assert alert_of_apply_coupon == test_data.coupon_success_applied,\
                test_data.assertion_error_cannot_applied_coupon
    except TimeoutException:
        # print("go in timeout exception")
        alert_duplicate_coupon = checkout_page.get_element(By.XPATH, locator.not_success_alert)

        if alert_duplicate_coupon.text == test_data.notification_about_already_applied_coupon:
            checkout_page.removing_applied_coupons

            checkout_page.find_and_click_on_element(By.LINK_TEXT, locator.link_for_coupon_block_in_order_page)

            alert_of_apply_coupon = checkout_page.apply_coupon(test_data.promo_code, locator.coupon_success_applied)  # SERT500
            if len(alert_of_apply_coupon) > 0:
                print("\n" + alert_of_apply_coupon)

                # Wait when block overlay finishes his work
                checkout_page.get_element(By.XPATH, locator.overlay_block)

                assert alert_of_apply_coupon == test_data.coupon_success_applied,\
                    test_data.assertion_error_cannot_applied_coupon
    log_out


def test_remove_added_coupon(preparation_work, log_in, log_out):
    checkout_page = preparation_work
    checkout_page.driver = log_in

    checkout_page.prepare_checkout_page()
    if checkout_page.get_element(By.LINK_TEXT, locator.link_to_remove_coupon):
        checkout_page.driver = checkout_page.remove_added_coupon()

    checkout_page.element_should_have_text(By.XPATH, locator.notification_about_deleted_coupon, test_data.coupon_removed,
                                           test_data.assertion_error_cannot_remove_coupon)
    log_out


def test_place_order_with_empty_mandatory_field(preparation_work, log_in, log_out):
    checkout_page = preparation_work
    checkout_page.driver = log_in

    checkout_page.driver = checkout_page.add_product_to_cart_and_go_to_order_page()
    checkout_page.find_and_clear_field(By.ID, locator.name_field_in_order_page)
    checkout_page.find_and_submit_on_button(By.ID, locator.apply_button_in_order_page)
    checkout_page.element_should_have_text(By.XPATH, locator.notification_element_about_empty_field,
                                           test_data.name_field_notification_for_assertion,
                                           test_data.assertion_error_test_place_order_with_empty_mandatory_field)
    log_out


def test_place_order_with_some_empty_mandatory_fields(preparation_work, log_in, log_out):
    checkout_page = preparation_work
    checkout_page.driver = log_in

    checkout_page.driver = checkout_page.add_product_to_cart_and_go_to_order_page()
    checkout_page.find_and_clear_field(By.ID, locator.name_field_in_order_page)
    checkout_page.find_and_clear_field(By.ID, locator.last_name_field_in_order_page)
    checkout_page.find_and_clear_field(By.ID, locator.city_field_in_order_page)
    checkout_page.find_and_submit_on_button(By.ID, locator.apply_button_in_order_page)
    time.sleep(1)

    main_errs_alerts = checkout_page.get_elements_lt(By.XPATH, locator.few_errors_by_empty_mandatory_fields)
    assert main_errs_alerts[0].text == test_data.name_field_notification_for_assertion \
           and main_errs_alerts[1].text == test_data.last_name_field_notification_for_assertion \
           and main_errs_alerts[2].text == test_data.city_field_notification_for_assertion, \
        test_data.assertion_error_test_place_order_with_some_empty_mandatory_fields
    log_out


# def test_place_order_via_direct_bank_transfer(driver_long_timeout):
#     driver_lt = add_product_to_cart_and_go_to_order_page(driver_long_timeout)
#
#     # li_elements = utilities.get_elements(driver_lt, By.XPATH, "//div[@id='payment']/ul[1]/li")
#     li_elements = utilities.get_elements_experimental(driver_lt, By.XPATH, "//div[@id='payment']/ul[1]/li")
#
#     for li in li_elements:
#         label = utilities.get_element(li, By.TAG_NAME, "label")
#         radio_button = utilities.get_element(li, By.TAG_NAME, "input")
#
#         if label.text == "Прямой банковский перевод" and radio_button.is_selected():
#             break
#         else:
#             utilities.get_element(driver_lt, By.XPATH, "//div[@id='payment']/ul[1]/li[1]/input").click()
#
#     time.sleep(2)
#     utilities.get_element_lt(driver_lt, By.ID, "place_order").click()
#
#     created_order = utilities.get_element(driver_lt, By.XPATH, "//h2[text()='Заказ получен']")
#     assert created_order.text == "Заказ получен", "Couldn't place the order"
#     utilities.logout_experiment(driver_lt)


# def test_place_order_via_payment_on_delivery(driver_long_timeout):
#     driver_lt = add_product_to_cart_and_go_to_order_page(driver_long_timeout)
#
#     # li_elements = utilities.get_elements(driver_lt, By.XPATH, "//div[@id='payment']/ul[1]/li")
#     li_elements = utilities.get_elements_experimental(driver_lt, By.XPATH, "//div[@id='payment']/ul[1]/li")
#
#     for li in li_elements:
#         print("li -", li)
#         label = li.find_element(By.TAG_NAME, "label")
#         # print("label -", label.text)
#         radio_button = li.find_element(By.TAG_NAME, "input")
#         # print("radio_button is selected -", radio_button.is_selected())
#
#         if label.text == "Оплата при доставке" and radio_button.is_selected():
#             break
#         else:
#             utilities.get_element(driver_lt, By.XPATH, "//div[@id='payment']/ul[1]/li[2]/input").submit()
#
#             selected_item = utilities.get_element(driver_lt, By.XPATH, "//div[@id='payment']/ul[1]/li[2]")
#             label = selected_item.find_element(By.TAG_NAME, "label")
#             radio_button = selected_item.find_element(By.TAG_NAME, "input")
#
#             if label.text == "Оплата при доставке" and radio_button.is_selected():
#                 utilities.get_element(driver_lt, By.ID, "place_order").submit()
#
#                 created_order = utilities.get_element(driver_lt, By.XPATH, "//h2[text()='Заказ получен']")
#                 assert created_order.text == "Заказ получен", "Couldn't place the order"
#
#     utilities.logout_experiment(driver)
