import pytest, time, random, re
import interhsop5skillbox.utilities as utilities
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

usernames = ["Faridun", "Ferdinand"]
passwords = ["ValayBalay", "ValaVala123'"]

@pytest.fixture(scope="module")
def driver(request):
    # options = ChromiumOptions()
    # options.add_argument("start-fullscreen")
    # wd = webdriver.Chrome(options=options)
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)

    # print("capabilities -", wd.capabilities)
    # return wd

    yield wd
    wd.quit()


# def test_example(driver):
#     driver.get("https://google.com/")
#     virtual_keyboard = driver.find_element(By.CLASS_NAME, "ly0Ckb")
#     virtual_keyboard.click()
#     space_key = driver.find_element(By.ID, "K32")
#     space_key.click()
#     virtual_keyboard.click()
#
#     element = driver.find_element(By.NAME, "q")
#     element.send_keys("webdriver")
#     element.submit() # также можно element.send_keys(Keys.ENTER)
#     WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))
    # driver.quit()

# _____________________________________________________________________________

# def login(driver):
#     # Нажать на ссылку "Войти" и пройти авторизацию
#     driver.find_element(By.LINK_TEXT, "Войти").click()
#     driver.find_element(By.ID, "username").send_keys(usernames[1])
#     driver.find_element(By.ID, "password").send_keys(passwords[1])
#     driver.find_element(By.NAME, "login").click()
#     WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт"))
#
#     return driver

# def login_with_data(driver, username, password):
#     driver.find_element(By.LINK_TEXT, "Войти").click()
#     driver.find_element(By.ID, "username").send_keys(username)
#     driver.find_element(By.ID, "password").send_keys(password)
#     driver.find_element(By.NAME, "login").click()
#     WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт"))
#
#     return driver

# def logout(driver):
#     driver.find_element(By.LINK_TEXT, "Выйти").click()

# def get_element(driver, by_what, prompt):
#     element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((by_what, prompt)))
#     return element

# ________________________________ ________________________________ ________________________________ ________________________________
# -- Ported and tested --
# def test_go_to_my_account_from_link_navbar(driver):
#     # Переход на сайт intershop3.skillbox.ru
#     driver.get("http://intershop3.skillbox.ru")
#
#     # Нажатие на ссылку "Мой аккаунт" в меню
#     my_account_link = driver.find_element(By.LINK_TEXT, "Мой аккаунт")
#     my_account_link.click()
#
#     # Ожидание загрузки страницы "Авторизация"
#     WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))
#
#     # Проверка заголовка на странице
#     header_in_logging_page = driver.find_element(By.CLASS_NAME, "post-title")
#     assert header_in_logging_page.text == "МОЙ АККАУНТ"


# -- Ported and tested --
# def test_go_to_my_account_from_login_link(driver):
#     driver.get("http://intershop3.skillbox.ru")
#
#     login_link = driver.find_element(By.LINK_TEXT, "Войти")
#     login_link.click()
#
#     WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))
#
#     header_in_logging_page = driver.find_element(By.CLASS_NAME, "post-title")
#     assert header_in_logging_page.text == "МОЙ АККАУНТ"


# -- Ported and tested --
# def test_go_to_my_account_from_footer_link(driver):
#     # Переход на сайт intershop3.skillbox.ru
#     driver.get("https://intershop3.skillbox.ru")
#
#     # Прокрутить страницу вниз до раздела "СТРАНИЦЫ САЙТА"
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#     # Нажатие на ссылку "Мой аккаунт" в разделе "СТРАНИЦЫ САЙТА"
#     my_account_link = driver.find_element(By.LINK_TEXT, "Мой аккаунт")
#     my_account_link.click()
#
#     # Ожидание загрузки страницы "Мой аккаунт -- Skillbox"
#     WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))
#
#     # Проверка заголовка на странице
#     header_in_logging_page = driver.find_element(By.CLASS_NAME, "post-title")
#     assert header_in_logging_page.text == "МОЙ АККАУНТ"


# -- Ported and tested --
# def test_go_to_orders_from_info_block_after_auth(driver):
#     driver.get("https://intershop3.skillbox.ru")
#     driver = login(driver)

#     driver.find_element(By.LINK_TEXT, "свои заказы").click()
#     header_in_logging_page = driver.find_element(By.CLASS_NAME, "post-title")
#     assert header_in_logging_page.text == "ЗАКАЗЫ"

#     logout(driver)


# -- Ported and tested --
# def test_go_to_orders_after_auth(driver):
#     driver.get("https://intershop3.skillbox.ru")
#     driver = login(driver)

#     driver.find_element(By.LINK_TEXT, "Заказы").click()
#     header_in_logging_page = driver.find_element(By.CLASS_NAME, "post-title")
#     assert header_in_logging_page.text == "ЗАКАЗЫ"

#     logout(driver)


# -- Ported and tested --
# def test_go_to_order_details(driver):
#     driver.get("https://intershop3.skillbox.ru")
#     driver = login(driver)
#
#     driver.find_element(By.LINK_TEXT, "Заказы").click()
#     WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))
#     element = driver.find_element(By.XPATH, "//div[@class='woocommerce-MyAccount-content']/div[2]")
#
#     try:
#         if element.is_displayed() and element.text.split("\n")[1] == "Заказов еще нет.":
#             # print("\nЗаказов нет")
#             assert element.text.split("\n")[1] == "Заказов еще нет."
#     except IndexError:
#         table_body_rows = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
#
#         if len(table_body_rows) > 0:
#             table_body_rows[0].find_element(By.LINK_TEXT, "Подробнее").click()
#             header_in_order_page = driver.find_element(By.CLASS_NAME, "post-title")
#             assert header_in_order_page.text.startswith("ORDER")
#
#     logout(driver)


def navigation_to_personal_details(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver = utilities.login(driver)

    driver.find_element(By.LINK_TEXT, "Данные аккаунта").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))

    expected_header = "ДАННЫЕ УЧЕТНОЙ ЗАПИСИ"
    actual_header = driver.find_element(By.CLASS_NAME, "post-title")

    return driver

def modify_one_field_in_account(driver, field_id, new_value):
    driver = navigation_to_personal_details(driver)

    # modifing second name
    field = driver.find_element(By.ID, field_id)
    field.clear()
    field.send_keys(new_value)

    # save modification
    driver.find_element(By.NAME, "save_account_details").click()

    # getting second name and check
    driver.find_element(By.LINK_TEXT, "Данные аккаунта").click()
    updated_field = driver.find_element(By.ID, field_id)
    updated_field = updated_field.get_attribute("value")
    utilities.logout(driver)

    return updated_field


# -- Ported and tested --
# def test_modify_name_in_account(driver):
#     new_name = "Faridun"
#     updated_name = modify_one_field_in_account(driver, "account_first_name", new_name)
#
#     assert updated_name == new_name, f"Expected updated name: {new_name}, Actual updated name: {updated_name}"


# -- Ported and tested --
# def test_modify_second_name_in_account(driver):
#     new_second_name = "Hushang-Mirzo"
#     updated_second_name = modify_one_field_in_account(driver, "account_last_name", new_second_name)
#
#     assert updated_second_name == new_second_name, f"Expected updated second name: {new_second_name}, Actual updated second name: {updated_second_name}"


# -- Ported and tested --
# def test_modify_showing_name_in_account(driver):
#     new_display_name = "Ferdinand Emperor of Austria"
#     updated_display_name = modify_one_field_in_account(driver, "account_display_name", new_display_name)
#
#     assert updated_display_name == new_display_name, f"Expected updated second name: {new_display_name}, Actual updated second name: {updated_display_name}"


# -- Ported and tested --
# def test_modify_email_in_account(driver):
#     new_email = "ValayBalay@mail.ru"
#     updated_email = modify_one_field_in_account(driver, "account_email", new_email)
#
#     assert updated_email == new_email, f"Expected updated second name: {new_email}, Actual updated second name: {updated_email}"


def change_password_fields(driver, current_pass, new_pass, repeat_new_pass):
    driver.find_element(By.ID, "password_current").send_keys(current_pass)
    driver.find_element(By.ID, "password_1").send_keys(new_pass)
    driver.find_element(By.ID, "password_2").send_keys(repeat_new_pass)
    driver.find_element(By.NAME, "save_account_details").click()

    return driver

# Revert old password
# def revert_password(driver, current_password):
#     driver = login_with_data(driver, usernames[1], current_password)
#
#     driver.find_element(By.LINK_TEXT, "Данные аккаунта").click()
#     WebDriverWait(driver, 10).until(EC.title_contains("Мой аккаунт — Skillbox"))
#
#     expected_header = "ДАННЫЕ УЧЕТНОЙ ЗАПИСИ"
#     actual_header = driver.find_element(By.CLASS_NAME, "post-title")
#
#     driver.find_element(By.ID, "password_current").send_keys(current_password)
#     driver.find_element(By.ID, "password_1").send_keys(passwords[1])
#     driver.find_element(By.ID, "password_2").send_keys(passwords[1])
#     driver.find_element(By.NAME, "save_account_details").click()
#
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-message")))
#     logout(driver)


# -- Ported and tested --
# def test_modify_password_in_account(driver):
#     new_password = "ValaVala123"
#     driver = navigation_to_personal_details(driver)
#     driver = change_password_fields(driver, passwords[1], new_password, new_password)
#
#     wait = WebDriverWait(driver, 10)
#     success_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-message")))
#     assert success_message.text == "Account details changed successfully.", "Password update failed"
#
#     logout(driver) # cause after update pass, service dont redirect on main page
#     login(driver)  # for check, auth with old pass
#
#     li_element = driver.find_element(By.XPATH, "//ul[@role='alert']//li[1]")
#
#     assert li_element.text == "Веденный пароль для пользователя Ferdinand неверный. Забыли пароль?", "Password update failed"
#     revert_password(driver, new_password)


# -- Ported and tested --
# def test_modify_password_without_current_pass(driver):
#     driver = navigation_to_personal_details(driver)
#
#     new_password = "ValaVala123"
#     driver = change_password_fields(driver, "", new_password, new_password)
#
#     wait = WebDriverWait(driver, 10)
#     error_message = wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@role='alert']//li[1]")))
#     assert error_message.text == "Введите пароль.", "Cannot save new password"


# -- Ported and tested --
# def test_mismatched_new_pass_with_repeat_new_pass_fields(driver):
#     new_password = "ValaVala123"
#     repeat_new_password = "ValaVala1234"
#     driver = change_password_fields(driver, passwords[1], new_password, repeat_new_password)
#
#     wait = WebDriverWait(driver, 10)
#     error_message = wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@role='alert']//li[1]")))
#     assert error_message.text == "Введенные пароли не совпадают.", "Cannot save new password"
#     logout(driver)


# -- Ported and tested --
# def test_logout_by_link_in_account(driver):
#     driver = navigation_to_personal_details(driver)
#
#     driver.find_element(By.XPATH, "//li[@class='woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--customer-logout']//a[1]").click()
#
#     wait = WebDriverWait(driver, 10)
#     success_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "post-title")))
#     assert success_message.text == "МОЙ АККАУНТ", "Cannot log out"


def get_sub_catalog_title(driver, element_text):
    while True:
        # Выполнять код в цикле
        element = driver.find_element(By.XPATH, f"//h4[text()='{element_text}']")

        # Проверка условия прерывания
        if element.is_displayed():
            sub_catalog1_title = element.text
            break

    return sub_catalog1_title


# -- Ported and tested --
# def test_go_to_sub_catalog_from_main_page(driver):
#     driver.get("https://intershop3.skillbox.ru")
#
#     # Checking 1st sub catalog
#     sub_catalog1 = driver.find_element(By.ID, "accesspress_storemo-2")
#     sub_catalog1_title = get_sub_catalog_title(driver, "Книги")
#
#     sub_catalog1.find_element(By.TAG_NAME, "a").click()
#     actual_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Книги']")))
#     assert actual_result.text == sub_catalog1_title, "Cannot redirect to 'Книги' sub catalog from main page"
#
#     driver.back()
#
#     # Checking 2nd sub catalog
#     sub_catalog2 = driver.find_element(By.ID,"accesspress_storemo-3")
#     sub_catalog2_title = get_sub_catalog_title(driver, "Планшеты")
#
#     sub_catalog2.find_element(By.TAG_NAME, "a").click()
#     actual_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Планшеты']")))
#     assert actual_result.text == sub_catalog2_title, "Cannot redirect to 'Планшеты' sub catalog from main page"
#
#     driver.back()
#
#     # Checking 3rd sub catalog
#     sub_catalog3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "accesspress_storemo-4")))
#     sub_catalog3.find_element(By.TAG_NAME, "a").click()
#
#     expected_result = "Фото/видео"
#     actual_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Фото/видео']")))
#     assert actual_result.text.upper() == expected_result.upper(), "Cannot redirect to 'Фото/видео' sub catalog"


# -- Ported and tested --
# def test_go_to_product_card_from_sale_block(driver):
#     driver.get("https://intershop3.skillbox.ru")
#
#     height = driver.execute_script("return window.innerHeight;")
#     driver.execute_script(f"window.scrollTo(0, {height * 0.95});")
#
#     wait = WebDriverWait(driver, 10)
#     product = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@data-slick-index='1']")))
#     product_title = product.find_element(By.TAG_NAME, "a").get_attribute("title")
#
#     product_img = driver.find_element(By.XPATH, f"//li[@data-slick-index='1']/div/a[@title='{product_title}']")
#     product_img.click()
#
#     wait = WebDriverWait(driver, 10)
#     expected_result = "ВСЕ ТОВАРЫ"
#     actual_result = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='entry-title ak-container']")))
#     assert actual_result.text == expected_result, "Cannot go to product card"


# -- Ported and tested --
# def test_go_to_product_card_from_new_arrivals_block(driver):
#     driver.get("https://intershop3.skillbox.ru")
#
#     height = driver.execute_script("return window.innerHeight;")
#     driver.execute_script(f"window.scrollTo(0, {height * 2.7});")
#
#     wait = WebDriverWait(driver, 10)
#     product = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='slick-track'])[3]/li[@data-slick-index='1']")))
#     product_title = product.find_element(By.TAG_NAME, "a").get_attribute("title")
#
#     product_img = driver.find_element(By.XPATH, f"(//div[@class='slick-track'])[3]/li[@data-slick-index='1']/div/a[@title='{product_title}']")
#     product_img.click()
#
#     wait = WebDriverWait(driver, 10)
#     expected_result = "ВСЕ ТОВАРЫ"
#     actual_result = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='entry-title ak-container']")))
#     assert actual_result.text == expected_result, "Cannot go to product card"


# -- Ported and tested --
# def test_go_to_product_card_from_viewed_products(driver):
#     driver.get("https://intershop3.skillbox.ru")
#
#     height = driver.execute_script("return window.innerHeight;")
#     driver.execute_script(f"window.scrollTo(0, {height * 0.95});")
#
#     wait = WebDriverWait(driver, 10)
#     product = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@data-slick-index='1']")))
#     product_title = product.find_element(By.TAG_NAME, "a").get_attribute("title")
#
#     product_img = driver.find_element(By.XPATH, f"//li[@data-slick-index='1']/div/a[@title='{product_title}']")
#     product_img.click()
#
#     wait = WebDriverWait(driver, 10)
#     expected_result = "ВСЕ ТОВАРЫ"
#     actual_result = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='entry-title ak-container']")))
#
#     if actual_result.text == expected_result:
#         driver.find_element(By.LINK_TEXT, "Главная").click()
#         height = driver.execute_script("return window.innerHeight;")
#         driver.execute_script(f"window.scrollTo(0, {height * 5.5});")
#
#         try:
#             viewed_products_block = driver.find_element(By.ID, "woocommerce_recently_viewed_products-2")
#             header_viewed_products = viewed_products_block.find_element(By.TAG_NAME, "h2")
#             viewed_product = viewed_products_block.find_element(By.TAG_NAME, "li")
#
#             if header_viewed_products.text == "Просмотренные товары".upper():
#                 viewed_product_title = viewed_product.find_element(By.TAG_NAME, "span").text
#                 viewed_product_title = viewed_product_title.replace("'", "’")
#
#                 if viewed_product_title == product_title:
#                     viewed_product.find_element(By.TAG_NAME, "a").click()
#
#                     wait = WebDriverWait(driver, 10)
#                     expected_result = "ВСЕ ТОВАРЫ"
#                     actual_result = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='entry-title ak-container']")))
#
#                     assert actual_result.text == expected_result, "Cannot redirect to viewed product"
#                     # print("Well done, success check go to viewed product")
#         except Exception as e:
#             print("Something went wrong -", e.args[0])


# -- Ported and tested --
# def test_go_to_catalog_of_product(driver):
#     driver.get("http://intershop3.skillbox.ru")
#
#     catalog = driver.find_element(By.LINK_TEXT, "КАТАЛОГ")
#     catalog_title = catalog.text
#     catalog.click()
#
#     wait = WebDriverWait(driver, 10)
#     header_title = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Каталог']")))
#
#     assert header_title.text == catalog_title, "Cannot redirect in catalog of products"


# -- Ported and tested --
# def test_go_to_sub_catalog_from_navbar(driver):
#     driver.get("https://intershop3.skillbox.ru")
#     dropdown_element = driver.find_element(By.XPATH, "(//li[@id='menu-item-46']//a)[1]")
#
#     action_chains = ActionChains(driver)
#     action_chains.move_to_element(dropdown_element).perform()
#     driver.find_element(By.XPATH, "//li[@id='menu-item-119']/a[1]").click()
#
#     wait = WebDriverWait(driver, 10)
#     success_message = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Бытовая техника']")))
#     assert success_message.text == "БЫТОВАЯ ТЕХНИКА", "Cannot go to sub catalog"


# -- Ported and tested --
# def test_go_to_category_of_product(driver):
#     test_go_to_catalog_of_product(driver)
#
#     driver.find_element(By.LINK_TEXT, "Без категории").click()
#     header_category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Без категории']")))
#     assert header_category.text == "Без категории".upper(), "Cannot redirect to non category chapter"
#
#     driver.back()
#
#     driver.find_element(By.LINK_TEXT, "Часы").click()
#     header_category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Часы']")))
#     assert header_category.text == "Часы".upper(), "Cannot redirect to watch chapter"
#
#     driver.back()
#
#     driver.find_element(By.LINK_TEXT, "Электроника").click()
#     header_category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Электроника']")))
#     assert header_category.text == "Электроника".upper(), "Cannot redirect to electronic chapter"


# -- Ported and tested --
# def test_select_another_variant_from_product_sorting(driver):
#     test_go_to_catalog_of_product(driver)
#     sorting_element = driver.find_element(By.NAME, "orderby")
#
#     action_chains = ActionChains(driver)
#     action_chains.move_to_element(sorting_element).click()
#
#     selected_item = sorting_element.find_element(By.XPATH, "//option[@value='popularity']")
#     selected_item_title = selected_item.text
#     selected_item.click()
#
#     default_item = driver.find_element(By.NAME, "orderby").find_element(By.XPATH, "//option[@selected='selected']")
#     assert selected_item_title == default_item.text, "Selected item not equal with default item"


# def change_slider(driver, pixel_offset, slider_xpath):
#     test_go_to_catalog_of_product(driver)
#
#     height = driver.execute_script("return window.innerHeight;")
#     driver.execute_script(f"window.scrollTo(0, {height * 1.5});")
#
#     filter_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "woocommerce_price_filter-2")))
#     slider = driver.find_element(By.XPATH, slider_xpath)
#
#     action = ActionChains(driver)
#     action.drag_and_drop_by_offset(slider, pixel_offset, 0).perform()
#     fixed_price_str = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='price_label']//span[1]"))).text
#     fixed_price = float(fixed_price_str[:-1])
#     driver.find_element(By.XPATH, "(//button[@type='submit'])[2]").click()
#
#     products = driver.find_elements(By.XPATH, "//ul[@class='products columns-4']/li")
#     for product in products:
#         price_element = product.find_element(By.XPATH, "(//span[@class='woocommerce-Price-amount amount']//bdi)[1]")
#         price_str = price_element.text[:-1].replace(",", ".")
#         price = float(price_str)
#         assert price >= fixed_price, "Products price is not equal"


# -- Ported and tested --
# def test_change_left_of_slider(driver):
#     change_slider(driver, 10, "(//span[contains(@class,'ui-slider-handle ui-state-default')])[1]")
#     change_slider(driver, 15, "(//span[contains(@class,'ui-slider-handle ui-state-default')])[1]")


# def test_change_right_of_slider(driver):
#     change_slider(driver, -20, "(//span[contains(@class,'ui-slider-handle ui-state-default')])[2]")
#     change_slider(driver, -25, "(//span[contains(@class,'ui-slider-handle ui-state-default')])[2]")

def get_price(driver, slider_xpath, price_xpath, offset):
    slider = utilities.get_element(driver, By.XPATH, slider_xpath)
    slider.click()
    action = ActionChains(driver)
    action.drag_and_drop_by_offset(slider, offset, 0).perform()
    fixed_price_str = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, price_xpath))).text
    return driver, float(fixed_price_str[:-1])


# -- Ported and tested --
# def test_move_both_sliders_in_price_filter(driver):
#     test_go_to_catalog_of_product(driver)
#
#     height = driver.execute_script("return window.innerHeight;")
#     driver.execute_script(f"window.scrollTo(0, {height * 1.5});")
#
#     slider_xpath1 = "//div[contains(@class,'price_slider ui-slider')]//span[1]"
#     price_xpath1 = "//div[@class='price_label']//span[1]"
#     driver, fixed_price1 = get_price(driver, slider_xpath1, price_xpath1, 15)
#
#     slider_xpath2 = "//div[contains(@class,'price_slider ui-slider')]//span[2]"
#     price_xpath2 = "//div[@class='price_label']//span[2]"
#     driver, fixed_price2 = get_price(driver, slider_xpath2, price_xpath2, -10)
#
#     get_element(driver, By.XPATH, "(//button[@type='submit'])[2]").click()
#     products = driver.find_elements(By.XPATH, "//ul[@class='products columns-4']/li")
#
#     for product in products:
#         price_element = product.find_element(By.XPATH, "(//span[@class='woocommerce-Price-amount amount']//bdi)[1]")
#         price_text = price_element.text.replace(",", ".")
#         price = float(price_text[:-1])  # Remove the last symbol and convert to float
#
#         assert fixed_price1 <= price <= fixed_price2, f"price {price} not between selected prices - 1st price {fixed_price1} and 2nd price {fixed_price2}"


# -- Ported and tested --
# def test_first_product_navigation(driver):
#     # Step 1: Launch the browser and navigate to the URL
#     test_go_to_catalog_of_product(driver)
#
#     # Step 2: Use WebDriverWait to check for the presence of the #products-grid element
#     wait = WebDriverWait(driver, 10)
#     products_grid = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "products.columns-4")))
#
#     # Step 3: Find all li elements within the #products-grid block
#     product_elements = products_grid.find_elements(By.TAG_NAME, "li")
#
#     # Step 4: Select the first element from the list and get his title
#     selected_product_title = product_elements[0].find_element(By.TAG_NAME, "h3").text
#     product_elements[0].find_element(By.TAG_NAME, "a").click()
#
#     # Step 5: Check for the presence of the #product-title element on the page
#     wait = WebDriverWait(driver, 10)
#     product_title = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='product_title entry-title']")))
#
#     # Expected Result: The product title of the selected product should be displayed on the page
#     assert product_title.text == selected_product_title, "Products title not the same"


# -- Ported and tested --
# def test_pagination_in_catalog(driver):
#     test_go_to_catalog_of_product(driver)
#
#     # Ждем загрузку страницы
#     time.sleep(2)
#
#     # Прокручиваем страницу до раздела пагинации
#     pagination_section = driver.find_element(By.XPATH, "//ul[@class='page-numbers']")
#     driver.execute_script("arguments[0].scrollIntoView();", pagination_section)
#
#     # Нажимаем на номер страницы, отличный от текущей
#     next_page_button = driver.find_element(By.XPATH, "(//a[@class='page-numbers'])[1]")
#     page_numb = next_page_button.text
#     # print("Номер страницы -", next_page_button.text)
#     next_page_button.click()
#
#     # Проверяем, что страница изменилась ли
#     new_page_number = driver.current_url.split('page/')[1].removesuffix("/")
#     assert new_page_number == page_numb, "Pagination page not equals"


def go_to_catalog_of_product(driver):
    driver.get("https://intershop5.skillbox.ru")

    catalog = driver.find_element(By.LINK_TEXT, "КАТАЛОГ")
    catalog_title = catalog.text
    catalog.click()

    wait = WebDriverWait(driver, 10)
    header_title = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Каталог']")))


# -- Ported and tested --
# def test_go_to_product_from_block_under_the_filter(driver):
#     go_to_catalog_of_product(driver)
#
#     products =  driver.find_elements(By.XPATH, "//ul[@class='product_list_widget']//li")
#     product = products[random.randint(0, 4)]
#     product_title = utilities.get_element(product, By.TAG_NAME, "span").text
#     product.find_element(By.TAG_NAME, "a").click()
#     prod_title_in_new_page = utilities.get_element(driver, By.XPATH, "//h1[@class='product_title entry-title']").text
#     prod_title_in_new_page = prod_title_in_new_page.replace("’", "'").replace("‘", "'")
#
#     assert prod_title_in_new_page == product_title, "Titles of products is not equals"


# -- Ported and tested --
# def test_go_to_product_from_search_field(driver):
#     search_product = "watch"
#     get_element(driver, By.XPATH, "(//input[@name='s'])[1]").send_keys(search_product)
#     get_element(driver, By.CLASS_NAME, "searchsubmit").click()
#
#     prod_title_in_search_output_page = get_element(driver, By.XPATH, "//h1[@class='entry-title ak-container']").text
#
#     assert search_product.upper() in prod_title_in_search_output_page, "Search prod not equals with product in search output page"


# -- Ported and tested --
# def test_upsize_count_buying_product(driver):
#     test_go_to_product_from_block_under_the_filter(driver)
#
#     try:
#         quantity_input = get_element(driver, By.NAME, "quantity")
#         quantity_input.clear()
#         quantity_input.send_keys("4")
#
#     except Exception as e:
#         assert 1 == 2, f"Dont find needed filed {e.args}"


# -- Ported and tested --
# def test_downsize_count_buying_product(driver):
#     test_go_to_product_from_block_under_the_filter(driver)
#
#     try:
#         quantity_input = get_element(driver, By.NAME, "quantity")
#         quantity_input.clear()
#         quantity_input.send_keys("0")
#
#     except Exception as e:
#         assert 1 == 2, f"Dont find needed filed {e.args}"


# -- Ported and tested --
# def test_add_product_to_cart(driver):
#     test_go_to_product_from_block_under_the_filter(driver)
#
#     try:
#         get_element(driver, By.NAME, "add-to-cart").click()
#         pop_up_button = get_element(driver, By.XPATH, "//a[@class='button wc-forward']")
#
#         assert pop_up_button.is_enabled() and pop_up_button.is_displayed(), "Can't added product in cart"
#     except Exception as e:
#         print(f"Something went wrong {e.args}")


# -- Ported and tested --
# def test_adding_more_items_than_are_in_stock(driver):
#     test_go_to_product_from_block_under_the_filter(driver)
#     print("текущая ссылка -", driver.current_url)
#
#     try:
#         product_in_stock = utilities.get_element(driver, By.XPATH, "//p[@class='stock in-stock']")
#         product_in_stock_count = int(re.findall(r"\d+", product_in_stock.text)[0])
#
#         quantity_field = utilities.get_element(driver, By.NAME, "quantity")
#         while True:
#             rand_num = random.randint(1, 40)
#
#             if rand_num > product_in_stock_count:
#                 break
#
#         quantity_field.send_keys(str(rand_num))
#         utilities.get_element(driver, By.NAME, "add-to-cart").click()
#         txt_in_alert = utilities.get_element(driver, By.XPATH, "//div[@role='alert']").text
#
#         product_count_in_alert = int(re.findall(r"\d+", txt_in_alert)[0])
#         time.sleep(2)
#
#         assert product_count_in_alert <= product_in_stock_count, f"desired number {product_count_in_alert} of items out of stock {product_in_stock_count}"
#     except Exception as e:
#         print(f"Something went wrong - {e.args[0]}")


# -- Ported and tested --
# def test_zoom_product_with_magnifying_glass_on_product_card(driver):
#     test_go_to_product_from_block_under_the_filter(driver)
#
#     try:
#         wait = WebDriverWait(driver, 10)
#         # lupa_icon = driver.find_element(By.CLASS_NAME, "woocommerce-product-gallery__trigger")
#         lupa_icon = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-product-gallery__trigger")))
#         lupa_icon.click()
#
#         wait = WebDriverWait(driver, 10)
#         zoom_window = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pswp__img")))
#
#         assert zoom_window.is_enabled(), "Cant using zoom tool"
#     except Exception as e:
#         print("Cannot find zoom element")


# -- Ported and tested --
# def test_leave_review_for_product(driver):
#     driver.get("http://intershop3.skillbox.ru")
#     driver = login(driver)
#
#     driver.find_element(By.LINK_TEXT, "Заказы").click()
#
#     # like a test we go in the next order page for get product with link
#     # driver.find_element(By.LINK_TEXT, "Next").click()
#
#     product_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//td[@data-title='Заказ']//a)[1]")))
#     product_link.click()
#
#     ordered_product = get_element(driver, By.XPATH, "//td[@class='woocommerce-table__product-name product-name']")
#
#     try:
#         ordered_product_link = ordered_product.find_element(By.TAG_NAME, "a")
#         ordered_product_link.click()
#
#         stars = driver.find_elements(By.CSS_SELECTOR, ".stars>span>a")
#         product_mark = random.randint(0, 4)
#         stars[product_mark].click()
#         review_field = driver.find_element(By.XPATH, "//textarea[@id='comment']")
#
#         match product_mark:
#             case 0:
#                 review_txt = "Не советую, мне не понравилось"
#             case 1:
#                 review_txt = "Так себе, можно найти по лучше за такую цену"
#             case 2:
#                 review_txt = "В целом всё норм, ничего плохого не могу сказать, получил то что заказывал"
#             case 3:
#                 review_txt = "Не плохая вешь, мне понравилось, однозначно могу посоветовать"
#             case 4:
#                 review_txt = "Берите не пожалейте, меня устраивает, уже который год пользуюсь"
#
#         review_field.send_keys(review_txt)
#         driver.find_element(By.CLASS_NAME, "submit").submit()
#         saved_review = get_element(driver, By.XPATH, f"//p[text()='{review_txt}']").text
#
#         assert saved_review == review_txt, "Review not sent"
#     except NoSuchElementException as missing_element:
#         assert False, "No such element on DOM"
#     except Exception as e:
#         print("Error -", e.args)


# -- Ported and tested --
# def test_go_to_catelog_subcatelog_in_sideblock_on_product_page(driver):
#     test_go_to_product_from_block_under_the_filter(driver)
#
#     gategories = driver.find_elements(By.XPATH, "//li[contains(@class,'cat-item')]//a")
#     gategory_link = gategories[random.randint(0, len(gategories)-1)]
#     title_category = gategory_link.text
#     gategory_link.click()
#
#     title_page = get_element(driver, By.XPATH, "//h1[@class='entry-title ak-container']").text
#
#     assert title_page.capitalize() == title_category, "Title selected category not equal title of page"


# -- Ported and tested --
# def test_go_to_product_from_related_products_on_product_page(driver):
#     test_go_to_product_from_block_under_the_filter(driver)
#
#     product_from_related_products = get_element(driver, By.XPATH, f"(//a[@class='collection_title']//h3)[{random.randint(1, 3)}]")
#     title_product = product_from_related_products.text
#     product_from_related_products.click()
#
#     title_page = get_element(driver, By.XPATH, "//h1[@class='product_title entry-title']")
#
#     assert title_page.text == title_product, "Titles of products is not equals"

def get_product_and_his_title(driver):
    if EC.visibility_of_element_located((By.XPATH, "//ul[@class='products columns-4']//li/div[2]")):
        products_card_footer = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='products columns-4']//li/div[2]")))
    else:
        return "Element not visible", driver

    for x in range(3):
        print("\nx -", x)
        product_card_footer = products_card_footer[x]
        title_product = product_card_footer.find_element(By.XPATH, "//a/h3").text
        button_to_add_cart = utilities.get_element(driver, By.XPATH, "//ul[@class='products columns-4']//li/div[2]/div/a")

        # print("button_to_add_cart -", button_to_add_cart.text)
        if button_to_add_cart.text.capitalize() == "В корзину":
            break

    return title_product, button_to_add_cart


# -- Ported and tested --
# def test_add_item_to_cart_from_related_products_on_product_page(driver):
#     test_go_to_product_from_block_under_the_filter(driver)
#     title_product, button_to_add_cart = get_product_and_his_title(driver)
#
#     if button_to_add_cart.text.capitalize() != "В корзину":
#         driver.refresh()
#         title_product, button_to_add_cart = get_product_and_his_title(driver)
#
#     button_to_add_cart.click()
#     button_to_add_cart2 = driver.find_element(By.XPATH, "//a[@title='Подробнее']")
#     button_to_add_cart2.click()
#
#     product_which_added_in_cart = get_element(driver, By.XPATH, "//td[@data-title='Товар']//a[1]").text
#
#     assert product_which_added_in_cart == title_product, "Titles of products not equals"


# -- Ported and tested --
# def test_go_to_product_from_products_sidebar_on_product_page(driver):
#     test_go_to_product_from_block_under_the_filter(driver)
#
#     products_in_sideblock = driver.find_elements(By.XPATH, "//ul[@class='product_list_widget']//li")
#     product = products_in_sideblock[random.randint(0,4)]
#     title_product = product.find_element(By.TAG_NAME, "a").text
#
#     product.find_element(By.TAG_NAME, "a").click()
#
#     prod_title_in_new_page = get_element(driver, By.XPATH, "//h1[@class='product_title entry-title']").text
#
#     assert prod_title_in_new_page == title_product, "Titles of products not equals"


def get_product_in_cart(driver):
    try:
        title_product_added_in_cart = utilities.get_element(driver, By.XPATH, "//td[@data-title='Товар']//a[1]").text

        return title_product_added_in_cart
    except TimeoutException as te:
        driver.refresh()
        get_product_in_cart(driver)


def go_to_product_from_block_under_the_filter(driver):
    go_to_catalog_of_product(driver)

    products =  driver.find_elements(By.XPATH, "//ul[@class='product_list_widget']//li")
    product = products[random.randint(0, 4)]
    product_title = utilities.get_element(product, By.TAG_NAME, "span").text
    product.find_element(By.TAG_NAME, "a").click()
    prod_title_in_new_page = utilities.get_element(driver, By.XPATH, "//h1[@class='product_title entry-title']").text
    prod_title_in_new_page = prod_title_in_new_page.replace("’", "'").replace("‘", "'")


def add_item_to_cart_from_related_products_on_product_page(driver):
    go_to_product_from_block_under_the_filter(driver)

    title_product, button_to_add_cart = get_product_and_his_title(driver)
    if title_product == "Element not visible":
        driver.get("https://intershop5.skillbox.ru")
        add_item_to_cart_from_related_products_on_product_page()

    if button_to_add_cart.text.capitalize() != "В корзину":
        driver.refresh()
        title_product, button_to_add_cart = get_product_and_his_title(driver)

    button_to_add_cart.click()
    button_to_add_cart2 = WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, "//a[@title='Подробнее']")))
    button_to_add_cart2.click()

    product_which_added_in_cart = get_product_in_cart(driver)

    return title_product


# def test_go_to_product_from_cart1(driver):
#     title_product = add_item_to_cart_from_related_products_on_product_page(driver)
#
#     driver.find_element(By.XPATH, "//img[@loading='lazy']").click()
#     prod_title_in_new_page = get_element(driver, By.XPATH, "//h1[@class='product_title entry-title']").text
#
#     assert prod_title_in_new_page == title_product, "Titles of products not equals"


# def test_go_to_product_from_cart2(driver):
#     title_product = add_item_to_cart_from_related_products_on_product_page(driver)
#
#     driver.find_element(By.XPATH, "//td[@data-title='Товар']//a[1]").click()
#     prod_title_in_new_page = get_element(driver, By.XPATH, "//h1[@class='product_title entry-title']").text
#
#     assert prod_title_in_new_page == title_product, "Titles of products not equals"


# def test_modify_count_of_prod_in_cart(driver):
#     add_item_to_cart_from_related_products_on_product_page(driver)
#
#     count_product_field = get_element(driver, By.XPATH, "//input[@inputmode='numeric']")
#     count_product_field.clear()
#     count_product_field.send_keys("2")
#
#     driver.find_element(By.NAME, "update_cart").click()


# def test_remove_product_added_in_cart(driver):
#     add_item_to_cart_from_related_products_on_product_page(driver)
#     driver.find_element(By.LINK_TEXT, "×").click()
#     alert_element = get_element(driver, By.XPATH, "//p[text()='Корзина пуста.']")
#
#     assert alert_element.text == "Корзина пуста.", "Cannot remove product from cart"


def remove_product_added_in_cart(driver):
    title_product = add_item_to_cart_from_related_products_on_product_page(driver)

    driver.find_element(By.LINK_TEXT, "×").click()
    return title_product

# def test_recovery_product_after_removing(driver):
#     removed_product = remove_product_added_in_cart(driver)
#
#     driver.find_element(By.LINK_TEXT, "Вернуть?").click()
#     recovery_product = get_element(driver, By.XPATH, "//td[@data-title='Товар']//a[1]").text
#
#     assert recovery_product == removed_product, "Deleted product does not match the recovered product"


def apply_coupon_on_cart_page(driver, coupon):
    coupon_field = driver.find_element(By.ID, "coupon_code")
    coupon_field.clear()
    coupon_field.send_keys(coupon)
    driver.find_element(By.NAME, "apply_coupon").click()

    alert_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[text()[normalize-space()='Купон успешно добавлен.']]")))

    return alert_element.text


# def test_apply_promo_code_on_cart_page(driver):
#     _ = add_item_to_cart_from_related_products_on_product_page(driver)
#     alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "GIVEMEHALYAVA")
#
#     if len(alert_of_apply_coupon) > 0:
#         print("\n" + alert_of_apply_coupon)
#         WebDriverWait(driver, 80).until_not(EC.presence_of_element_located((By.XPATH, "(//div[@class='blockUI blockOverlay'])[2]")))


# def test_apply_sertificate_on_cart_page(driver):
#     alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "SERT500")
#
#     if len(alert_of_apply_coupon) > 0:
#         print("\n" + alert_of_apply_coupon)
#         WebDriverWait(driver, 80).until_not(EC.presence_of_element_located((By.XPATH, "(//div[@class='blockUI blockOverlay'])[2]")))


# def test_apply_not_exist_coupon_on_cart_page(driver):
    # _ = add_item_to_cart_from_related_products_on_product_page(driver)
    # alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "Pedro-pedro-pedro_Pe")

    # if len(alert_of_apply_coupon) > 0 and alert_of_apply_coupon == "Coupon code applied successfully.":
    #     assert False, "Pedro-pedro-pedro_Pe does not exist"
    #     WebDriverWait(driver, 80).until_not(EC.presence_of_element_located((By.XPATH, "(//div[@class='blockUI blockOverlay'])[2]")))


def apply_promo_code_on_cart_page(driver):
    _ = add_item_to_cart_from_related_products_on_product_page(driver)
    alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "GIVEMEHALYAVA")

    if len(alert_of_apply_coupon) > 0:
        # print("\n" + alert_of_apply_coupon)
        WebDriverWait(driver, 80).until_not(EC.presence_of_element_located((By.XPATH, "(//div[@class='blockUI blockOverlay'])[2]")))


# def test_remove_applied_coupon(driver):
#     apply_promo_code_on_cart_page(driver)
#
#     driver.find_element(By.LINK_TEXT, "[Удалить]").click()
#
#     wait = WebDriverWait(driver, 10)
#     alert = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()[normalize-space()='Купон удален.']]")))
#
#     assert alert.text == "Купон удален.", "Cannot delete coupon"


def apply_coupon_on_checkout_page(driver, coupon):
    driver.find_element(By.ID, "coupon_code").send_keys(coupon)
    driver.find_element(By.NAME, "apply_coupon").click()

    alert_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[text()[normalize-space()='Купон успешно добавлен.']]")))

    return alert_element.text


# def test_apply_promo_code_on_checkout_page(driver):
#     driver.get("https://intershop5.skillbox.ru")
#     driver = login(driver)
#
#     _ = add_item_to_cart_from_related_products_on_product_page(driver)
#
#     driver.find_element(By.LINK_TEXT, "ОФОРМИТЬ ЗАКАЗ").click()
#     driver.find_element(By.LINK_TEXT, "Нажмите для ввода купона").click()
#
#     alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "GIVEMEHALYAVA")
#     if len(alert_of_apply_coupon) > 0:
#         print("\n" + alert_of_apply_coupon)
#
#         WebDriverWait(driver, 80).until_not(EC.presence_of_element_located((By.XPATH, "(//div[@class='blockUI blockOverlay'])[1]")))
#
#         assert alert_of_apply_coupon == "Купон успешно добавлен.", "Coupon was not applied"
#         time.sleep(5)


def remove_added_coupon(driver):
    height = driver.execute_script("return window.innerHeight;")
    driver.execute_script(f"window.scrollTo(0, {height * 2.2});")
    time.sleep(1)
    remove_link = driver.find_element(By.LINK_TEXT, "[Удалить]")
    remove_link.click()

    return driver


def test_apply_sert_on_checkout_page(driver):
    driver.get("https://intershop5.skillbox.ru")
    driver = utilities.login(driver)

    _ = add_item_to_cart_from_related_products_on_product_page(driver)
    driver.find_element(By.LINK_TEXT, "ОФОРМИТЬ ЗАКАЗ").click()

    try:
        if driver.find_element(By.LINK_TEXT, "[Удалить]"):
            driver = remove_added_coupon(driver)
    except NoSuchElementException as NoSuch:
        print("NoSuchElementException -", NoSuch.args)

    driver.find_element(By.LINK_TEXT, "Нажмите для ввода купона").click()
    alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "SERT500") # GIVEMEHALYAVA

    if len(alert_of_apply_coupon) > 0:
        print("\n" + alert_of_apply_coupon)
        WebDriverWait(driver, 80).until_not(EC.presence_of_element_located((By.XPATH, "(//div[@class='blockUI blockOverlay'])[1]")))

        # remove_added_coupon(driver)
        alert_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[text()[normalize-space()='Купон успешно добавлен.']]")))
        assert alert_element.text == "Купон успешно добавлен.", "Coupon was not applied"


    # driver.find_element(By.LINK_TEXT, "Нажмите для ввода купона").click()
    # alert_of_apply_coupon = apply_coupon_on_cart_page(driver, "GIVEMEHALYAVA")  # SERT500
    #
    # if len(alert_of_apply_coupon) > 0:
    #     print("\n" + alert_of_apply_coupon)
    #     WebDriverWait(driver, 80).until_not(
    #         EC.presence_of_element_located((By.XPATH, "(//div[@class='blockUI blockOverlay'])[1]")))
    #
    #     # remove_added_coupon(driver)
    #     alert_element = WebDriverWait(driver, 100).until(
    #         EC.presence_of_element_located((By.XPATH, "//div[text()[normalize-space()='Купон успешно добавлен.']]")))
    #     assert alert_element.text == "Купон успешно добавлен.", "Coupon was not applied"


# def test_remove_added_coupon(driver):
#     try:
#         if driver.find_element(By.LINK_TEXT, "[Удалить]"):
#             driver = remove_added_coupon(driver)
#     except NoSuchElementException as NoSuch:
#         print("NoSuchElementException -", NoSuch.args)
#
#     alert_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()[normalize-space()='Купон удален.']]")))
#
#     assert alert_element.text == "Купон удален.", "Coupon could not be deleted"


# def test_place_order_with_empty_mandatory_field(driver):
#     driver.find_element(By.ID, "billing_first_name").clear()
#     driver.find_element(By.ID, "place_order").click()
#
#     wait = WebDriverWait(driver, 10)
#     err_alert = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@data-id='billing_first_name']")))
#
#     assert err_alert.text == "Имя для выставления счета обязательное поле.", "We can order the product with empty name filed - its ERROR!"


# def test_place_order_with_some_empty_mandatory_fields(driver):
#     driver.find_element(By.ID, "billing_first_name").clear()
#     driver.find_element(By.ID, "billing_last_name").clear()
#     driver.find_element(By.ID, "billing_city").clear()
#
#     driver.find_element(By.ID, "place_order").click()
#     wait = WebDriverWait(driver, 10)
#     main_errs_alerts = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='woocommerce-error']/li")))
#
#     assert main_errs_alerts[0].text == "Имя для выставления счета обязательное поле." \
#            and main_errs_alerts[1].text == "Фамилия для выставления счета обязательное поле." \
#            and main_errs_alerts[2].text == "Город / Населенный пункт для выставления счета обязательное поле.", \
#         "We can order the product with empty name filed - its ERROR!"


# def test_place_order_via_direct_bank_transfer(driver):
#     li_elements = driver.find_elements(By.XPATH, "//div[@id='payment']/ul[1]/li")
#
#     for item in li_elements:
#         label = item.find_element(By.TAG_NAME, "label")
#         radio_button = item.find_element(By.TAG_NAME, "input")
#
#         if label.text == "Прямой банковский перевод" and radio_button.is_selected():
#             break
#         else:
#             direct_bank_transfer = driver.find_element(By.XPATH, "//div[@id='payment']/ul[1]/li[1]/input")
#             direct_bank_transfer.click()
#
#
#     driver.find_element(By.ID, "place_order").click()
#     created_order = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Заказ получен']")))
#
#     assert created_order.text == "Заказ получен", "Couldn't place the order"


# def test_place_order_via_payment_on_delivery(driver):
#     li_elements = driver.find_elements(By.XPATH, "//div[@id='payment']/ul[1]/li")
#
#     for item in li_elements:
#         label = item.find_element(By.TAG_NAME, "label")
#         radio_button = item.find_element(By.TAG_NAME, "input")
#
#         if label.text == "Оплата при доставке" and radio_button.is_selected():
#             break
#         else:
#             payment_on_delivery = driver.find_element(By.XPATH, "//div[@id='payment']/ul[1]/li[2]/input")
#             payment_on_delivery.click()
#
#     selected_item = driver.find_element(By.XPATH, "//div[@id='payment']/ul[1]/li[2]")
#     label = selected_item.find_element(By.TAG_NAME, "label")
#     radio_button = selected_item.find_element(By.TAG_NAME, "input")
#
#     if label.text == "Оплата при доставке" and radio_button.is_selected():
#         driver.find_element(By.ID, "place_order").click()
#         created_order = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Заказ получен']")))
#
#         assert created_order.text == "Заказ получен", "Couldn't place the order"
#     else:
#         assert False, "Couldn't place the order"