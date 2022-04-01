import inspect
import os
import random
import string
from functools import wraps
from typing import Iterable, Iterator

import allure
from _pytest.fixtures import SubRequest, FixtureRequest
from allure_commons.utils import func_parameters, represent
from pytest_bdd.parser import Step, Feature, ScenarioTemplate
from pytest_bdd.parsers import parse


def random_string(lenght=10):
    return "".join([random.choice(string.ascii_letters) for _ in range(lenght)])


def random_phone():
    return "".join([random.choice(string.digits) for _ in range(10)])


def random_email():
    return random_string() + "@" + random_string(5) + "." + random.choice(["com", "ua", "org", "ru"])


class XHelper:

    @staticmethod
    def dummy(function):
        return function

    @staticmethod
    def parse_str_table(table_with_headers: str):
        list_table_rows = table_with_headers.split("\n")
        list_headers = str(list_table_rows[0]).strip("|").split("|")
        dict_table = {}
        for header in list_headers:
            header_text = header.strip()
            lst_row = []
            for i in range(1, list_table_rows.__len__()):
                list_temp = list_table_rows[i].strip("|").split("|")
                lst_row.append(list_temp[list_headers.index(header)].strip())

            dict_table[header_text] = lst_row

        return dict_table

    @staticmethod
    def iter(*args: Iterable):
        for i in args:
            yield from iter(i)


class Str:

    @classmethod
    def strip_split(cls, s: str, sep: str = None) -> Iterator[str]:
        yield from (s.strip() for s in s.split(sep=sep))

    @classmethod
    def strip_splits(cls, *s: str, sep: str = None) -> Iterator[Iterator[str]]:
        for s_ in s:
            yield cls.strip_split(s_, sep=sep)


class XAllure:
    PYTEST_SCENARIO_WRAPPER_KEY = '__scenario__'

    @staticmethod
    def get_step_with_type(request: FixtureRequest) -> str:
        step: Step = getattr(request, 'global_curr_step')
        return f'{step.keyword} {step.name}'

    @classmethod
    def step_screen(cls, step_definition: str):
        """
            Для скриншота обязательно в параметрах декорируемого action д.б. наследник CONFIG.WithBrowser
            Возможность скриншота проверяется здесь из-за особенностей обработки фикстуры сценария BDD
        :param step_definition:
        :return:
        """

        def decorator(action):
            @wraps(action)
            def wrapper(*args, **kwargs):
                return cls._step_wrapper(action, args, kwargs, step_definition)

                # kw = func_parameters(action, *args, **kwargs)
                # a = list(map(lambda x: represent(x), args))
                # with allure.step(step_keyword + step_definition.format(*a, **kw)):
                #     err = None
                #     try:
                #         return action(*args, **kwargs)
                #     except Exception as e:
                #         err = e
                #         raise
                #     finally:
                #         from conftest import CONFIG
                #         if err or CONFIG.ALWAYS_SCREEN:
                #             browsers: list[CONFIG.WithBrowser] = \
                #                 list(filter(
                #                     lambda x: isinstance(x, CONFIG.WithBrowser),
                #                     XHelper.iter(args, kwargs.values())))
                #
                #             browser = browsers[0].browser if browsers else None
                #
                #             if browser:
                #                 allure.attach(
                #                     body=browser.get_screenshot_as_png(),
                #                     name="screenshot_image",
                #                     attachment_type=allure.attachment_type.PNG)

            return wrapper
        return decorator

    @classmethod
    def step(cls, action):
        """
            Обязательно в параметрах декорируемого action д.б. фикстура request
            Возможность скриншота тоже проверяется здесь, так как
        :param action:
        :return:
        """

        @wraps(action)
        def wrapper(*args, **kwargs):
            args_orig, kwargs_orig = args, kwargs

            requests = list(filter(lambda x: isinstance(x, FixtureRequest), list(args) + list(kwargs.values())))
            assert requests, 'Обязательно в параметрах декорируемого action д.б. стандартная фикстура request'
            request: FixtureRequest = requests[0]
            step_definition = cls.get_step_with_type(request)

            return cls._step_wrapper(action, args, kwargs, step_definition)
            # __tracebackhide__ = True
            # params = func_parameters(action, *args, **kwargs)
            # args = list(map(lambda x: represent(x), args))
            # with allure.step(step_definition.format(*args, **params)):
            #     err = None
            #     try:
            #         return action(*args_orig, **kwargs_orig)
            #     except Exception as e:
            #         err = e
            #         raise
            #     finally:
            #         from conftest import CONFIG
            #         if err or CONFIG.ALWAYS_SCREEN:
            #             browsers: list[CONFIG.WithBrowser] = \
            #                 list(filter(
            #                     lambda x: isinstance(x, CONFIG.WithBrowser),
            #                     XHelper.iter(args, kwargs.values())))
            #
            #             browser = browsers[0].browser if browsers else None
            #
            #             if browser:
            #                 allure.attach(
            #                     body=browser.get_screenshot_as_png(),
            #                     name="screenshot_image",
            #                     attachment_type=allure.attachment_type.PNG)

        return wrapper

    @staticmethod
    def _step_wrapper(action, args, kwargs, step_definition):
        # kw = func_parameters(action, *args, **kwargs)
        # a = list(map(lambda x: represent(x), args))

        args_names = inspect.signature(action).parameters.keys()
        step_definition_ = step_definition
        for arg, val in tuple(zip(args_names, args)) + tuple(kwargs.items()):
            key = '{' + arg + '}'
            if key in step_definition:
                step_definition_ = step_definition_.replace(key, str(val))

        # with allure.step(step_definition.format(*a, **kw)):
        with allure.step(step_definition_):
            err = None
            try:
                return action(*args, **kwargs)
            except Exception as e:
                err = e
                raise
            finally:
                from conftest import CONFIG
                if err or CONFIG.ALWAYS_SCREEN:
                    browsers: list[CONFIG.WithBrowser] = \
                        list(filter(
                            lambda x: isinstance(x, CONFIG.WithBrowser),
                            XHelper.iter(args, kwargs.values())))

                    browser = browsers[0].browser if browsers else None

                    if browser:
                        allure.attach(
                            body=browser.get_screenshot_as_png(),
                            name="screenshot_image",
                            attachment_type=allure.attachment_type.PNG)

    @classmethod
    def steps(cls, *steps):
        res = []
        for step in steps:
            @step
            @cls.step
            def decorator(action):
                def wrapper(*args, **kwargs):
                    return action(*args, **kwargs)

                return wrapper

            res.append(decorator)
        return tuple(res)

    @classmethod
    def scenario(cls, action):
        scenario_: ScenarioTemplate = getattr(action, cls.PYTEST_SCENARIO_WRAPPER_KEY)
        feature_: Feature = scenario_.feature
        names = list(Str.strip_split(feature_.name, '/'))

        for decorator in (
                allure.feature(feature := names[0]),
                allure.story(story := feature if len(names) == 1 else names[1]),
                allure.title(title := scenario_.name),
                allure.parent_suite(feature),
                allure.suite(story),
                allure.sub_suite(title),
                allure.description(feature_.description),
        ):
            action = decorator(action)

        return XHelper.dummy(action)

    @classmethod
    def meta(cls, name, parents, params) -> type:
        """ __metaclass__ for BDD scenarios """
        res = type(name, parents, params)
        for key, val in filter(lambda x: hasattr(x[1], cls.PYTEST_SCENARIO_WRAPPER_KEY), res.__dict__.items()):
            val = cls.scenario(val)
            val = staticmethod(val)
            setattr(res, key, val)
        return res

    @classmethod
    def scenarios(cls):
        """ hack to call after pytest_bdd.scenarios  """

        from pytest_bdd.utils import get_caller_module_locals
        caller_locals = get_caller_module_locals()

        for test_name, v in filter(lambda x: hasattr(x[1], "__scenario__"), caller_locals.items()):
            caller_locals[test_name] = cls.scenario(v)

