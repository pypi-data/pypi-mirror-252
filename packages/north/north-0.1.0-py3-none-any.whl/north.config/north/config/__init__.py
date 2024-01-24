from __future__ import annotations

import logging
import os
from asyncio.log import logger
from collections import ChainMap
from enum import EnumType
from functools import partial
from logging.config import dictConfig
from types import GenericAlias
from typing import Callable, Iterable, Mapping, Sequence, Type, TypeVar, cast

import environ as _environ
from environ._environ_config import RAISE

from .constants import constants

_base_config = {"handlers": ["console"], "level": logging.ERROR, "propagate": False}
_info_config = ChainMap({"level": logging.INFO}, _base_config)
_debug_config = ChainMap({"level": logging.DEBUG}, _base_config)


def configure_logging():
    logging_config = {
        "version": 1,
        "formatters": {
            "f": {"format": "%(asctime)s %(levelname)-8s %(name)-20s -- %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "f",
                "level": logging.DEBUG,
            }
        },
        "loggers": {
            "": {"handlers": ["console"], "level": logging.DEBUG, "propagate": True},
            "aiohttp.access": _info_config,
            "aiohttp.client": _info_config,
            "aiohttp.internal": _info_config,
            "aiohttp.server": _info_config,
            "aiohttp.web": _info_config,
            "aiohttp.websocket": _info_config,
            "__main__": _info_config,
            "welovebot": _debug_config,
        },
        "remove_existing_loggers": True,
    }

    dictConfig(logging_config)

    try:
        import coloredlogs

        coloredlogs.install(level="DEBUG", logger=logging.getLogger())
    except ImportError:
        pass


T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def environ_config(prefix: str, **kwargs: object) -> Callable[[Type[T]], Type[T]]:
    """wrapper for the environ config"""
    app_prefix = os.environ.get(
        constants.WELOVEBOT_CONFIG_PREFIX_ENVVAR.value,
        constants.WELOVEBOT_CONFIG_PREFIX_DEFAULT.value,
    )
    return _environ.config(prefix=f"{app_prefix}_{prefix}".upper(), **kwargs)  # type: ignore


def _convert_number(value: str) -> int | float:
    if value.isdigit():
        return int(value)
    raise Exception("i dont do floats yet")


def _convert_int(value: str) -> int:
    if value.isdigit():
        return int(value)
    raise Exception("not an int")


def _convert_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    value = value.lower().strip("""'" \n""")
    if value in ("1", "true", "yes", "on"):
        return True
    if value in ("0", "false", "no", "off"):
        return False
    raise RuntimeError(f"bad value for bool: `{value}`")


def _var(
    converter: Callable[[str], T],
    default: T | None = None,
    name: str | None = None,
    help: str | None = None,
) -> T:
    _default = RAISE if default is None else default
    return cast(T, _environ.var(default=_default, name=name, converter=converter, help=help))  # type: ignore


def str_var(
    default: str | None = None, name: str | None = None, help: str | None = None
) -> str:
    return _var(default=default, name=name, converter=str, help=help)


def bool_var(
    default: bool | None = None, name: str | None = None, help: str | None = None
) -> bool:
    return _var(default=default, name=name, converter=_convert_bool, help=help)


def num_var(
    default: int | float | None = None, name: str | None = None, help: str | None = None
) -> int | float:
    return _var(default=default, name=name, converter=_convert_number, help=help)


def int_var(
    default: int | None = None, name: str | None = None, help: str | None = None
) -> int:
    return _var(default=default, name=name, converter=int, help=help)


def float_var(
    default: float | None = None, name: str | None = None, help: str | None = None
) -> float:
    return _var(default=default, name=name, converter=float, help=help)


def seq_var(
    t: Callable[[str], T],
    default: Sequence[T] | None = None,
    name: str | None = None,
    help: str | None = None,
    sep: str = ",",
) -> Sequence[T]:
    def converter(value: str | Sequence[T]) -> list[T]:
        if not isinstance(value, str) and isinstance(value, Iterable):
            return [_ for _ in value]
        if not value:
            return []
        return [t(_.strip()) for _ in value.split(sep)]

    return cast(
        list[T], _var(converter=converter, default=default, name=name, help=help)
    )


def dict_var(
    t_K: Callable[[str], K] = str,
    t_V: Callable[[str], V] = str,
    default: Mapping[K, V] | None = None,
    name: str | None = None,
    help: str | None = None,
    sep: str = ",",
    kv_sep: str = "=",
) -> Mapping[K, V]:
    def converter(value: str | Mapping[K, V]) -> Mapping[K, V]:
        if isinstance(value, Mapping):
            return value
        if not value:
            return {}
        return {
            t_K(k): t_V(v) for k, v in (kv.split(kv_sep, 1) for kv in value.split(sep))
        }

    return _var(converter=converter, default=default, name=name, help=help)


def str_seq_var(
    default: Sequence[str] | None = None,
    name: str | None = None,
    help: str | None = None,
) -> Sequence[str]:
    return seq_var(str, default=default, name=name, help=help)


def int_seq_var(
    default: Sequence[int] | None = None,
    name: str | None = None,
    help: str | None = None,
) -> Sequence[int]:
    return seq_var(int, default=default, name=name, help=help)


def kv_seq_var(
    val_t: Callable[[str], T],
    default: Sequence[tuple[str, T]] | None = None,
    name: str | None = None,
    help: str | None = None,
    sep: str = ",",
    kv_sep: str = "=",
) -> Sequence[tuple[str, T]]:
    def t(value: str) -> tuple[str, T]:
        assert (
            kv_sep in value
        ), f"'{kv_sep}' missing from '{value}', nothing to split on"
        key, val = value.split(kv_sep, 1)
        return (key, val_t(val))

    return seq_var(t, default=default, name=name, help=help, sep=sep)


def var(
    t: Type[T] | GenericAlias,
    default: T | Callable[[], T] | None = None,
    name: str | None = None,
    help: str | None = None,
    sep: str = ",",
    kv_sep: str = "=",
) -> T:
    if callable(default):
        default = default()

    kwargs = dict(default=default, name=name, help=help)
    matchtype = t() if t in (int, float, str, bool) else t

    match matchtype:  # type: ignore
        case bool():
            var_func = partial(bool_var, **kwargs)
        case str():
            var_func = partial(str_var, **kwargs)
        case int() if t is int:
            var_func = partial(int_var, **kwargs)
        case float() if t is float:
            var_func = partial(float_var, **kwargs)
        case GenericAlias() if 1 == len(t.__args__):
            var_func = partial(seq_var, t.__args__[0], sep=sep, **kwargs)
        case GenericAlias() if 2 == len(t.__args__):
            var_func = partial(
                dict_var, t.__args__[0], t.__args__[1], sep=sep, kv_sep=kv_sep, **kwargs
            )
        case EnumType():
            var_func = partial(_var, t, **kwargs)
        case _:  # type: ignore
            raise ValueError(f"no shortcut for type '{t}'")

    return cast(T, var_func())


class HasConfig:
    def __new__(cls: type[HasConfig]) -> HasConfig:
        new_cls = super().__new__(cls)

        prefix = (
            getattr(cls, "config_prefix", None)
            or getattr(cls.config, "prefix", None)
            or cls.config.__name__
        )
        new_cls.config = _environ.to_config(environ_config(prefix)(cls.config))

        logger.log(5, new_cls.config)
        return new_cls
