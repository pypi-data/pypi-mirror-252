import os
import typing as t
from contextvars import ContextVar
from types import TracebackType

from ellar.common.constants import ELLAR_CONFIG_MODULE
from ellar.common.logging import logger
from ellar.common.utils.functional import SimpleLazyObject, empty
from ellar.core import Config
from ellar.di import EllarInjector
from ellar.events import app_context_started_events, app_context_teardown_events

if t.TYPE_CHECKING:
    from ellar.app.main import App

app_context_var: ContextVar[
    t.Optional[t.Union["ApplicationContext", t.Any]]
] = ContextVar("ellar.app.context")
app_context_var.set(empty)


class ApplicationContext:
    """
    Provides Necessary Application Properties when running Ellar CLI commands and when serving request.

    """

    __slots__ = ("_injector", "_config", "_app")

    def __init__(self, config: Config, injector: EllarInjector, app: "App") -> None:
        assert isinstance(config, Config), "config must instance of Config"
        assert isinstance(
            injector, EllarInjector
        ), "injector must instance of EllarInjector"

        self._injector = injector
        self._config = config
        self._app = app

    @property
    def app(self) -> "App":
        return self._app

    @property
    def injector(self) -> EllarInjector:
        return self._injector

    @property
    def config(self) -> Config:
        return self._config

    async def __aenter__(self) -> "ApplicationContext":
        app_context = app_context_var.get(empty)
        if app_context is empty:
            # If app_context exist
            app_context_var.set(self)
            if current_config._wrapped is not empty:  # pragma: no cover
                # ensure current_config is in sync with running application context.
                current_config._wrapped = self.config
            app_context = self
            await app_context_started_events.run()
        return app_context  # type:ignore[return-value]

    async def __aexit__(
        self,
        exc_type: t.Optional[t.Any],
        exc_value: t.Optional[BaseException],
        tb: t.Optional[TracebackType],
    ) -> None:
        await app_context_teardown_events.run()
        app_context_var.set(empty)

        current_app._wrapped = empty  # type:ignore[attr-defined]
        current_injector._wrapped = empty  # type:ignore[attr-defined]
        current_config._wrapped = empty

    @classmethod
    def create(cls, app: "App") -> "ApplicationContext":
        return cls(app.config, app.injector, app)


def _get_current_app() -> "App":
    app_context = app_context_var.get(empty)
    if app_context is empty:
        raise RuntimeError("ApplicationContext is not available at this scope.")

    return app_context.app  # type:ignore[union-attr]


def _get_injector() -> EllarInjector:
    app_context = app_context_var.get(empty)
    if app_context is empty:
        raise RuntimeError("ApplicationContext is not available at this scope.")

    return app_context.injector  # type:ignore[union-attr]


def _get_application_config() -> Config:
    app_context = app_context_var.get(empty)
    if app_context is empty:
        config_module = os.environ.get(ELLAR_CONFIG_MODULE)
        if not config_module:
            logger.warning(
                "You are trying to access app config outside app context "
                "and %s is not specified. This may cause differences in config "
                "values with the app" % (ELLAR_CONFIG_MODULE,)
            )
        return Config(config_module=config_module)

    return app_context.config  # type:ignore[union-attr]


current_app: "App" = t.cast("App", SimpleLazyObject(func=_get_current_app))
current_injector: EllarInjector = t.cast(
    EllarInjector, SimpleLazyObject(func=_get_injector)
)
current_config: Config = t.cast(Config, SimpleLazyObject(func=_get_application_config))
