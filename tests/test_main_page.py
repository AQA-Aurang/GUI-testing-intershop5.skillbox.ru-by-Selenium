import pytest

from conftest import chrome_browser as driver
from conftest import get_webdriver_instance_and_open_main_page as preparation_work
from pages.catalog_and_category_page import CatalogAndCategoryPage


@pytest.mark.parametrize('serial_number', [0, 1, 2])
def test_go_to_sub_catalog_from_main_page(preparation_work, serial_number):
    main_page = preparation_work

    catalog, title = main_page.get_catalog_and_title(serial_number)
    catalog.click()

    if title == "Фотоаппараты":
        title = "Фото/видео"

    sub_catalog_of_pad = CatalogAndCategoryPage(main_page.driver, title)

    assert sub_catalog_of_pad.get_title() == title, "Couldn't get a catalog"


@pytest.mark.parametrize('visible_product', [4, 5])
def test_go_to_product_card_from_sale_block(preparation_work, visible_product):
    main_page = preparation_work

    product, title = main_page.go_to_product_from_sales_section(visible_product)
    assert product.get_title() == title, "Couldn't get a product from sales block"


@pytest.mark.xfail(reason="Incorrect behavior of the program, it was expected to match the names of products both on "
                          "the product page and in the product card, but we get no match")
def test_go_to_product_from_poster(preparation_work):
    main_page = preparation_work
    product, title = main_page.get_product_and_title_from_poster_section()

    assert product.get_title() == title.capitalize(), "Couldn't get a product from poster section"


@pytest.mark.parametrize('visible_product', [4, 6])
def test_go_to_product_card_from_new_arrivals_block(preparation_work, visible_product):
    main_page = preparation_work

    product, title = main_page.go_to_product_from_new_arrivals_section(visible_product)
    assert product.get_title() == title, "Couldn't get a product from arrivals block"


@pytest.mark.xfail(reason="If the session is new, there are no information about the viewed products")
def test_go_to_product_card_from_viewed_products(preparation_work):
    main_page = preparation_work
    product, title = main_page.go_to_viewed_product(3)

    assert product.get_title() == title, "Couldn't get a product from viewed section"
