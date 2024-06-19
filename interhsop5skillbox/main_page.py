import pytest
import interhsop5skillbox.utilities as utilities
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope="module")
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)

    yield wd
    wd.quit()

# -------------------------------------------------
# Блок с подкаталогами на гл. стр.
def get_sub_catalog_title(driver, element_text):
    while True:
        element = utilities.get_element(driver, By.XPATH, f"//h4[text()='{element_text}']")

        if element.is_displayed():
            sub_catalog1_title = element.text
            break

    return sub_catalog1_title


def test_go_to_sub_catalog_from_main_page(driver):
    driver.get("https://intershop5.skillbox.ru")

    # Checking 1st sub catalog
    sub_catalog1 = utilities.get_element(driver, By.ID, "accesspress_storemo-2")
    sub_catalog1_title = get_sub_catalog_title(driver, "Книги")

    sub_catalog1.find_element(By.TAG_NAME, "a").click()
    actual_result = utilities.get_element(driver, By.XPATH, "//h1[text()='Книги']")
    assert actual_result.text == sub_catalog1_title, "Cannot redirect to 'Книги' sub catalog from main page"

    driver.back()

    # Checking 2nd sub catalog
    sub_catalog2 = utilities.get_element(driver, By.ID, "accesspress_storemo-3")
    sub_catalog2_title = get_sub_catalog_title(driver, "Планшеты")

    sub_catalog2.find_element(By.TAG_NAME, "a").click()
    actual_result = utilities.get_element(driver, By.XPATH, "//h1[text()='Планшеты']")
    assert actual_result.text == sub_catalog2_title, "Cannot redirect to 'Планшеты' sub catalog from main page"

    driver.back()

    # Checking 3rd sub catalog
    sub_catalog3 = utilities.get_element(driver, By.ID, "accesspress_storemo-4")
    sub_catalog3.find_element(By.TAG_NAME, "a").click()

    expected_result = "Фото/видео"
    actual_result = utilities.get_element(driver, By.XPATH, "//h1[text()='Фото/видео']")
    assert actual_result.text.upper() == expected_result.upper(), "Cannot redirect to 'Фото/видео' sub catalog"


# Блок "Распродажа" на гл. стр.
def test_go_to_product_card_from_sale_block(driver):
    driver.get("https://intershop5.skillbox.ru")

    height = driver.execute_script("return window.innerHeight;")
    driver.execute_script(f"window.scrollTo(0, {height * 0.95});")

    product = utilities.get_element(driver, By.XPATH, "//li[@data-slick-index='1']")
    product_title = product.find_element(By.TAG_NAME, "a").get_attribute("title")
    utilities.get_element(driver, By.XPATH, f"//li[@data-slick-index='1']/div/a[@title='{product_title}']").click()

    expected_result = "ВСЕ ТОВАРЫ"
    actual_result = utilities.get_element(driver, By.XPATH, "//h1[@class='entry-title ak-container']")
    assert actual_result.text == expected_result, "Cannot go to product card"


# Блок "Новые поступления" на гл. стр.
def test_go_to_product_card_from_new_arrivals_block(driver):
    driver.get("https://intershop5.skillbox.ru")

    height = driver.execute_script("return window.innerHeight;")
    driver.execute_script(f"window.scrollTo(0, {height * 2.7});")

    product = utilities.get_element(driver, By.XPATH, "(//div[@class='slick-track'])[3]/li[@data-slick-index='1']")
    product_title = product.find_element(By.TAG_NAME, "a").get_attribute("title")

    utilities.get_element(driver, By.XPATH, f"(//div[@class='slick-track'])[3]/li[@data-slick-index='1']/div/a[@title='{product_title}']").click()

    expected_result = "ВСЕ ТОВАРЫ"
    actual_result = utilities.get_element(driver, By.XPATH, "//h1[@class='entry-title ak-container']")
    assert actual_result.text == expected_result, "Cannot go to product card"


# Блок "Просмотренные товары" на гл. стр.
def test_go_to_product_card_from_viewed_products(driver):
    driver.get("https://intershop5.skillbox.ru")

    height = driver.execute_script("return window.innerHeight;")
    driver.execute_script(f"window.scrollTo(0, {height * 0.95});")

    product = utilities.get_element(driver, By.XPATH, "//li[@data-slick-index='1']")
    product_title = product.find_element(By.TAG_NAME, "a").get_attribute("title")

    utilities.get_element(driver, By.XPATH, f"//li[@data-slick-index='1']/div/a[@title='{product_title}']").click()

    expected_result = "ВСЕ ТОВАРЫ"
    actual_result = utilities.get_element(driver, By.XPATH, "//h1[@class='entry-title ak-container']")

    if actual_result.text == expected_result:
        utilities.get_element(driver, By.LINK_TEXT, "Главная").click()
        height = driver.execute_script("return window.innerHeight;")
        driver.execute_script(f"window.scrollTo(0, {height * 5.5});")

        try:
            viewed_products_block = utilities.get_element(driver, By.ID, "woocommerce_recently_viewed_products-2")
            header_viewed_products = viewed_products_block.find_element(By.TAG_NAME, "h2")
            viewed_product = viewed_products_block.find_element(By.TAG_NAME, "li")

            if header_viewed_products.text == "Просмотренные товары".upper():
                viewed_product_title = viewed_product.find_element(By.TAG_NAME, "span").text
                viewed_product_title = viewed_product_title.replace("'", "’")

                if viewed_product_title == product_title:
                    viewed_product.find_element(By.TAG_NAME, "a").click()

                    expected_result = "ВСЕ ТОВАРЫ"
                    actual_result = utilities.get_element(driver, By.XPATH, "//h1[@class='entry-title ak-container']")

                    assert actual_result.text == expected_result, "Cannot redirect to viewed product"
        except Exception as e:
            print("Something went wrong -", e.args[0])