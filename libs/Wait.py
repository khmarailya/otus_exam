from selenium.webdriver.support.wait import WebDriverWait


class Wait(WebDriverWait):
    """ my WebDriverWait """

    def __init__(self, driver, timeout=2, frequency=1):
        super().__init__(driver, timeout, poll_frequency=frequency)

    def until(self, method, message=''):
        try:
            return super().until(method, message=message)
        except Exception as e:
            raise AssertionError('Waiting is failed') from e

    def until_not(self, method, message=''):
        try:
            return super().until_not(method, message=message)
        except Exception as e:
            raise AssertionError('Waiting is failed') from e


if __name__ == '__main__':
    pass
