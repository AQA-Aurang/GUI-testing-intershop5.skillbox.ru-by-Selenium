import pytest
from selenium import webdriver


@pytest.fixture(scope="module")
def chrome_browser():
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)

    yield wd

    wd.quit()


# For ordering_page
@pytest.fixture(scope="module")
def chrome_browser_long_timeout():
    wd = webdriver.Chrome()
    wd.implicitly_wait(20)

    # Increase page load timeout to 40 seconds
    wd.set_page_load_timeout(40)

    # Increase JavaScript execution timeout to 20 seconds
    wd.set_script_timeout(20)

    yield wd

    wd.quit()
