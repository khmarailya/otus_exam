import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from libs import XHelper
from libs.config import CONFIG
from libs.page_object.RegisterPage import RegisterPage
from libs.xallure import XAllure


@pytest.fixture()
def register_page(current_page) -> RegisterPage:
    return RegisterPage(current_page)


scenarios('features/user.feature')
XAllure.scenarios()


@given('I go to Register page', target_fixture='current_page')
@XAllure.step
def _(request, pages):
    return pages.p_register()


@then('I stay on Register page')
@XAllure.step
def _(request, pages):
    return pages.p_register.assertion()


@then(parsers.parse('I go to Success Register page'))
@XAllure.step
def _(request, pages):
    pages.p_success_register.assertion()


@when(parsers.parse('I set firstname "{val}"'))
@when(parsers.parse('I set lastname "{val}"'))
@XAllure.step
def _(request, register_page, val):
    if 'firstname' in (s := CONFIG.get_current_step(request).name):
        inp = register_page.INPUT_FIRSTNAME()
    elif 'lastname' in s:
        inp = register_page.INPUT_LASTNAME()
    else:
        raise AssertionError(f'Something is wrong with step name "{s}"')

    inp.clear()
    inp.send_keys(val)


@when(parsers.parse('I set random email'))
@when(parsers.parse('I set random phone'))
@XAllure.step
def _(request, register_page):
    if 'email' in (s := CONFIG.get_current_step(request).name):
        inp, val = register_page.INPUT_EMAIL(), XHelper.random_email()
    elif 'phone' in s:
        inp, val = register_page.INPUT_TELEPHONE(), XHelper.random_phone()
    else:
        raise AssertionError(f'Something is wrong with step name "{s}"')

    inp.clear()
    inp.send_keys(val)


@when(parsers.parse('I set password "{val}"'))
@when(parsers.parse('I set password with "{val}" chars'))
@XAllure.step
def _(request, register_page, val):
    if 'chars' in CONFIG.get_current_step(request).name:
        val = XHelper.random_string(int(val))

    inp = register_page.INPUT_PASSWORD()
    inp.clear()
    inp.send_keys(val)


@then(parsers.parse('I see password alert "{val}"'))
@XAllure.step
def _(request, register_page, val):
    assert register_page.INPUT_PASSWORD_ALERT().text == val, 'Wrong register alert'


@then(parsers.parse('I see confirm alert "{val}"'))
@XAllure.step
def _(request, register_page, val):
    assert register_page.INPUT_CONFIRM_ALERT().text == val, 'Wrong confirm alert'


@then(parsers.parse('I do not see password alert'))
@XAllure.step
def _(request, register_page):
    register_page.INPUT_PASSWORD_ALERT.assert_invisible()


@when(parsers.parse('I confirm password "{val}"'))
@XAllure.step
def _(request, register_page, val):
    register_page.INPUT_CONFIRM().send_keys(val)


@when(parsers.parse('I agree'))
@XAllure.step
def _(request, register_page):
    register_page.AGREE().click()


@when(parsers.parse('I continue'))
@XAllure.step
def _(request, register_page):
    register_page.CONTINUE().click()
    register_page.re_ini()


if __name__ == '__main__':
    # for launching all local scenarios
    pass
