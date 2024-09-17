import pytest
import allure
from pages.catalog_and_category_page import CatalogAndCategoryPage
from pages.main_page import MainPage


# @pytest.mark.usefixtures('chrome_browser')
# @pytest.mark.usefixtures('edge_browser')
# @pytest.mark.usefixtures('firefox_browser')
@pytest.mark.usefixtures('browsers')
@allure.feature('Testing main page')
class TestsMainPage:

    @allure.story('testing link for go to sub catalog from main page')
    @pytest.mark.parametrize('serial_number', [0, 1, 2])
    def test_go_to_sub_catalog_from_main_page(self, main_page: MainPage, serial_number: int):
        """
        :param main_page: object
        :param serial_number: int, need point which catalog on main page you would like. Have a 3 variant
        """
        catalog, title = main_page.get_catalog_and_title(serial_number)
        catalog.click()

        if title == "Фотоаппараты":
            title = "Фото/видео"

        sub_catalog: CatalogAndCategoryPage = CatalogAndCategoryPage(main_page.driver, title)

        with allure.step('Check for match titles between sub catalog in main page and sub catalog page'):
            assert sub_catalog.get_title() == title, sub_catalog.logger.error("Couldn't get a catalog")

    @allure.story('testing link for go to product card from sales block')
    @pytest.mark.parametrize('visible_product', [5, 6])
    def test_go_to_product_card_from_sale_block(self, main_page: MainPage, visible_product: int):
        """
        :param main_page: object
        :param visible_product: int, need point product on sales section in main page you would like. Have a 16 variant, but can choise only 4 cause
        of only 4 variant is visible on page
        """
        product, title = main_page.go_to_product_from_sales_section(visible_product)

        with allure.step('Check for match titles between product in main page and product page'):
            assert title.capitalize() in product.get_title(), product.logger.error("Couldn't get a product from sales block")

    @allure.story('testing button in poster block for go to product page')
    @pytest.mark.xfail(
        reason="Incorrect behavior of the program, it was expected to match the names of products both on "
               "the product page and in the product card, but we get no match")
    def test_go_to_product_from_poster(self, main_page: MainPage):
        """
        :param main_page: object
        """
        product, title = main_page.get_product_and_title_from_poster_section()

        with allure.step('Check for match titles between product in main page and product page'):
            assert title.capitalize() in product.get_title(), product.logger.error("Couldn't get a product from poster section")

    @allure.story('testing links for product from arrivals block')
    @pytest.mark.parametrize('visible_product', [5, 6])
    def test_go_to_product_card_from_new_arrivals_block(self, main_page: MainPage, visible_product: int):
        """
        :param main_page: object
        :param visible_product: int, need point product on sales section in main page you would like. Have a 16 variant, but can choise only 4 cause
        of only 4 variant is visible on page
        """
        product, title = main_page.go_to_product_from_new_arrivals_section(visible_product)

        with allure.step('Check for match titles between product in main page and product page'):
            assert title.capitalize() in product.get_title(), product.logger.error("Couldn't get a product from arrivals block")

    @allure.story('testing links for product from viewed products')
    def test_go_to_product_card_from_viewed_products(self, main_page: MainPage):
        """
        :param main_page: object
        """
        main_page.go_to_product_from_sales_section(7)
        main_page.load()
        main_page.go_to_product_from_sales_section(8)
        main_page.load()

        product, title = main_page.go_to_viewed_product(1)

        with allure.step('Check for match titles between product in main page and product page'):
            assert title.capitalize() in product.get_title(), product.logger.error("Couldn't get a product from viewed section")
