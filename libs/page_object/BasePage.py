import logging
from typing import Optional, List, Union

import allure
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from conftest import CONFIG
from libs.Wait import Wait
from libs.xallure import Str, XAllure


class BasePage(CONFIG.WithBrowser):
    SELF: 'BasePageElement' = None
    __NAME__: str = None

    def __init__(self, driver: WebDriver, self_verify=True):
        self._driver = driver
        self._self_verify = self_verify
        self.driver: Optional[WebDriver, WebElement] = None
        self._config_logger()

        self.__cache__: dict = {}
        self.re_ini()

    def get_cache(self, locator: tuple[str, str], parent=None, renew=False) -> WebElement:
        if renew or locator not in self.__cache__:
            self.__cache__[locator] = res = self.verify_visible_element(locator, parent=parent)
        else:
            res = self.__cache__[locator]
        return res

    def get_cache_all(self, locator: tuple[str, str], parent=None, renew=False) -> list[WebElement]:
        if renew or locator not in self.__cache__:
            self.__cache__[locator] = res = self.verify_visible_elements(locator, parent=parent)
        else:
            res = self.__cache__[locator]
        return res

    def scroll_in_view(self, element: WebElement):
        # ActionChains(self._driver).move_to_element(element).perform()  # - работает медленнее
        self._driver.execute_script("arguments[0].scrollIntoView(false);", element)  # - работает рывками

    @property
    def browser(self) -> WebDriver:
        return self._driver

    def get_driver(self) -> WebDriver:
        return self.driver if isinstance(self.driver, WebDriver) else self._driver

    def re_ini(self):
        self.driver = None
        self.driver = self.SELF(renew=True) if self._self_verify and self.SELF else self._driver
        self.__cache__.clear()

    def _config_logger(self):
        test_name = getattr(self._driver, CONFIG.KEY_TEST_NAME)
        log_level = getattr(self._driver, CONFIG.KEY_LOG_LEVEL)

        self.logger = logging.getLogger(str(self))
        self.logger.addHandler(logging.FileHandler(f"{test_name}.log"))
        self.logger.setLevel(level=log_level)

    def __str__(self):
        res = self.__NAME__ + ' ' if self.__NAME__ else ''
        res += str(self.SELF)
        return res

    def attach_locator(self, locator: tuple):
        res = ': '.join(self.SELF.locator) + ' > ' if self.SELF else ''
        allure.attach(
            res + ': '.join(locator),
            name='locator',
            attachment_type=allure.attachment_type.TEXT
        )

    @XAllure.step_screen('I find Web element')
    def verify_visible_element(self, locator: tuple, parent=None) -> WebElement:
        self.logger.info(f'{self} => Verifying visible element: {locator}')
        self.attach_locator(locator)
        el = Wait(parent or self.driver or self._driver).until(EC.visibility_of_element_located(locator))
        self.scroll_in_view(el)
        return el

    @XAllure.step_screen('I find Web elements')
    def verify_visible_elements(self, locator: tuple, parent=None) -> List[WebElement]:
        self.logger.info(f'{self} => Verifying visible elements: {locator}')
        self.attach_locator(locator)
        els = Wait(parent or self.driver or self._driver).until(EC.visibility_of_all_elements_located(locator))
        self.scroll_in_view(els[0])
        return els

    def _click_element(self, element):
        self.logger.info(f'{self} => Clicking element')
        ActionChains(self._driver).pause(0.3).move_to_element(element).click().perform()

    def _send_keys(self, element: WebElement, val: str):
        self.logger.info(f'{self} => Typing {val}')
        element.send_keys(val)

    @staticmethod
    def get_classes(element: WebElement) -> list[str]:
        return list(Str.strip_split(element.get_attribute('class')))

    @classmethod
    def cache(cls, action):
        key = action.__name__

        def wrapper(self: BasePage, *args, renew=False, **kwargs) -> WebElement:
            if renew or key not in self.__cache__:
                self.__cache__[key] = res = action(self, *args, renew=renew, **kwargs)
            else:
                res = self.__cache__[key]
            return res

        return wrapper


class BasePageElement:

    def __init__(self, locator: tuple[str, str], *parents: Union[tuple[str, str], 'BasePageElement', object]):
        self.result = self.base_page = None
        self.locator = locator
        if parents and isinstance(parents[0], BasePageElement):
            res = []
            for i in parents:
                res += [i.locator] + list(i.parent_locators)
            self.parent_locators = tuple(res)
        else:
            self.parent_locators = parents

    def __get__(self, base_page: BasePage, owner):
        self.base_page = base_page
        return self

    def __call__(self, renew=False) -> WebElement:
        self.result = self.base_page.get_cache(self.locator, parent=self._get_parent(self.base_page), renew=renew)
        return self.result

    def _get_parent(self, base_page: BasePage, renew=False) -> WebElement:
        parent = None
        for parent_locator in self.parent_locators:
            parent = base_page.get_cache(parent_locator, parent=parent, renew=renew)
        return parent


class BasePageElements(BasePageElement):

    def __call__(self, renew=False) -> list[WebElement]:
        self.result = self.base_page.get_cache_all(self.locator, parent=self._get_parent(self.base_page), renew=renew)
        return self.result


if __name__ == '__main__':
    pass
