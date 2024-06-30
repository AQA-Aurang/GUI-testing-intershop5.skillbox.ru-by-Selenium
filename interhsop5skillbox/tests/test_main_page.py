import time

from selenium.webdriver.common.by import By
from conftest import chrome_browser as driver
import interhsop5skillbox.data.test_data as test_data
import interhsop5skillbox.data.locators as locator
from conftest2 import get_webdriver_instance_and_open_main_page as preparation_work
from interhsop5skillbox.pages.base_page import get_element_in_another_element


def test_go_to_sub_catalog_from_main_page(preparation_work):
    main_page = preparation_work

    main_page.go_to_sub_catalog_from_main_page(locator.first_sub_catalog, test_data.first_sub_catalog_title)

    main_page.driver.back()
    main_page.go_to_sub_catalog_from_main_page(locator.second_sub_catalog, test_data.second_sub_catalog_title)

    main_page.driver.back()
    main_page.go_to_sub_catalog_from_main_page(locator.third_sub_catalog, "", test_data.another_sub_catalog_title)


def test_go_to_product_card_from_sale_block(preparation_work):
    main_page = preparation_work

    main_page.move_down_in_altitude_by(0.95)
    product = main_page.get_element(By.XPATH, locator.product_in_sale_part)
    product_title = get_element_in_another_element(product, By.TAG_NAME, locator.tag_a).get_attribute("title")
    main_page.find_and_click_on_element(By.XPATH, f"{locator.product_in_sale_part}/div/a[@title='{product_title}']")
    main_page.element_should_have_text(By.XPATH, locator.sub_catalog_in_product_page,
                                       test_data.sub_catalog_in_product_page,
                                       test_data.assertion_error_in_finding_product_in_product_page)


def test_go_to_product_card_from_new_arrivals_block(preparation_work):
    main_page = preparation_work

    main_page.move_down_in_altitude_by(2.7)
    product = main_page.get_element(By.XPATH, locator.product_in_arrival_part)
    product_title = get_element_in_another_element(product, By.TAG_NAME, locator.tag_a).get_attribute("title")
    main_page.find_and_click_on_element(By.XPATH, f"{locator.product_in_arrival_part}/div/a[@title='{product_title}']")
    main_page.element_should_have_text(By.XPATH, locator.sub_catalog_in_product_page,
                                       test_data.sub_catalog_in_product_page,
                                       test_data.assertion_error_in_finding_product_in_product_page)


def test_go_to_product_card_from_viewed_products(preparation_work):
    main_page = preparation_work

    main_page.move_down_in_altitude_by(0.95)
    product = main_page.get_element(By.XPATH, locator.product_in_sale_part)
    product_title = get_element_in_another_element(product, By.TAG_NAME, locator.tag_a).get_attribute("title")
    main_page.find_and_click_on_element(By.XPATH, f"{locator.product_in_sale_part}/div/a[@title='{product_title}']")

    actual_result = main_page.get_element(By.XPATH, locator.sub_catalog_in_product_page)
    if actual_result.text == test_data.sub_catalog_in_product_page:
        main_page.find_and_click_on_element(By.LINK_TEXT, locator.link_in_navbar_to_main_page)
        main_page.move_down_in_altitude_by(5.5)

        try:
            viewed_products_block = main_page.get_element(By.ID, locator.viewed_products_block)
            header_viewed_products = get_element_in_another_element(viewed_products_block, By.TAG_NAME, "h2")
            viewed_product = get_element_in_another_element(viewed_products_block, By.TAG_NAME, "li")

            if header_viewed_products.text == test_data.viewed_products.upper():
                viewed_product_title = get_element_in_another_element(viewed_product, By.TAG_NAME, "span").text
                viewed_product_title = viewed_product_title.replace("'", "’")

                if viewed_product_title == product_title:
                    element = get_element_in_another_element(viewed_product, By.TAG_NAME, "a")
                    main_page.click_element(element)
                    main_page.element_should_have_text(By.XPATH, locator.sub_catalog_in_product_page,
                                            test_data.sub_catalog_in_product_page,
                                            test_data.assertion_error_in_test_go_to_product_card_from_viewed_products)
        except Exception as e:
            print("Something went wrong -", e.args)
