"""
    Применен хитрый костыл для уменьшение дублирования
"""
from typing import Optional

import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from libs.config import CONFIG
from libs.element.Footer import Footer
from libs.element.Header import Header
from libs.element.Menu import Menu
from libs.element.Top import Top
from libs.xallure import Str, XAllure

CURRENT_PAGE: tuple[Optional[str], Optional[WebDriver]] = (None, None)


@pytest.fixture()
def top(current_page) -> Top:
    return Top(current_page)


@pytest.fixture()
def header(current_page) -> Header:
    return Header(current_page)


@pytest.fixture()
def menu(current_page) -> Menu:
    return Menu(current_page)


@pytest.fixture()
def footer(current_page) -> Footer:
    return Footer(current_page)


@pytest.fixture()
def sub_item() -> WebElement:
    pass


scenarios('features')
XAllure.scenarios()


@given('I go to Main page', target_fixture='current_page')
@given('I go to Cart page', target_fixture='current_page')
@given('I go to Contacts page', target_fixture='current_page')
@XAllure.step
def _(request, pages):
    if 'Main' in (s := CONFIG.get_current_step(request).name):
        return pages.p_main()
    elif 'Cart' in s:
        return pages.p_cart()
    elif 'Contacts' in s:
        return pages.p_contacts()
    else:
        raise AssertionError(f'Something is wrong with step name "{s}"')


@then(parsers.parse('I see Currency in top'))
@XAllure.step
def _(request, top):
    top.CURRENCY_GROUP_BTN()


@then("I see Chopping Cart in top")
@XAllure.step
def _(request, top):
    top.CART_BTN()


@then("I see Contacts in top")
@XAllure.step
def _(request, top):
    top.CONTACTS()


@then("I see Cart button in header")
@XAllure.step
def _(request, header):
    header.CART()


@then("I see Search input in header")
@XAllure.step
def _(request, header):
    header.SEARCH()


@then("I see Logo in header")
@XAllure.step
def _(request, header):
    header.LOGO()


@then(parsers.parse('I see Menu with "{cnt}" items'))
@XAllure.step
def _(request, menu, cnt):
    menu.check_item_count(int(cnt))


@when(parsers.parse('I click on Menu item "{item}"'))
@XAllure.step
def _(request, menu, item):
    menu.item_by_text(item).click()


@then(parsers.parse('I see Menu sub item "{txt}"'), target_fixture='sub_item')
@XAllure.step
def _(request, menu, txt):
    return menu.ref_item_by_text(txt)


@when(parsers.parse('I click on Menu sub item'))
@XAllure.step
def _(request, sub_item):
    sub_item.click()


@then("I see Contacts in footer")
@XAllure.step
def _(request, footer):
    footer.CONTACTS_BTN()


@when("I open Currency menu")
@XAllure.step
def _(request, top):
    top.show_currency()


@when(parsers.parse('I choose "{text}" as Currency'))
@XAllure.step
def _(request, top, text):
    top.currency_btn_by_text(text).click()
    top.re_ini()


@then(parsers.parse("I see Currency list: {ls}"))
@XAllure.step
def _(request, top, ls: str):
    expected_btn_name_list = Str.strip_split(ls, ',')
    btn_name_list = list(btn.text for btn in top.CURRENCY_BTN())
    assert sorted(btn_name_list) == sorted(expected_btn_name_list), 'Wrong Currency list'


@then(parsers.parse('Currency has sign "{sign}"'))
@XAllure.step
def _(request, top, sign):
    assert top.CURRENCY_TITLE().text == sign, ''


@when('Cart is empty')
@XAllure.step
def _(request, header):
    pass


@when('I click on Cart')
@XAllure.step
def _(request, header):
    header.CART().click()


@when('I click on Chopping Cart')
@XAllure.step
def _(request, top):
    top.CART_BTN().click()


@when('I click on Contacts in top')
@XAllure.step
def _(request, top):
    top.CONTACTS_BTN().click()


@when('I click on Contacts in footer')
@XAllure.step
def _(request, footer):
    footer.CONTACTS_BTN().click()


@when('I click on Search button')
@XAllure.step
def _(request, header):
    header.SEARCH_BTN().click()


@when('I click on Logo')
@XAllure.step
def _(request, header):
    header.LOGO().click()


@then(parsers.parse('Cart has sign "{sign}"'))
@XAllure.step
def _(request, header, sign):
    header.check_cart_currency(sign)


@then(parsers.parse('I see Cart message "{msg}"'))
@XAllure.step
def _(request, header, msg):
    header.check_cart_menu_msg(msg)


@then(parsers.parse('I go to Main page'))
@then(parsers.parse('I go to Cart page'))
@then(parsers.parse('I go to Contacts page'))
@then(parsers.parse('I go to Search page'))
@XAllure.step
def _(request, pages):
    if 'Main' in (s := CONFIG.get_current_step(request).name):
        pages.p_main.assertion()
    elif 'Cart' in s:
        pages.p_cart.assertion()
    elif 'Contacts' in s:
        pages.p_contacts.assertion()
    elif 'Search' in s:
        pages.p_search.assertion()
    else:
        raise AssertionError(f'Something is wrong with step name "{s}"')


@then(parsers.parse('I go to Catalogue page "{title}"'))
@XAllure.step
def _(request, pages, title):
    if not (res := list(filter(lambda x: x[1] == title, pages.PARAMS['catalogue']))):
        raise AssertionError(f'Can\'t find page {title}')
    pages.assert_page(*res[0])


if __name__ == '__main__':
    # for launching all local scenarios
    pass
