from typing import Iterator

from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from pytest_bdd.parser import Step, ScenarioTemplate


class Option:
    def __init__(self, name: str, *args, default=None, **kwargs):
        self.name = name
        self.value = default
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.value


class CONFIG:
    __TEST_NAME__ = ''
    __ALLURE_RESULTS__ = 'allure-results'
    __ALLURE_REPORT__ = 'allure-report'

    __GLOBAL_CURR_SCENARIO__ = 'global_curr_scenario'
    __GLOBAL_CURR_STEP__ = 'global_curr_step'

    __BROWSERS__ = ['chrome', 'firefox', 'opera']

    BROWSER = Option(
        '--browser',
        default=__BROWSERS__[0],
        action='store',
        choices=__BROWSERS__,
        help='Browser choice',
    )
    BROWSER_PATH = Option(
        '--browser_path',
        default='E:/MyApp/otus_exam/setup/_browsers/chromedriver.exe',
        action='store',
        help='Browser path',
    )
    HEADLESS = Option(
        '--headless',
        action='store_true',
        default=False,
        help='Run headless',
    )
    ALWAYS_SCREEN = Option(
        '--always_screen',
        action='store_true',
        default=False,
        help='Screenshots at any chance',
    )
    URL = Option(
        '--url',
        action='store',
        default='http://172.17.0.1:8080/',
        help='Main page',
    )
    URL_HTTPS = Option(
        '--url_https',
        action='store',
        default='https://172.17.0.1/',
        help='Main page with https',
    )
    BROWSER_CONSOLE_LOG = Option(
        '--browser_console_log',
        action="store_true",
        default=False,
        help='Console logs to files',
    )
    LOG_LEVEL = Option(
        '--log_level',
        action='store',
        choices=['DEBUG'],
        default='DEBUG',
        help='Log level')
    EXECUTOR = Option(
        '--executor',
        action='store',
        default='http://localhost')  # http://localhost
    EXECUTOR_PORT = Option(
        '--executor_port',
        action='store',
        default='8090')
    EXECUTOR_PORT_HUB = Option(
        '--executor_port_hub',
        action='store',
        default='4444')
    BROWSER_VERSION = Option(
        '--bversion',
        action='store',
        default='86.0')
    BROWSER_VNC = Option(
        '--vnc',
        action='store_true',
        default=True)
    LOGS = Option(
        '--logs',
        action='store_true',
        default=True)
    BROWSER_VIDEO = Option(
        '--video',
        action='store_true',
        default=True)

    @classmethod
    def _get_option_vars(cls) -> Iterator[tuple[str, Option]]:
        yield from filter(lambda x: isinstance(x[1], Option), vars(cls).items())

    @classmethod
    def add_all_options(cls, parser: Parser):
        for name, option in cls._get_option_vars():
            args = (option.name,) + option.args
            parser.addoption(*args, default=option.value, **option.kwargs)

    @classmethod
    def get_all_options(cls, request: SubRequest):
        for name, option in cls._get_option_vars():
            option.value = request.config.getoption(option.name, default=option.value)

    @classmethod
    def get_current_step(cls, request) -> Step:
        return getattr(request, cls.__GLOBAL_CURR_STEP__)

    @classmethod
    def get_current_scenario(cls, request) -> ScenarioTemplate:
        return getattr(request, cls.__GLOBAL_CURR_SCENARIO__)
