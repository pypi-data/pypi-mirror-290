from typing import Any, Callable

import requests

from poetry_ycf_plugin import config


class PluginException(RuntimeError):
    def __str__(self) -> str:
        message = ''

        for arg in self.args:
            if isinstance(arg, requests.exceptions.RequestException):
                message += f'{type(arg).__name__} - {arg} - {arg.response.json()}; '

            elif isinstance(arg, BaseException):
                message += f'{type(arg).__name__} - {arg}; '

            else:
                message += f'{arg}; '

        return f'<b>{config.PLUGIN_NAME}</b>: {message}'


def plugin_exception_wrapper(func: Callable[..., Any]):
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)

        except PluginException as ex:
            raise ex

        except BaseException as ex:
            raise PluginException(ex) from ex

    return wrapper
