import functools
import importlib
import importlib.util
import inspect
import re
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Optional

from driverlessai import _logging, _server


def ignore_unexpected_kwargs(func: Callable) -> Callable:
    """Ignores passed kwargs to a function that are not function parameters."""

    @functools.wraps(func)
    def _wrapper(*args: Any, **kwargs: Any) -> Any:
        function_params = inspect.signature(func).parameters.keys()
        filtered_kwargs = {}
        for k, v in kwargs.items():
            if k in function_params:
                filtered_kwargs[k] = v
            else:
                _logging.logger.debug(
                    f"Parameter '{k}={v}' is ignored from "
                    f"function '{func.__qualname__}'. {function_params}"
                )
        return func(*args, **filtered_kwargs)

    return _wrapper


def apply_decorator_to_methods(
    decorator: Callable,
    include_regex: Optional[str] = None,
    exclude_regex: Optional[str] = None,
) -> Callable:
    """
    Applies the given decorator to all methods in a class.

    Args:
        decorator: the decorator to be applied
        include_regex: regular expression that will be matched with method names and
            included if so
        exclude_regex: regular expression that will be matched with method named and
            excluded from applying the decorator
    """

    def _wrapper(cls: type) -> type:
        methods = inspect.getmembers(
            cls,
            predicate=lambda m: inspect.isfunction(m) and not inspect.isbuiltin(m),
        )
        if include_regex:
            include_pattern = re.compile(include_regex)
            methods = [i for i in methods if include_pattern.match(i[0])]
        if exclude_regex:
            exclude_pattern = re.compile(exclude_regex)
            methods = [i for i in methods if not exclude_pattern.match(i[0])]
        for name, fn in methods:
            _logging.logger.debug(
                f"Applying decorator '{decorator.__name__}' "
                f"to method '{cls.__name__}.{name}'."
            )
            setattr(cls, name, decorator(fn))
        return cls

    return _wrapper


H2OAI_CLIENT_MODEL_NAME = "h2oai_client"


def _load_module_from_path(module_name: str, module_path: Path) -> ModuleType:
    if not module_path.exists():
        raise ModuleNotFoundError(f"Module path '{module_name}' doesn't exists.")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if not spec:
        raise Exception(f"Couldn't load module '{module_name}' from '{module_path}'.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _patch_messages_classes(h2oai_client: ModuleType) -> None:
    messages_sub_module = h2oai_client.messages
    for name, cls in inspect.getmembers(messages_sub_module, predicate=inspect.isclass):
        setattr(
            messages_sub_module,
            name,
            apply_decorator_to_methods(
                ignore_unexpected_kwargs,
                include_regex="^__init__$",
            )(cls),
        )


def get_h2oai_client_module_for(version: str) -> ModuleType:
    """
    Returns the `h2oai_client` for a given Driverless AI server version.

    Args:
        version: Driverless AI server version

    Returns:
        The `h2oai_client` module.
    """
    if H2OAI_CLIENT_MODEL_NAME in sys.modules:
        _logging.logger.debug(f"Module '{H2OAI_CLIENT_MODEL_NAME}' is already loaded.")
        return sys.modules[H2OAI_CLIENT_MODEL_NAME]

    module_path = (
        Path(__file__).parent.absolute()
        / f"_{H2OAI_CLIENT_MODEL_NAME}_{version.replace('.', '_')}"
        / "__init__.py"
    )
    h2oai_client = _load_module_from_path(H2OAI_CLIENT_MODEL_NAME, module_path)
    _patch_messages_classes(h2oai_client)
    return h2oai_client


def get_h2oai_client_client_class(version: str) -> type:
    """
    Returns the `h2oai_client.Client` class for the given Driverless AI server version.

    Args:
        version: Driverless AI server version.

    Returns:
        The `h2oai_client.Client` class object.
    """
    h2oai_client = sys.modules.get(H2OAI_CLIENT_MODEL_NAME)
    if not h2oai_client:
        raise ModuleNotFoundError(f"Cannot find module '{H2OAI_CLIENT_MODEL_NAME}'.")

    Client = h2oai_client.protocol.Client
    if _server.Version(version) < "1.10.5":
        import json
        import requests

        RequestError = h2oai_client.protocol.RequestError
        RemoteError = h2oai_client.protocol.RemoteError

        @apply_decorator_to_methods(ignore_unexpected_kwargs, exclude_regex="^_+")
        class PatchedClient(Client):  # type: ignore
            def _request(self, method: str, params: dict) -> Any:
                self._cid = self._cid + 1  # type: ignore
                req = json.dumps(
                    dict(id=self._cid, method="api_" + method, params=params)
                )
                max_retires = 5
                for i in range(max_retires):
                    res = self._session.post(
                        self.address + "/rpc",
                        data=req,
                        headers=self._get_authorization_headers(),
                    )
                    if (not res.url.endswith("/rpc")) and ("login" in res.url):
                        # exponential backoff sleep time
                        sleep_time = 2 * (i + 1)
                        retry_message = (
                            f"RPC call to '{method}' responded with '{res.url}' URL "
                            f"and {res.status_code} status. "
                            f"Retrying ... {i + 1}/{max_retires}"
                        )
                        _logging.logger.debug(retry_message)
                        time.sleep(sleep_time)
                    else:
                        break
                try:
                    res.raise_for_status()
                except requests.HTTPError as e:
                    msg = f"Driverless AI server responded with {res.status_code}."
                    print(f"[ERROR] {msg}\n\n{res.content}")
                    raise RequestError(msg) from e

                try:
                    response = res.json()
                except json.JSONDecodeError as e:
                    msg = "Driverless AI server response is not a valid JSON."
                    print(f"[ERROR] {msg}\n\n{res.content}")
                    raise RequestError(msg) from e

                if "error" in response:
                    raise RemoteError(response["error"])

                return response["result"]

        return PatchedClient
    else:
        return apply_decorator_to_methods(
            ignore_unexpected_kwargs, exclude_regex="^_+"
        )(Client)
