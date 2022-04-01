import inspect
import logging
from typing import Optional, List, Iterable, Union

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from conftest import CONFIG
from libs.Wait import Wait
from libs.helpers import Str, XAllure


def screen_step(step_definition: str, exceptions: Iterable[type] = None):
    def decorator(action):
    #     args_names = inspect.signature(action).parameters.keys()
    #
    #     def wrapper(self: 'BasePage', *args, **kwargs):
    #         err = None
    #         step_definition_ = step_definition
    #         for arg, val in tuple(zip(args_names, (self, ) + args)) + tuple(kwargs.items()):
    #             key = '{' + arg + '}'
    #             if key in step_definition:
    #                 step_definition_ = step_definition_.replace(key, str(val))
    #
    #         with allure.step(step_definition_):
    #             try:
    #                 return action(self, *args, **kwargs)
    #             except Exception as e:
    #                 err = e
    #                 if exceptions and isinstance(e, tuple(exceptions)):
    #                     raise AssertionError(e)
    #                 else:
    #                     raise
    #             finally:
    #                 if err or CONFIG.ALWAYS_SCREEN:
    #                     driver = self._driver
    #                     allure.attach(
    #                         body=driver.get_screenshot_as_png(),
    #                         name="screenshot_image",
    #                         attachment_type=allure.attachment_type.PNG)
    #
    #     return wrapper
        return action

    return decorator


# class wait_exception:
#
#     @classmethod
#     def Timeout(cls, msg: str):
#         def decorator(action):
#             args_names = inspect.signature(action).parameters.keys()
#
#             def wrapper(*args, **kwargs):
#                 try:
#                     return action(*args, **kwargs)
#                 except TimeoutException:
#                     msg_ = msg
#                     for arg, val in tuple(zip(args_names, args)) + tuple(kwargs.items()):
#                         key = '{' + arg + '}'
#                         if key in msg:
#                             msg_ = msg_.replace(key, str(val))
#
#                     raise AssertionError(msg_)
#
#             return wrapper
#
#         return decorator


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

    @screen_step('[{self}] Clicking element')
    def _click_element(self, element):
        self.logger.info(f'{self} => Clicking element')
        ActionChains(self._driver).pause(0.3).move_to_element(element).click().perform()

    @screen_step('[{self}] Typing "{val}"')
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
