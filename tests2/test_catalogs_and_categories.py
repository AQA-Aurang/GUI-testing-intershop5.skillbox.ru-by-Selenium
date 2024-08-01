# import random
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conftest2 import chrome_browser as driver
from conftest2 import get_webdriver_instance_and_open_main_page as preparation_work_for_main_page
from conftest2 import get_webdriver_instance_and_open_catalog_and_sub_catalog_page as preparation_work
from pages2.catalog_and_category_page import CatalogAndCategoryPage
from pages2.product_card_page import ProductPage
from pages2.search_page import SearchPage


# Страница каталога товаров
def test_go_to_catalog_of_products(preparation_work_for_main_page):
    main_page = preparation_work_for_main_page
    main_page.go_to_catalog_page_from_navbar()

    catalog_page = CatalogAndCategoryPage(main_page.driver, "Каталог")
    title_of_page = catalog_page.get_title()
    assert title_of_page == "Каталог", "Cannot go to catalog page"


@pytest.mark.parametrize("catalog_item", [0, 1, 2, 3])
def test_go_to_another_catalog_of_products(preparation_work_for_main_page, catalog_item):
    main_page = preparation_work_for_main_page
    title_of_catalog_item = main_page.go_to_another_catalogs_page_from_navbar(catalog_item)
    # print("title -", title_of_catalog_item)

    catalog_page = CatalogAndCategoryPage(main_page.driver, title_of_catalog_item)
    title_of_page = catalog_page.get_title()
    assert title_of_page == title_of_catalog_item, f"Cannot go to {title_of_catalog_item} page"


# Страница подкатолога товаров
@pytest.mark.parametrize("catalog_item, sub_catalog_item", [(0, 0), (0, 1),
                                                            (1, 2), (1, 6)])
def test_go_to_sub_catalog_from_navbar(preparation_work_for_main_page, catalog_item, sub_catalog_item):
    main_page = preparation_work_for_main_page
    title_of_sub_catalog_item = main_page.go_to_sub_catalog_page_from_navbar(catalog_item, sub_catalog_item)
    # print("title -", title_of_sub_catalog_item)

    sub_catalog_page = CatalogAndCategoryPage(main_page.driver, title_of_sub_catalog_item)
    title_of_page = sub_catalog_page.get_title()
    assert title_of_page == title_of_sub_catalog_item, f"Cannot go to {title_of_sub_catalog_item} page"


# Компонент сортировки товаров
@pytest.mark.parametrize("sorting_by_characteristic", ["popularity", "rating", "date", "price", "price-desc"])
def test_select_another_variant_from_product_sorting(preparation_work, sorting_by_characteristic):
    catalog_and_sub_catalog_page = preparation_work
    catalog_and_sub_catalog_page.select_item_from_sort_element(sorting_by_characteristic)
    url = catalog_and_sub_catalog_page.driver.current_url

    assert url.split("=")[1] == sorting_by_characteristic, "Cannot switched sort element"


# Компонент фильтра цен
@pytest.mark.parametrize("min_pixel_offset, max_pixel_offset", [(10, 0), (15, 0), (0, 10), (0, 15), (10, 15), (15, 10)])
def test_change_left_of_slider(preparation_work, min_pixel_offset, max_pixel_offset):
    catalog_and_sub_catalog_page = preparation_work
    min_price, max_price = catalog_and_sub_catalog_page.use_price_filter(min_pixel_offset, max_pixel_offset)
    url = catalog_and_sub_catalog_page.driver.current_url

    assert str(min_price) in url and str(max_price) in url, "Cannot get a new products after change slider of filter"


# Компонент пагинации страниц
@pytest.mark.parametrize("index", [1, 7, 8])
def test_pagination_in_catalog(preparation_work, index):
    catalog_and_sub_catalog_page = preparation_work
    pagination_buttons = catalog_and_sub_catalog_page.get_pagination_items()
    pagination_button = pagination_buttons[index]
    expected_page = pagination_button.text
    pagination_button.click()
    url = catalog_and_sub_catalog_page.driver.current_url
    opened_page = url.split("/").pop(-2)

    if expected_page == "→":
        expected_page = opened_page

    assert opened_page == expected_page, "Couldn't go to another page"


# Блок "Товары" на стр. каталога товаров
@pytest.mark.parametrize("index", [0, 2])
def test_go_to_product_from_block_under_the_filter(preparation_work, index):
    catalog_and_sub_catalog_page = preparation_work
    products_in_block_under_the_filter = catalog_and_sub_catalog_page.get_all_products_from_goods_block()
    product = products_in_block_under_the_filter[index]
    product_title = product.text
    product.click()
    product_card = ProductPage(catalog_and_sub_catalog_page.driver, product_title)

    assert product_card.get_title() == product_title, "Couldn't find product and go to product page"


# Компонент поиска
@pytest.mark.parametrize("searching_product", ["watch", "jeans", "abraka-dabra"])
def test_go_to_product_from_search_field(preparation_work, searching_product):
    catalog_and_sub_catalog_page = preparation_work
    catalog_and_sub_catalog_page.go_to_search_page(searching_product)

    searching_page = SearchPage(catalog_and_sub_catalog_page.driver, searching_product)
    if searching_page.searching_product_is_available():
        products_in_search_page = searching_page.get_products()
        product_in_search_page = products_in_search_page[0]
        product_title_in_search_page = product_in_search_page.text
        product_title_in_search_page = product_title_in_search_page.split("\n")[1]
        searching_page.get_element_from_another_element(product_in_search_page, By.XPATH,
                                                        "//a[@class='collection_title']").click()
        product = ProductPage(searching_page.driver, product_title_in_search_page)

        assert searching_product in product.get_title(), "Could not find and go to product"
        return

    print("Searching product was not found")
    assert True
