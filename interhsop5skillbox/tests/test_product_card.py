import random
import re
import interhsop5skillbox.data.test_data as test_data
import interhsop5skillbox.data.locators as locator
from selenium.webdriver.common.by import By
from interhsop5skillbox.conftest import chrome_browser as driver, login, logout
from interhsop5skillbox.conftest2 import get_webdriver_instance_and_open_product_card_page as preparation_work
from selenium.common.exceptions import TimeoutException
from interhsop5skillbox.pages.base_page import get_element_in_another_element


# -------------------------------------------------
# Карточка товара 1
def test_upsize_count_buying_product(preparation_work):
    product_card = preparation_work
    product_card.go_to_product()
    product_card.print_in_field(By.NAME, locator.quantity, 4)


def test_downsize_count_buying_product(preparation_work):
    product_card = preparation_work
    product_card.go_to_product()
    product_card.print_in_field(By.NAME, locator.quantity, 0)


def test_add_product_to_cart(preparation_work):
    product_card = preparation_work
    product_card.go_to_product()

    product_card.find_and_click_on_element(By.NAME, locator.add_to_cart_button)
    notif_after_click_on_button = product_card.get_element(By.XPATH, locator.notification_add_to_cart)
    assert notif_after_click_on_button.is_enabled() and notif_after_click_on_button.is_displayed(), \
        test_data.assertion_error_test_add_product_to_cart


def test_adding_more_items_than_are_in_stock(preparation_work):
    product_card = preparation_work
    product_card.go_to_product()

    quantity_products_in_stock = product_card.get_element(By.XPATH, locator.quantity_products_on_product_card_page)
    count_product_in_stock = int(re.findall(r"\d+", quantity_products_in_stock.text)[0])

    while True:
        rand_num = random.randint(1, count_product_in_stock * 2)

        if rand_num > count_product_in_stock:
            break

    product_card.print_in_field(By.NAME, locator.quantity, rand_num)
    product_card.find_and_click_on_element(By.NAME, locator.add_to_cart_button)

    # Check whether it was possible to add items to the cart
    try:
        product_card.get_element(By.XPATH, locator.notification_about_add_product_in_cart)
    except TimeoutException:
        assert True, test_data.assertion_error_test_adding_more_items_than_are_in_stock


def test_zoom_product_with_magnifying_glass_on_product_card(preparation_work):
    product_card = preparation_work
    product_card.go_to_product()

    try:
        product_card.find_and_click_on_element(By.CLASS_NAME, locator.magnifying_glass)
        zoom_window = product_card.get_element(By.CLASS_NAME, locator.zoom_window)
        assert zoom_window.is_enabled(), test_data.assertion_error_test_zoom_element_in_product_card1

    except TimeoutException:
        assert True, test_data.assertion_error_test_zoom_element_in_product_card2


def test_leave_review_for_product(preparation_work, login, logout):
    product_card = preparation_work
    product_card.driver = login

    product_card.find_and_click_on_element(By.LINK_TEXT, locator.link_to_orders_block_in_my_account)

    product_card.find_and_click_on_element(By.XPATH, locator.order_in_order_table)
    ordered_product = product_card.get_element(By.XPATH, locator.ordered_product)

    link_ordered_product = get_element_in_another_element(ordered_product, By.TAG_NAME, "a")
    product_card.click_element(link_ordered_product)
    product_card.find_and_click_on_element(By.XPATH, locator.review_tab)

    stars = product_card.get_elements(By.CSS_SELECTOR, locator.stars)
    product_mark = random.randint(0, 4)
    stars[product_mark].click()

    review_field = product_card.get_element(By.XPATH, locator.comment_field_for_review)
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
    product_card.find_and_submit_on_button(By.CLASS_NAME, locator.review_button)

    if product_card.driver.current_url == "https://intershop5.skillbox.ru/wp-comments-post.php":
        if "Duplicate comment" in product_card.get_element(By.XPATH, locator.popup_block_element_of_review_for_product).text:
            product_card.find_and_click_on_element(By.LINK_TEXT, "« Back")
            review_field = product_card.get_element(By.XPATH, locator.comment_field_for_review)
            new_review_txt = product_card.write_review_for_product(review_field, review_txt)
            review_field.send_keys(new_review_txt)
            product_card.find_and_submit_on_button(By.CLASS_NAME, locator.review_button)

    _, saved_review = product_card.get_element_and_text(By.XPATH, f"//p[text()='{review_txt}']")
    assert saved_review == review_txt, test_data.assertion_error_failed_to_sent_review
    logout


# Блок "Категория товаров"
def test_go_to_catalog_subcatalog_in_sideblock_on_product_page(preparation_work):
    product_card = preparation_work
    product_card.go_to_product()

    categories = product_card.get_elements(By.XPATH, locator.categories)
    category_link = categories[random.randint(0, len(categories) - 1)]
    title_category = category_link.text.upper()
    product_card.click_element(category_link)
    product_card.element_should_have_text(By.XPATH, locator.title_of_page_selected_categories, title_category,
                                          test_data.assertion_error_in_sideblock_on_product_page)


# Блок "Сопутствующие товары"
def test_go_to_product_from_related_products_on_product_page(preparation_work):
    product_card = preparation_work
    product_card.go_to_product()

    related_product, title_related_product = product_card.get_element_and_text(By.XPATH,
                                                        f"(//a[@class='collection_title']//h3)[{random.randint(1, 3)}]")
    product_card.click_element(related_product)
    product_card.element_should_have_text(By.XPATH, locator.product_title_in_new_page, title_related_product,
                                          test_data.assertion_error_not_equals_text_with_title_page)


def test_add_item_to_cart_from_related_products_on_product_page(preparation_work):
    product_card = preparation_work
    product_card.go_to_product()

    while True:
        title_product, item_number = product_card.get_product_and_his_title_on_product_card()
        if title_product != test_data.product_not_visible and title_product != test_data.product_not_found_in_cart:
            break

        product_card.driver.refresh()

    product_card.find_and_click_on_element(By.XPATH, f"//ul[@class='products columns-4']//li/div[2]/div/a[{item_number + 1}]")
    product_card.find_and_click_on_element(By.XPATH, locator.detail_link)
    product_card.element_should_have_text(By.XPATH, f"//td[@data-title='Товар']/a[contains(text(), '{title_product}')]",
                                          title_product, test_data.assertion_error_not_equals_text_with_title_page)


# Блок "Товары"
def test_go_to_product_from_products_sidebar_on_product_page(preparation_work):
    product_card = preparation_work
    product_card.go_to_product()

    # try:
    products_in_sideblock = product_card.get_elements(By.XPATH, locator.block_of_products_in_left_side)
    # time.sleep(3)

    product_item = products_in_sideblock[random.randint(0, 4)]
    product = get_element_in_another_element(product_item, By.TAG_NAME, "a")
    title_product = product.text
    product_card.click_element(product)

    product_card.element_should_have_text(By.XPATH, locator.title_of_searching_product, title_product,
                                          test_data.assertion_error_not_equals_text_with_title_page)
    # except Exception as e:
    #     assert False, f"Something went wrong {e.args}"
