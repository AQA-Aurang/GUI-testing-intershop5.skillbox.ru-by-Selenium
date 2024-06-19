import pytest, time
import interhsop5skillbox.utilities as utilities
import interhsop5skillbox.product_card as p_card
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


# from selenium.common.exceptions import ElementClickInterceptedException

@pytest.fixture(scope="module")
def driver():
    wd = webdriver.Chrome()
    wd.implicitly_wait(20)

    # Increase page load timeout to 40 seconds
    wd.set_page_load_timeout(40)

    # Increase JavaScript execution timeout to 20 seconds
    wd.set_script_timeout(20)

    yield wd
    wd.quit()


# -------------------------------------------------
# Страница оформления заказа

def go_to_product(driver):
    driver.get("https://intershop5.skillbox.ru")
    utilities.get_element_experimental(driver, By.XPATH, "(//li[@data-slick-index='0'])[1]/div/a").click()


def add_item_to_cart_from_related_products_on_product_page(driver):
    go_to_product(driver)

    while True:
        title_product, item_numb = p_card.get_product_and_his_title(driver)

        if title_product != "Element not visible" and title_product != "To cart not found":
            break

        driver.refresh()

    utilities.get_element(driver, By.XPATH,
                          f"//ul[@class='products columns-4']//li/div[2]/div/a[{item_numb + 1}]").click()
    utilities.get_element(driver, By.XPATH, "//a[@title='Подробнее']").click()

    return title_product


def apply_coupon_on_checkout_page(driver, coupon):
    coupon_field = utilities.get_element(driver, By.ID, "coupon_code")
    coupon_field.clear()
    coupon_field.send_keys(coupon)
    utilities.get_element(driver, By.NAME, "apply_coupon").click()

    alert_element = utilities.get_element(driver, By.XPATH,
                                          "//div[text()[normalize-space()='Купон успешно добавлен.']]")

    return alert_element.text


def test_apply_coupon_on_checkout_page(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver = utilities.login(driver)

    _ = add_item_to_cart_from_related_products_on_product_page(driver)
    utilities.get_element(driver, By.LINK_TEXT, "ОФОРМИТЬ ЗАКАЗ").click()
    utilities.get_element(driver, By.LINK_TEXT, "Нажмите для ввода купона").click()

    try:
        alert_of_apply_coupon = apply_coupon_on_checkout_page(driver, "GIVEMEHALYAVA")  # SERT500

        if len(alert_of_apply_coupon) > 0:
            print("\n" + alert_of_apply_coupon)

            # Wait when block overlay finishes his work
            utilities.get_element(driver, By.XPATH, "(//div[@class='blockUI blockOverlay'])[1]")
            assert alert_of_apply_coupon == "Купон успешно добавлен.", "Coupon was not applied"
    except TimeoutException:
        print("go in timeout exception")
        alert_duplicate_coupon = utilities.get_element(driver, By.XPATH, "//ul[@role='alert']//li[1]")

        if alert_duplicate_coupon.text == "Coupon code already applied! ":
            # print("Получили ошибку")
            coupons = utilities.get_elements_experimental(driver, By.XPATH, "//th[contains(text(), 'Скидка')]")

            for coupon in coupons:
                if "GIVEMEHALYAVA" in coupon.text:
                    row = utilities.get_element(coupon, By.XPATH, "./..")
                    row.find_element(By.CSS_SELECTOR, "td a").submit()
                    break

            # print("Уже удалили купон, будем по новой добавлять его")
            utilities.get_element(driver, By.LINK_TEXT, "Нажмите для ввода купона").click()
            alert_of_apply_coupon = apply_coupon_on_checkout_page(driver, "GIVEMEHALYAVA")  # SERT500

            # print("Проверяем добавилось ли")
            if len(alert_of_apply_coupon) > 0:
                print("\n" + alert_of_apply_coupon)

                # Wait when block overlay finishes his work
                utilities.get_element(driver, By.XPATH, "(//div[@class='blockUI blockOverlay'])[1]")
                assert alert_of_apply_coupon == "Купон успешно добавлен.", "Coupon was not applied"
                # print("Всё прошли")

    utilities.logout_experiment(driver)

    # try:
    #     coupons = utilities.get_elements_experimental(driver, By.XPATH, "//th[contains(text(), 'Скидка')]")
    #
    #     for coupon in coupons:
    #         if "GIVEMEHALYAVA" in coupon.text:
    #             row = utilities.get_element(coupon, By.XPATH, "./..")
    #             row.find_element(By.CSS_SELECTOR, "td a").submit()
    #             break
    #
    # except TimeoutException:
    #     utilities.get_element(driver, By.LINK_TEXT, "Нажмите для ввода купона").click()
    #     alert_of_apply_coupon = apply_coupon_on_checkout_page(driver, "GIVEMEHALYAVA")  # SERT500
    #
        # if len(alert_of_apply_coupon) > 0:
        #     print("\n" + alert_of_apply_coupon)
        #
        #     utilities.get_element(driver, By.XPATH, "(//div[@class='blockUI blockOverlay'])[1]")
        #     assert alert_of_apply_coupon == "Купон успешно добавлен.", "Coupon was not applied"

def prepare_checkout_page(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver = utilities.login(driver)

    add_item_to_cart_from_related_products_on_product_page(driver)
    utilities.get_element(driver, By.LINK_TEXT, "ОФОРМИТЬ ЗАКАЗ").click()

    try:
        coupons = utilities.get_elements(driver, By.XPATH, "//th[contains(text(), 'Скидка')]")

        for coupon in coupons:
            if "GIVEMEHALYAVA" in coupon.text:
                row = utilities.get_element(coupon, By.XPATH, "./..")
                row.find_element(By.CSS_SELECTOR, "td a").submit()
                break

    except TimeoutException:
        utilities.get_element(driver, By.LINK_TEXT, "Нажмите для ввода купона").click()
        alert_of_apply_coupon = apply_coupon_on_checkout_page(driver, "GIVEMEHALYAVA")  # SERT500

        if len(alert_of_apply_coupon) > 0:
            # print("\n" + alert_of_apply_coupon)

            utilities.get_element(driver, By.XPATH, "(//div[@class='blockUI blockOverlay'])[1]")
    return driver


def remove_added_coupon(driver):
    height = driver.execute_script("return window.innerHeight;")
    driver.execute_script(f"window.scrollTo(0, {height * 2.2});")
    remove_link = driver.find_element(By.LINK_TEXT, "[Удалить]")
    remove_link.click()

    return driver


def test_remove_added_coupon(driver):
    prepare_checkout_page(driver)

    try:
        if utilities.get_element(driver, By.LINK_TEXT, "[Удалить]"):
            driver = remove_added_coupon(driver)
    except NoSuchElementException as NoSuch:
        print("NoSuchElementException -", NoSuch.args)

    alert_element = utilities.get_element(driver, By.XPATH, "//div[text()[normalize-space()='Купон удален.']]")
    assert alert_element.text == "Купон удален.", "Coupon could not be deleted"

    utilities.logout_experiment(driver)

def add_product_to_cart_and_go_to_order_page(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver = utilities.login(driver)

    add_item_to_cart_from_related_products_on_product_page(driver)
    utilities.get_element(driver, By.LINK_TEXT, "ОФОРМИТЬ ЗАКАЗ").click()

    return driver


def test_place_order_with_empty_mandatory_field(driver):
    driver = add_product_to_cart_and_go_to_order_page(driver)

    utilities.get_element_lt(driver, By.ID, "billing_first_name").clear()
    utilities.get_element_lt(driver, By.ID, "place_order").submit()

    err_alert = utilities.get_element_lt(driver, By.XPATH, "//li[@data-id='billing_first_name']")

    assert err_alert.text == "Имя для выставления счета обязательное поле.", \
        "We can order the product with empty name filed - its ERROR!"
    utilities.logout_experiment(driver)


def overfilling_of_fields(driver):
    name = utilities.get_element(driver, By.ID, "billing_first_name")
    if len(name.text) == 0:
        name.send_keys("Faridun")

    last_name = utilities.get_element(driver, By.ID, "billing_last_name")
    if len(last_name.text) == 0:
        last_name.send_keys("Hushang-Mirzo")

    city = utilities.get_element(driver, By.ID, "billing_city")
    if len(city.text) == 0:
        city.send_keys("Tashkent")

    utilities.get_element_lt(driver, By.ID, "place_order").submit()


def test_place_order_with_some_empty_mandatory_fields(driver):
    driver = add_product_to_cart_and_go_to_order_page(driver)

    utilities.get_element(driver, By.ID, "billing_first_name").clear()
    utilities.get_element(driver, By.ID, "billing_last_name").clear()
    utilities.get_element(driver, By.ID, "billing_city").clear()

    utilities.get_element_lt(driver, By.ID, "place_order").submit()
    time.sleep(1)

    main_errs_alerts = utilities.get_elements_lt(driver, By.XPATH, "//ul[@class='woocommerce-error']/li")

    assert main_errs_alerts[0].text == "Имя для выставления счета обязательное поле." \
           and main_errs_alerts[1].text == "Фамилия для выставления счета обязательное поле." \
           and main_errs_alerts[2].text == "Город / Населенный пункт для выставления счета обязательное поле.", \
        "We can order the product with empty name filed - its ERROR!"
    overfilling_of_fields(driver)
    utilities.logout_experiment(driver)


# def test_place_order_via_direct_bank_transfer(driver):
#     driver = add_product_to_cart_and_go_to_order_page(driver)
#
#     # li_elements = utilities.get_elements(driver, By.XPATH, "//div[@id='payment']/ul[1]/li")
#     li_elements = utilities.get_elements_experimental(driver, By.XPATH, "//div[@id='payment']/ul[1]/li")
#
#     for li in li_elements:
#         label = utilities.get_element(li, By.TAG_NAME, "label")
#         radio_button = utilities.get_element(li, By.TAG_NAME, "input")
#
#         if label.text == "Прямой банковский перевод" and radio_button.is_selected():
#             break
#         else:
#             utilities.get_element(driver, By.XPATH, "//div[@id='payment']/ul[1]/li[1]/input").click()
#
#     time.sleep(2)
#     utilities.get_element_lt(driver, By.ID, "place_order").click()
#
#     created_order = utilities.get_element(driver, By.XPATH, "//h2[text()='Заказ получен']")
#     assert created_order.text == "Заказ получен", "Couldn't place the order"
#     utilities.logout_experiment(driver)


# def test_place_order_via_payment_on_delivery(driver):
#     driver = add_product_to_cart_and_go_to_order_page(driver)
#
#     # li_elements = utilities.get_elements(driver, By.XPATH, "//div[@id='payment']/ul[1]/li")
#     li_elements = utilities.get_elements_experimental(driver, By.XPATH, "//div[@id='payment']/ul[1]/li")
#
#     for li in li_elements:
#         print("li -", li)
#         label = li.find_element(By.TAG_NAME, "label")
#         # print("label -", label.text)
#         radio_button = li.find_element(By.TAG_NAME, "input")
#         # print("radio_button is selected -", radio_button.is_selected())
#
#         if label.text == "Оплата при доставке" and radio_button.is_selected():
#             break
#         else:
#             utilities.get_element(driver, By.XPATH, "//div[@id='payment']/ul[1]/li[2]/input").submit()
#
#             selected_item = utilities.get_element(driver, By.XPATH, "//div[@id='payment']/ul[1]/li[2]")
#             label = selected_item.find_element(By.TAG_NAME, "label")
#             radio_button = selected_item.find_element(By.TAG_NAME, "input")
#
#             if label.text == "Оплата при доставке" and radio_button.is_selected():
#                 utilities.get_element(driver, By.ID, "place_order").submit()
#
#                 created_order = utilities.get_element(driver, By.XPATH, "//h2[text()='Заказ получен']")
#                 assert created_order.text == "Заказ получен", "Couldn't place the order"
#
#     utilities.logout_experiment(driver)
