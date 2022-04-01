"""
Примеры:
pytest -m 'ui' --browser=chrome --executor=http://q.w.ru --bversion=86.0
E:/ПО/allure-2.14.0/bin/allure.bat generate allure-results --clean -o allure-report
allure open allure-report
"""
import json
import logging
import random
import time
from datetime import datetime

import allure
import pytest
import requests
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from _pytest.runner import CallInfo
from pytest_bdd.parser import Step
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from libs.Wait import Wait


class CONFIG:
    KEY_TEST_NAME = '__KEY_TEST_NAME__'
    KEY_LOG_LEVEL = '__KEY_LOG_LEVEL__'
    ALWAYS_SCREEN = True

    ALLURE_RESULTS = 'allure-results'
    ALLURE_REPORT = 'allure-report'

    PATH_TO_BROWSERS = 'E:/MyApp/otus_exam/setup/_browsers/'
    BROWSERS = {
        'chrome': PATH_TO_BROWSERS + 'chromedriver.exe',  # путь до хрома
        'firefox': PATH_TO_BROWSERS + 'geckodriver.exe',  # путь до лисы
        'opera': PATH_TO_BROWSERS + 'operadriver.exe',  # путь до оперы
    }

    @classmethod
    def driver_factory(cls, browser: str) -> WebDriver:
        if browser in cls.BROWSERS:
            path = cls.BROWSERS[browser]
            func = getattr(cls, browser)
            return func(path)

        raise Exception("Driver not supported")

    @staticmethod
    @allure.step("Get page {url}")
    def get_page(driver: WebDriver, url: str, title: str) -> WebDriver:
        driver.get(url)
        Wait(driver).until(EC.title_is(title))

        return driver

    class WithBrowser:

        @property
        def browser(self) -> WebDriver:
            raise NotImplementedError()


def pytest_addoption(parser: Parser):
    parser.addoption('--browser', action='store', choices=list(CONFIG.BROWSERS.keys()), default='chrome', type=str,
                     help='Browser choice', )
    parser.addoption('--headless', action='store_true', help='Run headless')
    parser.addoption('--url', action='store', help='Main page', default='http://localhost:8080/')
    parser.addoption('--browser_console_log', action="store_true", help='Console logs to files')
    parser.addoption('--log_level', action='store', choices=['DEBUG'], default='DEBUG', type=str, help='Log level')
    parser.addoption('--executor', action='store', default='')  # http://localhost
    parser.addoption('--bversion', action='store', default='')  # 86.0
    parser.addoption('--vnc', action='store_true', default=True)
    parser.addoption('--logs', action='store_true', default=True)
    parser.addoption('--video', action='store_true', default=False)


# https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Function, call: CallInfo):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'

    if rep.failed or CONFIG.ALWAYS_SCREEN:
        driver = None

        from libs.page_object.BasePage import BasePage
        pages: list[BasePage] = \
            list(filter(lambda x: isinstance(x, BasePage), item.funcargs.values()))

        if pages:
            driver = pages[0].get_driver()

        if driver:
            allure.attach(
                body=driver.get_screenshot_as_png(),
                name="screenshot_image",
                attachment_type=allure.attachment_type.PNG)

    # if rep.failed:
    #     try:
    #         if 'browser' in item.fixturenames:
    #             web_driver = item.funcargs['browser']
    #         else:
    #             print('Fail to take screen-shot')
    #             return
    #
    #         allure.attach(
    #             web_driver.get_screenshot_as_png(),
    #             name='screenshot',
    #             attachment_type=allure.attachment_type.PNG
    #         )
    #
    #     except Exception as e:
    #         print(f'Fail to take screen-shot: {e}')


@pytest.fixture(autouse=True)
def run_around_tests():
    pass
    yield
    pass


def pytest_bdd_before_scenario(request, feature, scenario):
    request.global_curr_scenario = scenario


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    pass


def pytest_bdd_before_step_call(request, feature, scenario, step: Step, step_func, step_func_args):
    request.global_curr_step = step


@allure.step("Waiting for resource availability {url}")
def wait_url_data(url, timeout=10) -> requests.Response:
    while timeout:
        response = requests.get(url)
        if not response.ok:
            time.sleep(1)
            timeout -= 1
        else:
            return response


@pytest.fixture(scope='session')
def self():
    """ Обманка для сокращения кода при использовании тестовых классов в BDD """
    pass


@pytest.fixture(scope='session')
def browser(request: SubRequest) -> WebDriver:
    test_name = request.node.name
    log_level = request.config.getoption("--log_level")
    console_log = request.config.getoption('--browser_console_log')

    logger = logging.getLogger('driver')
    logger.addHandler(logging.FileHandler(f'{test_name}.log'))
    logger.setLevel(level=log_level)
    logger.info(f'Test {test_name} started: {datetime.now()}')

    browser = request.config.getoption('--browser')
    executor = request.config.getoption('--executor')
    version = request.config.getoption('--bversion')
    video = request.config.getoption('--video')
    logs = request.config.getoption('--logs')

    if browser == 'firefox':
        caps = DesiredCapabilities.FIREFOX
        options = webdriver.FirefoxOptions()
        driver_class = webdriver.Firefox
    elif browser == 'chrome':
        caps = DesiredCapabilities.CHROME
        options = webdriver.ChromeOptions()
        driver_class = webdriver.Chrome
        options.add_experimental_option('w3c', False)
    elif browser == 'opera':
        from selenium.webdriver.opera.options import Options as OperaOptions
        options = OperaOptions()
        caps = DesiredCapabilities.OPERA
        driver_class = webdriver.Opera
    else:
        raise Exception('Incorrect browser')

    if console_log:
        caps['loggingPrefs'] = {'performance': 'ALL', 'browser': 'ALL', 'driver': 'ALL'}

    if executor:
        driver_class = webdriver.Remote
        caps.update({
            "version": version,
            "enableVNC": request.config.getoption('--vnc'),
            "enableVideo": video,
            "enableLog": logs,
            "sessionTimeout": "5m",
            "timeZone": "Europe/Moscow",
            "acceptInsecureCerts": True
        })
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        kwargs = dict(command_executor=f'{executor}:4444/wd/hub')
    else:
        kwargs = dict(executable_path=CONFIG.BROWSERS[browser])

    driver = driver_class(desired_capabilities=caps,
                          options=options,
                          **kwargs)

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities),
        attachment_type=allure.attachment_type.JSON)

    if executor:
        logger.info(f'{executor}:8090/#/sessions/' + driver.session_id)

    logger.info(f'Browser {browser}: {driver.desired_capabilities}')

    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(5)

    def fin():
        if console_log:
            # Логирование
            for key in (
                    'performance',  # производительности страницы
                    'browser',  # WARNINGS, ERRORS
                    'driver'  # Локальное - драйвер
            ):
                with open(f'{key}.log', 'w+') as f:
                    for line in driver.get_log(key):
                        f.write(f'{line}\n')

        if executor:
            failed = request.session.testsfailed != 0

            def fin_url(url: str, content_key: str, name_pref: str, attachment_type):
                url_data = wait_url_data(url)
                if not url_data:
                    return

                content = getattr(url_data, content_key)
                if failed and content:
                    allure.attach(name=name_pref + driver.session_id, body=content, attachment_type=attachment_type)
                if content:
                    requests.delete(url=url)

            if video:
                fin_url(f'http://{executor}:8080/video/{driver.session_id}.mp4', 'content', 'video_',
                        allure.attachment_type.MP4)

            if logs:
                fin_url(f'{executor}/logs/{driver.session_id}.log', 'text', 'log_', allure.attachment_type.TEXT)

        driver.quit()
        logger.info(f'Test {test_name} finished: {datetime.now()}')
        logger.info(f'Report: (after generate) allure open {CONFIG.ALLURE_REPORT}')

        # Add environment info to allure-report
        with open(f'{CONFIG.ALLURE_RESULTS}/environment.xml', 'w+') as file:
            s = '<environment>'

            def add_param(key, value):
                return f"""
                    <parameter>
                        <key>{key}</key>
                        <value>{value}</value>
                    </parameter>
                """

            s += add_param('Browser', browser)
            s += add_param('Browser.Version', version) if version else ''
            s += add_param('Executor', executor) if executor else ''
            s += '</environment>'
            file.write(s)

    request.addfinalizer(fin)

    setattr(driver, CONFIG.KEY_TEST_NAME, test_name)
    setattr(driver, CONFIG.KEY_LOG_LEVEL, log_level)
    setattr(request, 'driver', driver)
    return driver


@pytest.fixture(scope='session')
def url_main(request: SubRequest) -> str:
    return str.strip(request.config.getoption("--url"), '/')


class Pages(CONFIG.WithBrowser):
    PARAMS = {
        'main': ('index.php?route=common/home', 'Your Store'),
        'catalogue': [
            ('desktops', 'Desktops'),
            ('laptop-notebook', 'Laptops & Notebooks'),
            ('component', 'Components')
        ],
        'contacts': ('index.php?route=information/contact', 'Contact Us'),
        'cart': ('index.php?route=checkout/cart', 'Shopping Cart'),
        'search': ('index.php?route=product/search', 'Search')
    }

    # PARAMS_WITH_CURRENCY = PARAMS_MAIN + PARAMS_CATALOGUE + []
    # PARAMS_ALL = PARAMS_MAIN + PARAMS_CATALOGUE + []

    def __init__(self, browser, url_main):
        self.url_main = url_main
        self._browser = browser

    @property
    def params_all(self):
        for k, v in self.PARAMS:
            if isinstance(v, list):
                yield from iter(v)
            else:
                yield v

    @property
    def browser(self) -> WebDriver:
        return self._browser

    def __call__(self, path, title) -> WebDriver:
        url = self.get_url(path)
        if not self.check_url(url):
            self.browser.get(url)
            Wait(self.browser).until(EC.title_contains(title))

        return self.browser

    def random(self, params: list[tuple[str, str]] = None) -> WebDriver:
        return self(*random.choice(params or self.params_all))

    @property
    def pr_main(self):
        return self(*self.PARAMS['main'])

    def check_page(self, path: str, title: str):
        assert self.browser.current_url == f'{self.url_main}/{path}', ''
        Wait(self.browser).until(EC.title_contains(title))

    def check_path(self, path: str) -> bool:
        return self.check_url(self.get_url(path))

    def check_url(self, url: str) -> bool:
        return self.browser.current_url == url

    def get_url(self, path) -> str:
        return f'{self.url_main}/{path}'


@pytest.fixture(scope='session')
def pages(browser, url_main) -> Pages:
    return Pages(browser, url_main)


@pytest.fixture(scope='function')
def main_page(pages) -> WebDriver:
    return pages.pr_main


# @pytest.fixture(scope='session')
# def main_page(browser, url_main) -> WebDriver:
#     return CONFIG.get_page(browser, url_main, 'Your Store')


@pytest.fixture(scope='session')
def register_page(browser, url_main) -> WebDriver:
    return CONFIG.get_page(browser, url_main + '/index.php?route=account/register', 'Register Account')


@pytest.fixture(scope='session')
def admin_page(browser, url_main) -> WebDriver:
    return CONFIG.get_page(browser, url_main + '/admin', 'Administration')


@pytest.fixture(scope='function')
def admin_products_page(browser, url_main) -> WebDriver:
    return CONFIG.get_page(browser, url_main + '/admin/index.php?route=catalog/product', 'Administration')



@pytest.fixture(scope='session', params=Pages.PARAMS['catalogue'])
def catalogue_page(request: SubRequest, pages) -> WebDriver:
    return pages(*request.param)


@pytest.fixture(scope='session')
def catalogue_page(catalogue_page) -> WebDriver:
    return catalogue_page.random()
