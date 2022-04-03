from libs.locators import CSS, XPATH
from libs.page_object.BasePage import BasePage, BasePageElement


class Footer(BasePage):
    """
        footer
        находится на каждой странице магазина
    """

    SELF = BasePageElement(
        CSS().body.descendant.footer.res)

    CUSTOMER_SERVICE_PANEL = BasePageElement(
        XPATH().h5.text('Customer Service').parent.div.res)

    CONTACTS_BTN = BasePageElement(
        XPATH().a.text('Contact Us').res, CUSTOMER_SERVICE_PANEL)


if __name__ == '__main__':
    print(Footer.CONTACTS_BTN.locator)
