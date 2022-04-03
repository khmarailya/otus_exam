"""
Примеры:
pytest -m "ui" --browser=chrome --executor=http://q.w.ru --bversion=86.0
E:/ПО/allure-2.14.0/bin/allure.bat generate allure-results --clean -o allure-report
allure open allure-report
"""
import logging
from datetime import datetime

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from _pytest.runner import CallInfo
from pytest_bdd.parser import Step
from selenium.webdriver.remote.webdriver import WebDriver

from libs.browser import Browser
from libs.config import CONFIG
from libs.page_object.BasePage import Pages


def pytest_addoption(parser: Parser):
    CONFIG.add_all_options(parser)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Function, call: CallInfo):
    """ https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536 """
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


def pytest_bdd_before_scenario(request, feature, scenario):
    setattr(request, CONFIG.__GLOBAL_CURR_SCENARIO__, scenario)


def pytest_bdd_before_step_call(request, feature, scenario, step: Step, step_func, step_func_args):
    setattr(request, CONFIG.__GLOBAL_CURR_STEP__, step)


@pytest.fixture(scope='session')
def self():
    """ Обманка для сокращения кода при использовании декораторов в тестовых классах BDD """
    pass


@pytest.fixture(scope='session')
def config(request: SubRequest) -> type[CONFIG]:
    CONFIG.get_all_options(request)
    CONFIG.__TEST_NAME__ = test_name = request.node.name

    logger = logging.getLogger(test_name)  # todo ???
    logger.addHandler(logging.FileHandler(f'{test_name}.log'))
    logger.setLevel(level=CONFIG.LOG_LEVEL())
    logger.info(f'Test {test_name} started: {datetime.now()}')

    return CONFIG


@pytest.fixture(scope='function')
def browser(request: SubRequest, config) -> WebDriver:
    driver = Browser.get_browser()
    setattr(request, 'driver', driver)
    return driver


@pytest.fixture(scope='session')
def url_main() -> str:
    return str.strip(CONFIG.URL(), '/')


@pytest.fixture(scope='session')
def url_main_https() -> str:
    return str.strip(CONFIG.URL_HTTPS(), '/')


@pytest.fixture(scope='function')
def pages(browser, url_main, url_main_https) -> Pages:
    return Pages(browser, url_main, url_main_https=url_main_https)


@pytest.fixture()
def current_page() -> WebDriver:
    pass


@pytest.fixture(autouse=True)
def run_around_tests(request, browser):
    yield
    # video for each test
    Browser.finalizer(browser, request)