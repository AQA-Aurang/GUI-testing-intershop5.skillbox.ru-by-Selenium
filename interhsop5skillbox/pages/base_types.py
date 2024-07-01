from abc import ABC
from interhsop5skillbox.conftest import chrome_browser as chrome
from interhsop5skillbox.conftest import chrome_browser_long_timeout as chrome_lt


class BaseType(ABC):
    @property
    def get_driver(self):
        pass


class PageWithChromeBrowser(BaseType):
    def __init__(self, chrome):
        self._driver = chrome

    @property
    def get_driver(self):
        return self._driver


class PageWithChromeBrowserLongTimeout(BaseType):
    def __init__(self, chrome_lt):
        self._driver = chrome_lt

    @property
    def get_driver(self):
        return self._driver
