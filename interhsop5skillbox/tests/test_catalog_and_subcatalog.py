import random

import interhsop5skillbox.data.test_data as test_data
import interhsop5skillbox.data.locators as locator
from selenium.webdriver.common.by import By
from conftest import chrome_browser as driver
from conftest2 import get_webdriver_instance_and_open_catalog_and_subcatalog_page as preparation_work
from selenium.common.exceptions import TimeoutException
from interhsop5skillbox.pages.base_page import get_element_in_another_element


# Страница каталога товаров
def test_go_to_catalog_of_products(preparation_work):
    catalog_and_subcatalog_page = preparation_work

    catalog, catalog_title = catalog_and_subcatalog_page.get_element_and_text(By.LINK_TEXT, locator.catalog_link)
    catalog_and_subcatalog_page.click_element(catalog)
    catalog_and_subcatalog_page.element_should_have_text(By.XPATH, locator.title_of_catalog_page, catalog_title,
                                                         test_data.assertion_error_test_go_to_catalog_of_products)


# Страница подкатологов товаров
def test_go_to_sub_catalog_from_navbar(preparation_work):
    catalog_and_subcatalog_page = preparation_work

    dropdown_element = catalog_and_subcatalog_page.get_element(By.XPATH, locator.dropdown_element_in_navbar)
    catalog_and_subcatalog_page.driver = catalog_and_subcatalog_page.point_move_and_click_on_element(dropdown_element)
    catalog_and_subcatalog_page.element_should_have_text(By.XPATH, locator.title_household_appliances,
                                                         test_data.household_appliances,
                                                         test_data.assertion_error_test_go_to_sub_catalog_from_navbar)


# Компонент сортировки товаров
def test_select_another_variant_from_product_sorting(preparation_work):
    catalog_and_subcatalog_page = preparation_work
    catalog_and_subcatalog_page.go_to_catalog_of_product()

    sorting_element = catalog_and_subcatalog_page.get_element(By.NAME, locator.sorting_element)
    catalog_and_subcatalog_page.driver = catalog_and_subcatalog_page.point_and_click(sorting_element)
    selected_item, selected_item_title = catalog_and_subcatalog_page.get_element_and_text(By.XPATH,
                                                                                        locator.value_attribute_of_tag)
    catalog_and_subcatalog_page.click_element(selected_item)
    catalog_and_subcatalog_page.get_selected_item_and_assert(selected_item_title,
                                            test_data.assertion_error_test_select_another_variant_from_product_sorting)


# Компонент фильтра цен
def test_change_left_of_slider(preparation_work):
    catalog_and_subcatalog_page = preparation_work
    catalog_and_subcatalog_page.go_to_catalog_of_product()

    catalog_and_subcatalog_page.change_slider(1.25, 10, locator.left_slider, test_data.assertion_error_in_change_slider)
    catalog_and_subcatalog_page.change_slider(1.25, 15, locator.left_slider, test_data.assertion_error_in_change_slider)


def test_change_right_of_slider(preparation_work):
    catalog_and_subcatalog_page = preparation_work
    catalog_and_subcatalog_page.go_to_catalog_of_product()

    catalog_and_subcatalog_page.change_slider(1.25, 10, locator.right_slider, test_data.assertion_error_in_change_slider)
    catalog_and_subcatalog_page.change_slider(1.25, 15, locator.right_slider, test_data.assertion_error_in_change_slider)


def test_move_both_sliders_in_price_filter(preparation_work):
    catalog_and_subcatalog_page = preparation_work
    catalog_and_subcatalog_page.go_to_catalog_of_product()

    catalog_and_subcatalog_page.move_down_in_altitude_by(1.5)
    catalog_and_subcatalog_page.driver, fixed_price1 = catalog_and_subcatalog_page.get_price(locator.slider_xpath1,
                                                                                             locator.price_xpath1, 15)
    catalog_and_subcatalog_page.driver, fixed_price2 = catalog_and_subcatalog_page.get_price(locator.slider_xpath2,
                                                                                             locator.price_xpath2, -25)
    catalog_and_subcatalog_page.find_and_click_on_element(By.XPATH, locator.apply_for_sliders)

    try:
        products = catalog_and_subcatalog_page.get_elements(By.XPATH, locator.products_after_sliders_apply)
        for product in products:
            product_price = get_element_in_another_element(product, By.XPATH, locator.product_price)
            price_text = product_price.text.replace(",", ".")
            price = float(price_text[:-1])

            assert fixed_price1 <= price <= fixed_price2, \
                test_data.assertion_error_in_test_move_both_sliders_in_price_filter1
    except TimeoutException:
        notification = catalog_and_subcatalog_page.get_element(By.XPATH, locator.notification_in_absent_products)
        assert notification.text == test_data.notification_absent_txt_for_assertion, \
            test_data.assertion_error_in_test_move_both_sliders_in_price_filter2


# Компонент пагинации страниц
def test_pagination_in_catalog(preparation_work):
    catalog_and_subcatalog_page = preparation_work
    catalog_and_subcatalog_page.go_to_catalog_of_product()

    pagination_section = catalog_and_subcatalog_page.get_element(By.XPATH, locator.pagination_section)
    catalog_and_subcatalog_page.scroll_to_element(pagination_section)
    next_page_button, page_number = catalog_and_subcatalog_page.get_element_and_text(By.XPATH,
                                                                                     locator.first_button_in_pagination)
    catalog_and_subcatalog_page.click_element(next_page_button)
    new_page_number = catalog_and_subcatalog_page.driver.current_url.split('page/')[1].removesuffix("/")
    assert new_page_number == page_number, test_data.assertion_not_equals_page_numbers


# Блок "Товары" на стр. каталога товаров
def test_go_to_product_from_block_under_the_filter(preparation_work):
    catalog_and_subcatalog_page = preparation_work
    catalog_and_subcatalog_page.go_to_catalog_of_product()

    products = catalog_and_subcatalog_page.get_elements(By.XPATH, locator.products_under_the_filter)
    product = products[random.randint(0, 4)]
    product_title = get_element_in_another_element(product, By.TAG_NAME, "span").text
    link = get_element_in_another_element(product, By.TAG_NAME, "a")
    catalog_and_subcatalog_page.click_element(link)

    prod_title_in_new_page = catalog_and_subcatalog_page.get_element(By.XPATH, locator.product_title_in_new_page).text
    prod_title_in_new_page = prod_title_in_new_page.replace("’", "'").replace("‘", "'")
    assert prod_title_in_new_page == product_title, \
        test_data.assertion_error_not_equals_text_with_title_page


# Компонент поиска
def test_go_to_product_from_search_field(preparation_work):
    catalog_and_subcatalog_page = preparation_work

    catalog_and_subcatalog_page.print_in_field(By.XPATH, locator.search_field, test_data.search_product)
    catalog_and_subcatalog_page.find_and_click_on_element(By.CLASS_NAME, locator.search_button)

    product_links = catalog_and_subcatalog_page.get_elements(By.XPATH, locator.product_links)
    for product_link in product_links:
        catalog_and_subcatalog_page.click_element(product_link)

        catalog_and_subcatalog_page.expected_text_consist_in_searching_element(By.XPATH,
                                                     locator.product_title_in_new_page,
                                                     test_data.search_product.capitalize(),
                                                     test_data.assertion_error_in_test_go_to_product_from_search_field)
        catalog_and_subcatalog_page.driver.back()
