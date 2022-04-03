import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from libs.element.AdminLoginForm import AdminLoginForm
from libs.xallure import XAllure


@pytest.fixture()
def admin_login_form(current_page) -> AdminLoginForm:
    return AdminLoginForm(current_page)


scenarios('features/admin.feature')
XAllure.scenarios()


@given('I go to Admin login page', target_fixture='current_page')
@XAllure.step
def _(request, pages):
    return pages.p_admin()


@then(parsers.parse('I go to Dashboard page'))
@XAllure.step
def _(request, pages):
    pages.p_dashboard.assertion()


@then(parsers.parse('I stay on Admin login page'))
@XAllure.step
def _(request, pages):
    pages.p_admin.assertion()


@when(parsers.parse('I login as "{user}" with "{password}"'))
@XAllure.step
def _(request, admin_login_form, user, password):
    admin_login_form.login(user, password)


@then(parsers.parse('I see Alert "{txt}"'))
def _(request, txt, admin_login_form):
    admin_login_form.assert_alert_text(txt)


if __name__ == '__main__':
    # for launching all local scenarios
    pass
