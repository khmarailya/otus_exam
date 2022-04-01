from selenium.webdriver.remote.webelement import WebElement

from libs.locators import CSS, XPATH
from libs.page_object.BasePage import BasePage, BasePageElement, BasePageElements


class Menu(BasePage):
    """ menu находится на каждой странице магазина """

    SELF = BasePageElement(
        CSS().body.descendant.id('menu').res)
    BUTTONS = BasePageElements(
        CSS().classes('nav').child.li.child.a.res)

    def check_item_count(self, cnt):
        assert len(self.BUTTONS()) == cnt, 'Incorrect menu button count'

    def item_by_text(self, text: str) -> WebElement:
        if not (res := list(filter(lambda x: x.text == text, self.BUTTONS()))):
            raise AssertionError(f'Can\'t find menu item "{text}"')
        return res[0]

    def ref_item_by_text(self, text: str) -> WebElement:
        return self.verify_visible_element(XPATH().a.text(text).res)
