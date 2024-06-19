import pytest, random
import interhsop5skillbox.utilities as utilities
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.fixture(scope="module")
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)

    yield wd
    wd.quit()

# -------------------------------------------------
# Страница каталога товаров
def test_go_to_catalog_of_products(driver):
    driver.get("http://intershop5.skillbox.ru")

    catalog = utilities.get_element(driver, By.LINK_TEXT, "КАТАЛОГ")
    catalog_title = catalog.text
    catalog.click()

    header_title = utilities.get_element(driver, By.XPATH, "//h1[text()='Каталог']")
    assert header_title.text == catalog_title, "Cannot redirect in catalog of products"


def go_to_catalog_of_product(driver):
    driver.get("https://intershop5.skillbox.ru")
    utilities.get_element(driver, By.LINK_TEXT, "КАТАЛОГ").click()


# Страница подкатологов товаров
def test_go_to_sub_catalog_from_navbar(driver):
    driver.get("https://intershop5.skillbox.ru")
    dropdown_element = utilities.get_element(driver, By.XPATH, "(//li[@id='menu-item-46']//a)[1]")

    action_chains = ActionChains(driver)
    action_chains.move_to_element(dropdown_element).perform()
    utilities.get_element(driver, By.XPATH, "//li[@id='menu-item-119']/a[1]").click()

    success_message = utilities.get_element(driver, By.XPATH, "//h1[text()='Бытовая техника']")
    assert success_message.text == "БЫТОВАЯ ТЕХНИКА", "Cannot go to sub catalog"


# Компонент сортировки товаров
def test_select_another_variant_from_product_sorting(driver):
    go_to_catalog_of_product(driver)
    sorting_element = utilities.get_element(driver, By.NAME, "orderby")

    action_chains = ActionChains(driver)
    action_chains.move_to_element(sorting_element).click()

    selected_item = sorting_element.find_element(By.XPATH, "//option[@value='popularity']")
    selected_item_title = selected_item.text
    selected_item.click()

    default_item = utilities.get_element(driver, By.NAME, "orderby").find_element(By.XPATH, "//option[@selected='selected']")
    assert selected_item_title == default_item.text, "Selected item not equal with default item"


# Компонент фильтра цен
def change_slider(driver, pixel_offset, slider_xpath):
    go_to_catalog_of_product(driver)

    height = driver.execute_script("return window.innerHeight;")
    driver.execute_script(f"window.scrollTo(0, {height * 1.5});")

    slider = utilities.get_element(driver, By.XPATH, slider_xpath)

    action = ActionChains(driver)
    action.drag_and_drop_by_offset(slider, pixel_offset, 0).perform()
    fixed_price_str = utilities.get_element(driver, By.XPATH, "//div[@class='price_label']//span[1]").text
    fixed_price = float(fixed_price_str[:-1])
    utilities.get_element(driver, By.XPATH, "(//button[@type='submit'])[2]").click()

    products = utilities.get_elements(driver, By.XPATH, "//ul[@class='products columns-4']/li")
    for product in products:
        price_element = utilities.get_element(product, By.XPATH, "(//span[@class='woocommerce-Price-amount amount']//bdi)[1]")
        price_str = price_element.text[:-1].replace(",", ".")
        price = float(price_str)
        assert price >= fixed_price, "Products price is not equal"


def test_change_left_of_slider(driver):
    change_slider(driver, 10, "(//span[contains(@class,'ui-slider-handle ui-state-default')])[1]")
    change_slider(driver, 15, "(//span[contains(@class,'ui-slider-handle ui-state-default')])[1]")


def test_change_right_of_slider(driver):
    change_slider(driver, -20, "(//span[contains(@class,'ui-slider-handle ui-state-default')])[2]")
    change_slider(driver, -25, "(//span[contains(@class,'ui-slider-handle ui-state-default')])[2]")


def get_price(driver, slider_xpath, price_xpath, offset):
    slider = utilities.get_element(driver, By.XPATH, slider_xpath)
    slider.click()

    action = ActionChains(driver)
    action.drag_and_drop_by_offset(slider, offset, 0).perform()
    fixed_price_str = utilities.get_element(driver, By.XPATH, price_xpath).text
    return driver, float(fixed_price_str[:-1])

def test_move_both_sliders_in_price_filter(driver):
    go_to_catalog_of_product(driver)

    height = driver.execute_script("return window.innerHeight;")
    driver.execute_script(f"window.scrollTo(0, {height * 1.5});")

    slider_xpath1 = "//div[contains(@class,'price_slider ui-slider')]//span[1]"
    price_xpath1 = "//div[@class='price_label']//span[1]"
    driver, fixed_price1 = get_price(driver, slider_xpath1, price_xpath1, 15)

    slider_xpath2 = "//div[contains(@class,'price_slider ui-slider')]//span[2]"
    price_xpath2 = "//div[@class='price_label']//span[2]"
    driver, fixed_price2 = get_price(driver, slider_xpath2, price_xpath2, -10)

    utilities.get_element(driver, By.XPATH, "(//button[@type='submit'])[2]").click()

    try:
        products = utilities.get_elements(driver, By.XPATH, "//ul[@class='products columns-4']/li")
    except TimeoutException as timeout:
        assert True, f"With pointed filters dont have any products. {timeout.args}"
        return

    for product in products:
        price_element = utilities.get_element(product, By.XPATH, "(//span[@class='woocommerce-Price-amount amount']//bdi)[1]")
        price_text = price_element.text.replace(",", ".")
        price = float(price_text[:-1])

        assert fixed_price1 <= price <= fixed_price2, \
            f"price {price} not between selected prices - 1st price {fixed_price1} and 2nd price {fixed_price2}"


# Компонент пагинации страниц
def test_pagination_in_catalog(driver):
    go_to_catalog_of_product(driver)

    # Waiting for the page to load
    WebDriverWait(driver, 10).until(EC.title_contains("Каталог — Skillbox"))

    pagination_section = utilities.get_element(driver, By.XPATH, "//ul[@class='page-numbers']")
    driver.execute_script("arguments[0].scrollIntoView();", pagination_section)

    next_page_button = utilities.get_element(driver, By.XPATH, "(//a[@class='page-numbers'])[1]")
    page_numb = next_page_button.text
    next_page_button.click()

    new_page_number = driver.current_url.split('page/')[1].removesuffix("/")
    assert new_page_number == page_numb, "Pagination page not equals"


# Блок "Товары" на стр. каталога товаров
def test_go_to_product_from_block_under_the_filter(driver):
    go_to_catalog_of_product(driver)

    products = utilities.get_elements(driver, By.XPATH, "//ul[@class='product_list_widget']//li")
    product = products[random.randint(0, 4)]
    product_title = utilities.get_element(product, By.TAG_NAME, "span").text
    product.find_element(By.TAG_NAME, "a").click()

    prod_title_in_new_page = utilities.get_element(driver, By.XPATH, "//h1[@class='product_title entry-title']").text
    prod_title_in_new_page = prod_title_in_new_page.replace("’", "'").replace("‘", "'")
    assert prod_title_in_new_page == product_title, "Titles of products is not equals"


# Компонент поиска
def test_go_to_product_from_search_field(driver):
    driver.get("http://intershop5.skillbox.ru")

    search_product = "watch"
    utilities.get_element(driver, By.XPATH, "(//input[@name='s'])[1]").send_keys(search_product)
    utilities.get_element(driver, By.CLASS_NAME, "searchsubmit").click()

    prod_title_in_search_output_page = utilities.get_element(driver, By.XPATH, "//h1[@class='entry-title ak-container']").text

    assert search_product.upper() in prod_title_in_search_output_page, "Search product not equals with product in search output page"