from typing import Iterator

from libs.locators import CSS, XPATH
from libs.page_object.BasePage import BasePage, BasePageElement


def _get_common_input(parent, *keys) -> Iterator[BasePageElement]:
    for key in keys:
        yield BasePageElement(XPATH().label.for_(key).res, parent)
        yield BasePageElement(CSS().input.id(key).res, parent)
        yield BasePageElement(CSS().input.id(key).neighbor.div.classes('text-danger').res, parent)


class RegisterPage(BasePage):
    CONTENT = BasePageElement(
        CSS().id('content').res)
    AGREE = BasePageElement(
        CSS().input.attr('name', 'agree').res, CONTENT)
    CONTINUE = BasePageElement(
        CSS().input.attr('value', 'Continue').res, CONTENT)

    INPUT_LABEL_FIRSTNAME, INPUT_FIRSTNAME, INPUT_FIRSTNAME_ALERT, \
        INPUT_LABEL_LASTNAME, INPUT_LASTNAME, INPUT_LASTNAME_ALERT, \
        INPUT_LABEL_EMAIL, INPUT_EMAIL, INPUT_EMAIL_ALERT, \
        INPUT_LABEL_TELEPHONE, INPUT_TELEPHONE, INPUT_TELEPHONE_ALERT, \
        INPUT_LABEL_PASSWORD, INPUT_PASSWORD, INPUT_PASSWORD_ALERT, \
        INPUT_LABEL_CONFIRM, INPUT_CONFIRM, INPUT_CONFIRM_ALERT = tuple(_get_common_input(
            CONTENT,
            'input-firstname',
            'input-lastname',
            'input-email',
            'input-telephone',
            'input-password',
            'input-confirm',
        ))


if __name__ == '__main__':
    pass
