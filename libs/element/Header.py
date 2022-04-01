from selenium.webdriver.common.by import By

from libs.locators import CSS
from libs.page_object.BasePage import BasePage, BasePageElement


class Header(BasePage):
    """ #header находится на большинстве странице магазина """

    SELF = BasePageElement(
        CSS().body.child.header.res)
    LOGO = BasePageElement(
        CSS().id('logo').res)

    CART = BasePageElement(
        CSS().id('cart').res)
    CART_MENU = BasePageElement(
        CSS().classes('dropdown-menu').res, CART)

    SEARCH = BasePageElement(
        CSS().id('search').res)
    SEARCH_INPUT = BasePageElement(
        (By.NAME, 'search'), SEARCH)
    SEARCH_BTN = BasePageElement(
        CSS().classes('input-group-btn').res, SEARCH)

    def check_logo_text(self):
        assert self.LOGO().text == 'Your Store', 'Incorrect Logo text'

    def check_cart_menu_msg(self, msg):
        assert self.CART_MENU().text == msg, 'Incorrect Cart message'

    def check_cart_currency(self, currency: str):
        assert currency in self.CART().text, 'Incorrect Cart text'

    def check_search(self):
        assert self.SEARCH_INPUT().get_attribute('placeholder') == 'Search', 'Incorrect placeholder'
