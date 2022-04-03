import allure

from libs.locators import XPATH, CSS
from libs.page_object.BasePage import BasePage, BasePageElement
from libs.xallure import XAllure


class AdminLoginForm(BasePage):
    SELF = BasePageElement(
        CSS().body.descendant.id('content').res)
    USER_LABEL = BasePageElement(
        XPATH().label.for_('input-username').res)
    USER_INPUT = BasePageElement(
        XPATH().input.name('username').res)
    PASSWORD_LABEL = BasePageElement(
        XPATH().label.for_('input-password').res)
    PASSWORD_INPUT = BasePageElement(
        XPATH().input.name('password').res)
    SUBMIT = BasePageElement(
        XPATH().button.type('submit').res)
    ALERT = BasePageElement(
        CSS().div.classes('alert').res)

    def login(self, user, password):
        with allure.step(f'Find user input and type "{user}"'):
            self.USER_LABEL()
            input_ = self.USER_INPUT()
            input_.clear()
            self._send_keys(input_, user)
        with allure.step(f'Find password input and type "{password}"'):
            self.PASSWORD_LABEL()
            input_ = self.PASSWORD_INPUT()
            input_.clear()
            self._send_keys(input_, password)

        with allure.step('Submit'):
            self.SUBMIT().click()

        self.re_ini()

    def assert_alert_text(self, txt: str):
        assert str(self.ALERT().text).startswith(txt), 'Incorrect Alert text'
