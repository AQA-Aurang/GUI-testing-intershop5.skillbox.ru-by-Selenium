from time import sleep

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.main_page import MainPage
from pages.catalog_and_category_page import CatalogAndCategoryPage
from pages.product_card_page import ProductPage
from pages.search_page import SearchPage


@pytest.mark.usefixtures('browsers')
class TestsCatalogAndSubCatalogPage:

    # Страница каталога товаров
    def test_go_to_catalog_of_products(self, main_page: MainPage):
        main_page.go_to_catalog_page_from_navbar()

        catalog_page: CatalogAndCategoryPage = CatalogAndCategoryPage(main_page.driver, "Каталог")
        title_of_page: str = catalog_page.get_title()
        assert title_of_page == "Каталог", catalog_page.logger.error("Cannot go to catalog page")

    @pytest.mark.parametrize("catalog_item", [0, 1, 2, 3])
    def test_go_to_another_catalog_of_products(self, main_page: MainPage, catalog_item: int):
        title_of_catalog_item: str = main_page.go_to_another_catalogs_page_from_navbar(catalog_item)

        catalog_page: CatalogAndCategoryPage = CatalogAndCategoryPage(main_page.driver, title_of_catalog_item)
        title_of_page: str = catalog_page.get_title()
        assert title_of_page == title_of_catalog_item, catalog_page.logger.error(f"Cannot go to {title_of_catalog_item} page")

    # Страница подкатолога товаров
    @pytest.mark.parametrize("catalog_item, sub_catalog_item", [(0, 0), (0, 1),
                                                                (1, 2), (1, 6)])
    def test_go_to_sub_catalog_from_navbar(self, main_page: MainPage, catalog_item: int, sub_catalog_item: int):
        title_of_sub_catalog_item: str = main_page.go_to_sub_catalog_page_from_navbar(catalog_item, sub_catalog_item)

        sub_catalog_page: CatalogAndCategoryPage = CatalogAndCategoryPage(main_page.driver, title_of_sub_catalog_item)
        title_of_page: str = sub_catalog_page.get_title()
        assert title_of_page == title_of_sub_catalog_item, sub_catalog_page.logger.error(f"Cannot go to {title_of_sub_catalog_item} page")

    # Компонент сортировки товаров
    @pytest.mark.parametrize("sorting_by_characteristic", ["popularity", "rating", "date", "price", "price-desc"])
    def test_select_another_variant_from_product_sorting(self, electronic_sub_catalog_page: CatalogAndCategoryPage, sorting_by_characteristic: str):
        electronic_sub_catalog_page.select_item_from_sort_element(sorting_by_characteristic)
        url: str = electronic_sub_catalog_page.driver.current_url

        assert url.split("=")[1] == sorting_by_characteristic, electronic_sub_catalog_page.logger.error("Cannot switched sort element")

    # Компонент фильтра цен
    @pytest.mark.parametrize("min_pixel_offset, max_pixel_offset", [(10, 0), (15, 0), (0, 10), (0, 15), (10, 15), (15, 10)])
    def test_change_price_sliders(self, electronic_sub_catalog_page: CatalogAndCategoryPage, min_pixel_offset: int, max_pixel_offset: int):
        min_price, max_price = electronic_sub_catalog_page.use_price_filter(min_pixel_offset, max_pixel_offset)
        url: str = electronic_sub_catalog_page.driver.current_url

        assert str(min_price) in url and str(max_price) in url, \
            electronic_sub_catalog_page.logger.error("Cannot get a new products after change slider of filter")

    # Компонент пагинации страниц
    @pytest.mark.parametrize("index", [1, 7, 8])
    def test_pagination_in_catalog(self, catalog_and_sub_catalog_page: CatalogAndCategoryPage, index: int):
        pagination_buttons: list[WebElement] = catalog_and_sub_catalog_page.get_pagination_items()
        pagination_button: WebElement = pagination_buttons[index]
        expected_page: str = pagination_button.text
        pagination_button.click()
        url: str = catalog_and_sub_catalog_page.driver.current_url
        opened_page = url.split("/").pop(-2)

        if expected_page == "→":
            expected_page = opened_page

        assert opened_page == expected_page, catalog_and_sub_catalog_page.logger.error("Couldn't go to another page")

    # Блок "Товары" на стр. каталога товаров
    @pytest.mark.parametrize("index", [0, 2])
    def test_go_to_product_from_block_under_the_filter(self, electronic_sub_catalog_page: CatalogAndCategoryPage, index: int):
        products_in_block_under_the_filter: list[WebElement] = electronic_sub_catalog_page.get_all_products_from_goods_block()
        product: WebElement = products_in_block_under_the_filter[index]
        product_title: str = product.text
        product.click()
        product_card: ProductPage = ProductPage(electronic_sub_catalog_page.driver, product_title)

        assert product_card.get_title() == product_title.capitalize(), product_card.logger.error("Couldn't find product and go to product page")

    # Компонент поиска
    @pytest.mark.parametrize("searching_product", ["watch", "jeans", "abraka-dabra"])
    @pytest.mark.xfail
    def test_go_to_product_from_search_field(self, catalog_and_sub_catalog_page: CatalogAndCategoryPage, searching_product: str):
        catalog_and_sub_catalog_page.go_to_search_page(searching_product)

        searching_page: SearchPage = SearchPage(catalog_and_sub_catalog_page.driver, searching_product)
        if searching_page.searching_product_is_available():
            products_in_search_page: list[WebElement] = searching_page.get_products()
            product_in_search_page: WebElement = products_in_search_page[0]
            product_title_in_search_page: str = product_in_search_page.text.split("\n")[1]
            searching_page.get_element_from_another_element(product_in_search_page, By.XPATH, "//a[@class='collection_title']").click()
            product: ProductPage = ProductPage(searching_page.driver, product_title_in_search_page)

            assert searching_product in product.get_title(), product.logger.error("Could not find and go to product")
        else:
            assert False, searching_page.logger.error("Searching product was not found")
