import inspect
from functools import wraps

import allure
from _pytest.fixtures import FixtureRequest
from pytest_bdd.parser import Step, Feature, ScenarioTemplate

from libs import XHelper, Str


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
            requests = list(filter(lambda x: isinstance(x, FixtureRequest), list(args) + list(kwargs.values())))
            assert requests, 'Обязательно в параметрах декорируемого action д.б. стандартная фикстура request'
            request: FixtureRequest = requests[0]
            step_definition = cls.get_step_with_type(request)

            return cls._step_wrapper(action, args, kwargs, step_definition)

        return wrapper

    @staticmethod
    def _step_wrapper(action, args, kwargs, step_definition):
        __tracebackhide__ = True
        args_names = inspect.signature(action).parameters.keys()
        step_definition_ = step_definition
        for arg, val in tuple(zip(args_names, args)) + tuple(kwargs.items()):
            key = '{' + arg + '}'
            if key in step_definition:
                step_definition_ = step_definition_.replace(key, str(val))

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
