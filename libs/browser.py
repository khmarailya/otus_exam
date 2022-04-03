import logging
import time
from datetime import datetime

import allure
import requests
from _pytest.fixtures import SubRequest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver

from libs.config import CONFIG
from libs.xallure import XAllure


class Browser:
    class WithBrowser:

        @property
        def browser(self) -> WebDriver:
            raise NotImplementedError()

    @staticmethod
    def get_params():
        if (browser := CONFIG.BROWSER()) == 'firefox':
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

        if executor := CONFIG.EXECUTOR():
            driver_class = webdriver.Remote
            caps.update({
                "version": CONFIG.BROWSER_VERSION(),
                "enableVNC": CONFIG.BROWSER_VNC(),
                "enableVideo": CONFIG.BROWSER_VIDEO(),
                "enableLog": CONFIG.LOGS(),
                "sessionTimeout": "5m",
                "timeZone": "Europe/Moscow"
            })
            options.add_argument('--no-sandbox')
            params = dict(command_executor=f'{executor}:{CONFIG.EXECUTOR_PORT_HUB()}/wd/hub')
        else:
            params = dict(executable_path=CONFIG.BROWSER_PATH())

        caps.update({
            "acceptInsecureCerts": True
        })
        options.add_argument('--ignore-certificate-errors')
        return caps, options, driver_class, params

    @classmethod
    def get_browser(cls) -> WebDriver:
        caps, options, driver_class, params = Browser.get_params()
        if CONFIG.BROWSER_CONSOLE_LOG():
            caps['loggingPrefs'] = {'performance': 'ALL', 'browser': 'ALL', 'driver': 'ALL'}

        driver = driver_class(desired_capabilities=caps,
                              options=options,
                              **params)

        logger = logging.getLogger(CONFIG.__TEST_NAME__)

        if executor := CONFIG.EXECUTOR():
            logger.info(f'{executor}:{CONFIG.EXECUTOR_PORT()}/#/sessions/' + driver.session_id)

        logger.info(f'Browser {CONFIG.BROWSER()}: {driver.desired_capabilities}')

        driver.maximize_window()
        driver.implicitly_wait(5)
        driver.set_page_load_timeout(5)

        return driver

    @classmethod
    def wait_url_data(cls, url, timeout=10) -> requests.Response:
        while timeout:
            response = requests.get(url)
            if not response.ok:
                time.sleep(1)
                timeout -= 1
            else:
                return response

    @classmethod
    def fin_url(cls, url: str, content_key: str, name_pref: str, attachment_type, failed, timeout=10):
        if not (url_data := cls.wait_url_data(url, timeout=timeout)):
            return

        if (content := getattr(url_data, content_key)) and (failed or True):
            allure.attach(name=name_pref, body=content, attachment_type=attachment_type)

        if content:
            requests.delete(url=url)

    @classmethod
    def finalizer(cls, driver: WebDriver, request: SubRequest):
        if CONFIG.BROWSER_CONSOLE_LOG():
            # Логирование
            for key in (
                    'performance',  # производительности страницы
                    'browser',  # WARNINGS, ERRORS
                    'driver'  # Локальное - драйвер
            ):
                with open(f'{key}.log', 'w+') as f:
                    for line in driver.get_log(key):
                        f.write(f'{line}\n')

        # video change url to session id only after finishing session
        session_id = driver.session_id
        driver.quit()
        # time.sleep(1)

        if executor := CONFIG.EXECUTOR():
            failed = request.session.testsfailed != 0
            executor_path = f'{executor}:{CONFIG.EXECUTOR_PORT()}'

            if CONFIG.BROWSER_VIDEO():
                cls.fin_url(
                    f'{executor_path}/video/{session_id}.mp4',
                    'content',
                    f'video_{session_id}',
                    allure.attachment_type.MP4,
                    failed,
                    timeout=10
                )

            if CONFIG.LOGS() and False:  # todo: deal with logs
                cls.fin_url(
                    f'{executor_path}/logs/{session_id}.log',
                    'text',
                    f'log_{session_id}',
                    allure.attachment_type.TEXT,
                    failed,
                    timeout=1
                )

        logger = logging.getLogger(test_name := CONFIG.__TEST_NAME__)
        logger.info(f'Test {test_name} finished: {datetime.now()}')
        logger.info(f'Report: (after generate) allure open {CONFIG.__ALLURE_REPORT__}')

        XAllure.add_environment()
