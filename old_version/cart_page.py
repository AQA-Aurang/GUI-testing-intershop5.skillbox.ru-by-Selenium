import interhsop5skillbox.old_version.utilities as utilities
import interhsop5skillbox.old_version.product_card as p_card
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


# -------------------------------------------------
# Страница корзины

def get_product_in_cart(driver):
    try:
        title_product_added_in_cart = utilities.get_element(driver, By.XPATH, "//td[@data-title='Товар']//a[1]").text

        return title_product_added_in_cart
    except TimeoutException:
        driver.refresh()
        get_product_in_cart(driver)


def add_item_to_cart_from_related_products_on_product_page(driver):
    utilities.go_to_product(driver)

    while True:
        title_product, item_numb = p_card.get_product_and_his_title(driver)

        if title_product != "Element not visible" and title_product != "To cart not found":
            break

        driver.refresh()

    utilities.get_element(driver, By.XPATH,
                          f"//ul[@class='products columns-4']//li/div[2]/div/a[{item_numb + 1}]").click()
    utilities.get_element(driver, By.XPATH, "//a[@title='Подробнее']").click()

    return title_product


def test_go_to_product_from_cart1(driver):
    title_product = add_item_to_cart_from_related_products_on_product_page(driver)

    utilities.get_element(driver, By.XPATH, "//img[@loading='lazy']").click()
    prod_title_in_new_page = utilities.get_element_lt(driver, By.XPATH,
                                                      "//h1[@class='product_title entry-title']").text

    assert prod_title_in_new_page == title_product, "Titles of products not equals"


def test_go_to_product_from_cart2(driver):
    title_product = add_item_to_cart_from_related_products_on_product_page(driver)

    utilities.get_element(driver, By.XPATH,
                          f"//td[@data-title='Товар']/a[contains(text(), '{title_product}')]").click()
    prod_title_in_new_page = utilities.get_element_lt(driver, By.XPATH, "//h1[@class='product_title entry-title']").text

    assert prod_title_in_new_page == title_product, "Titles of products not equals"


def test_modify_count_of_prod_in_cart(driver):
    add_item_to_cart_from_related_products_on_product_page(driver)

    count_product_field = utilities.get_element(driver, By.XPATH, "//input[@inputmode='numeric']")
    count_product_field.clear()
    count_product_field.send_keys("6")

    utilities.get_element(driver, By.NAME, "apply_coupon").click()


def test_remove_product_added_in_cart(driver):
    title_product = add_item_to_cart_from_related_products_on_product_page(driver)

    removed_link_product = utilities.get_element(driver, By.LINK_TEXT, title_product)
    parent_tr_element = removed_link_product.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
    remove_icon = parent_tr_element.find_element(By.TAG_NAME, "td").find_element(By.TAG_NAME, "a")
    remove_icon.click()

    alert_element = utilities.get_element(driver, By.XPATH, "//div[@role='alert']")
    assert title_product in alert_element.text, "Cannot remove product from cart"


def remove_product_added_in_cart(driver):
    title_product = add_item_to_cart_from_related_products_on_product_page(driver)

    removed_link_product = utilities.get_element(driver, By.LINK_TEXT, title_product)
    parent_tr_element = removed_link_product.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
    remove_icon = parent_tr_element.find_element(By.TAG_NAME, "td").find_element(By.TAG_NAME, "a")
    remove_icon.click()
    return title_product


def test_recovery_product_after_removing(driver):
    removed_product = remove_product_added_in_cart(driver)

    driver.find_element(By.LINK_TEXT, "Вернуть?").click()
    recovery_product = utilities.get_element(driver, By.XPATH,
                                             f"//td[@data-title='Товар']/a[contains(text(), '{removed_product}')]").text

    assert recovery_product == removed_product, "Deleted product does not match the recovered product"


def apply_coupon_on_cart_page(driver, coupon, xpath_prompt):
    coupon_field = utilities.get_element(driver, By.ID, "coupon_code")
    coupon_field.clear()
    coupon_field.send_keys(coupon)
    utilities.get_element(driver, By.NAME, "apply_coupon").click()

    alert_element = utilities.get_element_lt(driver, By.XPATH, xpath_prompt)

    return alert_element.text


def test_apply_promo_code_on_cart_page(driver):
    _ = add_item_to_cart_from_related_products_on_product_page(driver)
    alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "GIVEMEHALYAVA", "//div[@role='alert']")

    if len(alert_of_apply_coupon) > 0:
        # print("\n" + alert_of_apply_coupon)
        utilities.get_element_lt(driver, By.XPATH, "(//div[@class='blockUI blockOverlay'])[2]")
        assert True


def test_apply_sertificate_on_cart_page(driver):
    _ = add_item_to_cart_from_related_products_on_product_page(driver)
    alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "SERT500", "//div[@role='alert']")

    if len(alert_of_apply_coupon) > 0:
        # print("\n" + alert_of_apply_coupon)
        utilities.get_element_lt(driver, By.XPATH, "(//div[@class='blockUI blockOverlay'])[2]")


def test_apply_not_exist_coupon_on_cart_page(driver):
    _ = add_item_to_cart_from_related_products_on_product_page(driver)
    alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "Pedro-pedro-pedro_Pe", "//ul[@role='alert']//li[1]")

    assert len(alert_of_apply_coupon) > 0 and alert_of_apply_coupon == "Неверный купон.", \
        "Pedro-pedro-pedro_Pe does not exist"


def apply_promo_code_on_cart_page(driver):
    try:
        alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "GIVEMEHALYAVA", "//div[@role='alert']")

        if len(alert_of_apply_coupon) > 0:
            utilities.get_element(driver, By.XPATH, "(//div[@class='blockUI blockOverlay'])[2]")

            return alert_of_apply_coupon
    except TimeoutException:
        return utilities.get_element(driver, By.XPATH, "//ul[@role='alert']//li[1]").text


def test_remove_applied_coupon(driver):
    _ = add_item_to_cart_from_related_products_on_product_page(driver)

    try:
        coupons = utilities.get_elements(driver, By.XPATH, "//th[contains(text(), 'Скидка')]")

        for coupon in coupons:
            if "GIVEMEHALYAVA" in coupon.text:
                row = utilities.get_element(coupon, By.XPATH, "./..")
                row.find_element(By.CSS_SELECTOR, "td a").click()

    except TimeoutException:
        alert_txt = apply_promo_code_on_cart_page(driver)

        if alert_txt == "Coupon code already applied!":
            utilities.get_element(driver, By.LINK_TEXT, "[Удалить]").click()

    alert = utilities.get_element(driver, By.XPATH, "//div[text()[normalize-space()='Купон удален.']]")
    assert alert.text == "Купон удален.", "Cannot delete coupon"
