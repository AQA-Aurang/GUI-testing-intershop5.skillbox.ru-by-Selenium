import pytest, re, random
import interhsop5skillbox.utilities as utilities
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

@pytest.fixture(scope="module")
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(20)

    # Increase page load timeout to 40 seconds
    wd.set_page_load_timeout(40)

    # Increase JavaScript execution timeout to 20 seconds
    wd.set_script_timeout(20)

    yield wd
    wd.quit()

# -------------------------------------------------
# Карточка товара 1
def go_to_product(driver):
    driver.get("https://intershop5.skillbox.ru")
    utilities.get_element(driver, By.XPATH, "(//li[@data-slick-index='0'])[1]/div/a").click()


def test_upsize_count_buying_product(driver):
    go_to_product(driver)

    try:
        quantity_input = utilities.get_element(driver, By.NAME, "quantity")
        quantity_input.clear()
        quantity_input.send_keys("4")

    except Exception as e:
        assert False, f"Dont find needed filed {e.args}"


def test_downsize_count_buying_product(driver):
    go_to_product(driver)

    try:
        quantity_input = utilities.get_element(driver, By.NAME, "quantity")
        quantity_input.clear()
        quantity_input.send_keys("0")

    except Exception as e:
        assert False, f"Dont find needed filed {e.args}"


def test_add_product_to_cart(driver):
    go_to_product(driver)

    try:
        utilities.get_element(driver, By.NAME, "add-to-cart").click()
        pop_up_button = utilities.get_element(driver, By.XPATH, "//a[@class='button wc-forward']")

        assert pop_up_button.is_enabled() and pop_up_button.is_displayed(), "Can't added product in cart"
    except Exception as e:
        print(f"Something went wrong {e.args}")


def test_adding_more_items_than_are_in_stock(driver):
    go_to_product(driver)

    try:
        product_in_stock = utilities.get_element(driver, By.XPATH, "//p[@class='stock in-stock']")
        product_in_stock_count = int(re.findall(r"\d+", product_in_stock.text)[0])

        quantity_field = utilities.get_element(driver, By.NAME, "quantity")

        while True:
            rand_num = random.randint(1, product_in_stock_count * 2)

            if rand_num > product_in_stock_count:
                break

        quantity_field.clear()
        quantity_field.send_keys(str(rand_num))
        utilities.get_element(driver, By.NAME, "add-to-cart").click()

        # Check whether it was possible to add items to the cart
        try:
            utilities.get_element(driver, By.XPATH, "//div[@role='alert']/text()")
        except TimeoutException:
            assert True, "Got to add more products to the cart than in stock"

    except NoSuchElementException as NoSuch:
        assert False, f"Cannot find element - {NoSuch.args}"
    except Exception as e:
        print(f"Something went wrong - {e.args}")


def test_zoom_product_with_magnifying_glass_on_product_card(driver):
    go_to_product(driver)

    try:
        utilities.get_element(driver, By.CLASS_NAME, "woocommerce-product-gallery__trigger").click()
        zoom_window = utilities.get_element(driver, By.CLASS_NAME, "pswp__img")

        assert zoom_window.is_enabled(), "Zoom element is disable"
    except Exception:
        assert False, "Cannot find zoom element"


def test_leave_review_for_product(driver):
    driver.get("http://intershop5.skillbox.ru")
    driver = utilities.login(driver)

    driver.find_element(By.LINK_TEXT, "Заказы").click()

    # like a test we go in the next order page for get product with link
    # driver.find_element(By.LINK_TEXT, "Next").click()

    utilities.get_element(driver, By.XPATH, "(//td[@data-title='Заказ']//a)[1]").click()
    ordered_product = utilities.get_element(driver, By.XPATH, "//td[@class='woocommerce-table__product-name product-name']")

    try:
        ordered_product.find_element(By.TAG_NAME, "a").click()
        utilities.get_element(driver, By.XPATH, "//a[@href='#tab-reviews']").click()

        stars = driver.find_elements(By.CSS_SELECTOR, ".stars>span>a")
        product_mark = random.randint(0, 4)
        stars[product_mark].click()

        review_field = utilities.get_element(driver, By.XPATH, "//textarea[@id='comment']")
        review_txt = ""

        match product_mark:
            case 0:
                review_txt = "Не советую, мне не понравилось"
            case 1:
                review_txt = "Так себе, можно найти по лучше за такую цену"
            case 2:
                review_txt = "В целом всё норм, ничего плохого не могу сказать, получил то что заказывал"
            case 3:
                review_txt = "Не плохая вешь, мне понравилось, однозначно могу посоветовать"
            case 4:
                review_txt = "Берите не пожалейте, меня устраивает, уже который год пользуюсь"

        review_field.send_keys(review_txt)
        utilities.get_element(driver, By.CLASS_NAME, "submit").submit()
        saved_review = utilities.get_element(driver, By.XPATH, f"//p[text()='{review_txt}']").text

        assert saved_review == review_txt, "Review not sent"
    except NoSuchElementException:
        assert False, "No such element on DOM"
    except Exception as e:
        print("Error -", e.args)


# Блок "Категория товаров"
def test_go_to_catelog_subcatelog_in_sideblock_on_product_page(driver):
    go_to_product(driver)

    categories = utilities.get_elements(driver, By.XPATH, "//li[contains(@class,'cat-item')]//a")
    category_link = categories[random.randint(0, len(categories)-1)]
    title_category = category_link.text
    category_link.click()

    title_page = utilities.get_element(driver, By.XPATH, "//h1[@class='entry-title ak-container']").text
    assert title_page.capitalize() == title_category, "Title selected category not equal title of page"


# Блок "Сопутствующие товары"
def test_go_to_product_from_related_products_on_product_page(driver):
    go_to_product(driver)

    product_from_related_products = utilities.get_element(driver, By.XPATH, f"(//a[@class='collection_title']//h3)[{random.randint(1, 3)}]")
    title_product = product_from_related_products.text
    product_from_related_products.click()

    title_page = utilities.get_element(driver, By.XPATH, "//h1[@class='product_title entry-title']").text
    assert title_page == title_product, "Titles of products is not equals"


def get_product_and_his_title(driver):
    if EC.visibility_of_element_located((By.XPATH, "//ul[@class='products columns-4']//li/div[2]")):
        products_card_footers = utilities.get_elements(driver, By.XPATH, "//ul[@class='products columns-4']//li/div[2]")
    else:
        return "Element not visible", 0

    for x in range(len(products_card_footers)):
        product_card_footer = products_card_footers[x]
        title_product = product_card_footer.find_element(By.XPATH, "//a/h3").text
        button_to_add_cart = utilities.get_element(driver, By.XPATH, "//ul[@class='products columns-4']//li/div[2]/div/a")
        # print("\nx -", x, "button title -", button_to_add_cart.text.capitalize())

        if button_to_add_cart.text.capitalize() == "В корзину":
            return title_product, x

    return "To cart not found", 0


def test_add_item_to_cart_from_related_products_on_product_page(driver):
    go_to_product(driver)

    while True:
        title_product, item_numb = get_product_and_his_title(driver)
        # print("title_product -", title_product)

        if title_product != "Element not visible" and title_product != "To cart not found":
            break

        driver.refresh()

    # height = driver.execute_script("return window.innerHeight;")
    # driver.execute_script(f"window.scrollTo(0, {height * 1.25});")
    #
    # screenshot = driver.get_screenshot_as_png()
    # with open("C:/Users/Farid/Desktop/screenshot4.png", "wb") as f:
    #     f.write(screenshot)

    utilities.get_element(driver, By.XPATH, f"//ul[@class='products columns-4']//li/div[2]/div/a[{item_numb+1}]").click()
    utilities.get_element(driver, By.XPATH, "//a[@title='Подробнее']").click()

    title_of_added_in_cart_product = utilities.get_element(driver, By.XPATH, f"//td[@data-title='Товар']/a[contains(text(), '{title_product}')]").text

    assert title_of_added_in_cart_product == title_product, "Titles of products not equals"


# Блок "Товары"
def test_go_to_product_from_products_sidebar_on_product_page(driver):
    go_to_product(driver)

    try:
        products_in_sideblock = utilities.get_elements(driver, By.XPATH, "//ul[@class='product_list_widget']//li")
        # time.sleep(3)
        product = products_in_sideblock[random.randint(0, 4)].find_element(By.TAG_NAME, "a")
        title_product = product.text
        product.click()

        title_product_in_new_page = utilities.get_element(driver, By.XPATH, "//h1[@class='product_title entry-title']").text
        if "‘" in title_product_in_new_page and "’" in title_product_in_new_page:
            title_product_in_new_page = title_product_in_new_page.replace("‘", "'").replace("’", "'")

        assert title_product_in_new_page == title_product, "Titles of products not equals"
    except Exception as e:
        assert False, f"Something went wrong {e.args}"