from selenium.webdriver.remote.webelement import WebElement

from libs.locators import CSS, XPATH
from libs.page_object.BasePage import BasePage, BasePageElement, BasePageElements


class Top(BasePage):
    """
        #top
        находится на каждой странице магазина
    """

    SELF = BasePageElement(
        CSS().body.child.id('top').res)

    CURRENCY_GROUP_BTN = BasePageElement(
        CSS().id('form-currency').child.classes('btn-group').res)
    CURRENCY_TITLE = BasePageElement(
        CSS().button.classes('dropdown-toggle').child.strong.res,
        CURRENCY_GROUP_BTN)
    CURRENCY_PANEL = BasePageElement(
        CSS().classes('btn-group').child.ul.classes('dropdown-menu').res,
        CURRENCY_GROUP_BTN)
    CURRENCY_BTN = BasePageElements(
        CSS().button.classes('currency-select').res,
        CURRENCY_PANEL)

    CONTACTS = BasePageElement(
        XPATH().a.child.classes('fa-phone').ancestor.li.res)
    CONTACTS_BTN = BasePageElement(
        XPATH().child.a.res, CONTACTS)

    TOP_LINKS_PANEL = BasePageElement(
        CSS().id('top-links').res)
    CART_BTN = BasePageElement(
        CSS().a.title('Shopping Cart').res,
        TOP_LINKS_PANEL)

    def show_currency(self):
        btn = self.CURRENCY_GROUP_BTN()
        if 'open' not in self.get_classes(btn):
            self._click_element(btn)

    def currency_btn_by_text(self, text: str) -> WebElement:
        return list(filter(lambda x: x.text == text, self.CURRENCY_BTN()))[0]


if __name__ == '__main__':
    pass
