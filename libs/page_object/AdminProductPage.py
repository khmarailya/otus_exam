import allure
from selenium.webdriver.support import expected_conditions as EC

from libs.Wait import Wait
from libs.element.AlertError import AlertError
from libs.locators import CSS, XPATH
from libs.page_object.BasePage import BasePage, BasePageElement, BasePageElements


class AdminProductPage(BasePage):
    ADD_BTN = BasePageElement(
        CSS().a.attr('data-original-title', 'Add New').res)
    SAVE_BTN = BasePageElement(
        CSS().button.attr('data-original-title', 'Save').res)
    DELETE_BTN = BasePageElement(
        CSS().button.attr('data-original-title', 'Delete').res)

    FORM_PRODUCT = BasePageElement(
        CSS().id('form-product').res)
    PRODUCT_LIST_CHECKBOXES = BasePageElements(
        CSS().id('form-product').descendant.tbody.descendant.input.attr('type', 'checkbox').res, FORM_PRODUCT)

    GENERAL_TAB = BasePageElement(
        XPATH().li.content('General').res, FORM_PRODUCT)
    GENERAL_TAB_CONTENT = BasePageElement(
        CSS().id('tab-general').res, FORM_PRODUCT)

    DATA_TAB = BasePageElement(
        XPATH().li.content('Data').res, FORM_PRODUCT)
    DATA_TAB_CONTENT = BasePageElement(
        CSS().id('tab-data').res, FORM_PRODUCT)

    PRODUCT_NAME_LABEL = XPATH().label.for_('input-name1').res
    PRODUCT_NAME_INPUT = CSS().input.id('input-name1').res

    PRODUCT_META_TAG_LABEL = XPATH().label.for_('input-meta-title1').res
    PRODUCT_META_TAG_INPUT = CSS().input.id('input-meta-title1').res

    USUAL_PRODUCT_INPUTS = {
        key: (XPATH().label.for_(val).res, CSS().input.id(val).res)
        for key, val in (
            ('name', 'input-name1'),
            ('meta_tag', 'input-meta-title1'),
            ('model', 'input-model'),
        )
    }

    def check_loaded(self):
        Wait(self.driver).until(EC.title_is('Products'))
        return self

    def _check_alert_and_accept(self, text: str):
        alert = self._driver.switch_to.alert
        assert alert.text == text, 'Incorrect alert text'
        alert.accept()

    def add_new(self):
        self.ADD_BTN().click()
        self.FORM_PRODUCT()

    def delete(self):
        self.DELETE_BTN().click()
        self._check_alert_and_accept('Are you sure?')
        AlertError(self.driver).check_have_no_permission()

    def save(self):
        self.SAVE_BTN().click()
        AlertError(self.driver).check_have_no_permission()

    def open_general(self):
        self.GENERAL_TAB().click()
        self.GENERAL_TAB_CONTENT()

    def open_data(self):
        self.DATA_TAB().click()
        self.DATA_TAB_CONTENT()

    def _set_usual_input(self, key: str, val: str, parent=None):
        label, input_ = self.USUAL_PRODUCT_INPUTS.get(key)
        self.verify_visible_element(label, parent=parent)
        self._send_keys(self.verify_visible_element(input_, parent=parent), val)

    def set_product_name(self, val: str):
        return self._set_usual_input('name', val, parent=self.GENERAL_TAB_CONTENT())

    def set_meta_tag(self, val: str):
        return self._set_usual_input('meta_tag', val, parent=self.GENERAL_TAB_CONTENT())

    def set_model(self, val: str):
        return self._set_usual_input('model', val, parent=self.DATA_TAB_CONTENT())

    def select(self, *indexes):
        checkboxes = self.PRODUCT_LIST_CHECKBOXES()
        for i in indexes:
            checkboxes[i].click()


if __name__ == '__main__':
    pass
