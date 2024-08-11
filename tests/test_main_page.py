import time

import pytest

from pages.catalog_and_category_page import CatalogAndCategoryPage


@pytest.mark.usefixtures('chrome_browser')
class Tests:

    @pytest.mark.parametrize('serial_number', [0, 1, 2])
    def test_go_to_sub_catalog_from_main_page(self, prepare_main_page, serial_number):
        prepare_main_page.check_and_go_back_in_main_page()

        catalog, title = prepare_main_page.get_catalog_and_title(serial_number)
        catalog.click()

        if title == "Фотоаппараты":
            title = "Фото/видео"

        sub_catalog_of_pad = CatalogAndCategoryPage(prepare_main_page.driver, title)

        assert sub_catalog_of_pad.get_title() == title, "Couldn't get a catalog"

    @pytest.mark.parametrize('visible_product', [4, 5])
    def test_go_to_product_card_from_sale_block(self, prepare_main_page, visible_product):
        prepare_main_page.check_and_go_back_in_main_page()

        product, title = prepare_main_page.go_to_product_from_sales_section(visible_product)
        assert product.get_title() == title.capitalize(), "Couldn't get a product from sales block"

    @pytest.mark.xfail(reason="Incorrect behavior of the program, it was expected to match the names of products both on "
                              "the product page and in the product card, but we get no match")
    def test_go_to_product_from_poster(self, prepare_main_page):
        prepare_main_page.check_and_go_back_in_main_page()

        product, title = prepare_main_page.get_product_and_title_from_poster_section()

        assert product.get_title() == title.capitalize(), "Couldn't get a product from poster section"

    @pytest.mark.parametrize('visible_product', [4, 6])
    def test_go_to_product_card_from_new_arrivals_block(self, prepare_main_page, visible_product):
        prepare_main_page.check_and_go_back_in_main_page()

        product, title = prepare_main_page.go_to_product_from_new_arrivals_section(visible_product)
        assert product.get_title() == title.capitalize(), "Couldn't get a product from arrivals block"

    def test_go_to_product_card_from_viewed_products(self, prepare_main_page):
        prepare_main_page.check_and_go_back_in_main_page()

        product, title = prepare_main_page.go_to_viewed_product(1)

        assert product.get_title() == title.capitalize(), "Couldn't get a product from viewed section"
