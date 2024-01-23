import json
import typing as t

from ellar.common.compatible import cached_property
from ellar.common.constants import TEMPLATE_FILTER_KEY, TEMPLATE_GLOBAL_KEY
from ellar.common.datastructures import URL
from ellar.common.templating import (
    Environment,
    JinjaLoader,
    JinjaTemplating,
    ModuleTemplating,
)
from ellar.common.types import ASGIApp
from ellar.core.conf import Config
from ellar.core.connection import Request
from ellar.di import EllarInjector
from jinja2 import Environment as BaseEnvironment
from starlette.templating import pass_context

if t.TYPE_CHECKING:
    from .main import App


class AppMixin(JinjaTemplating):
    _static_app: t.Optional[ASGIApp]
    _injector: EllarInjector
    _config: Config
    # rebuild_stack: t.Callable

    def get_module_loaders(self) -> t.Generator[ModuleTemplating, None, None]:
        for loader in self._injector.get_templating_modules().values():
            yield loader

    @property
    def debug(self) -> bool:
        return self._config.DEBUG

    @debug.setter
    def debug(self, value: bool) -> None:
        del self.__dict__["jinja_environment"]
        self._config.DEBUG = value
        # TODO: Add warning
        # self.rebuild_stack()

    @cached_property
    def jinja_environment(self) -> BaseEnvironment:  # type: ignore[override]
        _jinja_env = self._create_jinja_environment()
        self._update_jinja_env_filters(_jinja_env)
        return _jinja_env

    def _create_jinja_environment(self) -> Environment:
        def select_jinja_auto_escape(filename: str) -> bool:
            if filename is None:  # pragma: no cover
                return True
            return filename.endswith((".html", ".htm", ".xml", ".xhtml"))

        options_defaults: t.Dict = {
            "extensions": [],
            "auto_reload": self.debug,
            "autoescape": select_jinja_auto_escape,
        }
        jinja_options: t.Dict = t.cast(
            t.Dict, self._config.JINJA_TEMPLATES_OPTIONS or {}
        )

        for k, v in options_defaults.items():
            jinja_options.setdefault(k, v)

        @pass_context
        def url_for(context: dict, name: str, **path_params: t.Any) -> URL:
            request = t.cast(Request, context["request"])
            return request.url_for(name, **path_params)

        app: "App" = t.cast("App", self)

        jinja_env = Environment(app, **jinja_options)
        jinja_env.globals.update(
            url_for=url_for,
            config=self._config,
        )
        jinja_env.policies["json.dumps_function"] = json.dumps
        return jinja_env

    def create_global_jinja_loader(self) -> JinjaLoader:
        return JinjaLoader(t.cast("App", self))

    def _update_jinja_env_filters(self, jinja_environment: BaseEnvironment) -> None:
        jinja_environment.globals.update(self._config.get(TEMPLATE_GLOBAL_KEY, {}))
        jinja_environment.filters.update(self._config.get(TEMPLATE_FILTER_KEY, {}))
