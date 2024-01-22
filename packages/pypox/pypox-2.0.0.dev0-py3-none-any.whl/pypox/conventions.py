"""
This module defines the conventions used in the pypox library for defining HTTP and websocket endpoints.

Classes:
    BaseConvention: Base class for conventions in the pypox library.
    HTTPConvention: Represents a convention for HTTP endpoints.
    WebsocketConvention: Represents a convention for websocket endpoints.
"""
from importlib.machinery import ModuleSpec
from inspect import iscoroutinefunction
import os
from types import ModuleType
from typing import Any
import importlib.util
from starlette.routing import Router, BaseRoute, Route, WebSocketRoute
from starlette.requests import Request
from starlette.responses import Response
from pypox.processor import (
    BaseProcessor,
    encode_request,
    decode_response,
    exception_response,
)


class BaseConvention:
    """
    Base class for conventions in the pypox library.

    Attributes:
        name (str): The name of the convention.
        type (str): The type of the convention.
        files (list[str]): The list of files associated with the convention.
        callable (str): The name of the callable function in the module.
        directory (str): The directory path where the convention is defined.

    Methods:
        __init__(self,
        processor_func: list[BaseProcessor] | None,
        name: str, type: str,
        files: list[str],
        callable: str,
        directory: str) -> None:
            Initializes a BaseConvention object.
        __call__(self) -> list[BaseRoute]:
            Calls the convention and returns a list of BaseRoute objects.
        processor(self, func) -> Any:
            Decorator function that wraps the callable function with additional processing logic.
    """

    def __init__(
        self,
        name: str,
        _type: str,
        files: dict[str, str],
        _callable: str,
        directory: str,
    ) -> None:
        self._name = name
        self._type = _type
        self._files: dict[str, str] = files
        self._callable = _callable
        self._directory = directory

    @property
    def name(self) -> str:
        """
        The name of the convention.
        """
        return self._name

    @property
    def type(self) -> str:
        """
        The type of the convention.
        """
        return self._type

    @property
    def files(self) -> dict[str, str]:
        """
        The list of files associated with the convention.
        """
        return self._files

    @property
    def callable(self) -> str:
        """
        The name of the callable function in the module.
        """
        return self._callable

    @property
    def directory(self) -> str:
        """
        The directory path where the convention is defined.
        """
        return self._directory

    def __call__(self, processor_list: list[BaseProcessor]) -> list[BaseRoute]:
        """
        Retrieves a list of BaseRoute objects based on the specified directory and files.

        Returns:
            A list of BaseRoute objects representing the routes defined in the specified directory and files.
        """
        router: list[BaseRoute] = []

        for root, _, files in os.walk(self.directory):
            for file in files:
                if file not in self.files:
                    continue
                module_name = file.split(".")[0]
                module_path = os.path.join(root, file)

                spec: ModuleSpec | None = importlib.util.spec_from_file_location(
                    module_name, module_path
                )
                if not spec:
                    continue
                module: ModuleType = importlib.util.module_from_spec(spec)
                if not spec.loader:
                    continue
                spec.loader.exec_module(module)
                if not hasattr(module, self.callable):
                    raise AttributeError("Callable not found in module")

                if self.type == "http":
                    router.append(
                        Route(
                            root.replace(self.directory, "")
                            .replace("\\", "/")
                            .replace("[", "{")
                            .replace("]", "}")
                            + "/",
                            self.processor(
                                getattr(module, self.callable), processor_list
                            ),
                            methods=[self.files[file].upper()],
                        )
                    )
                elif self.type == "websocket":
                    router.append(
                        WebSocketRoute(
                            root.replace(self.directory, "")
                            .replace("\\", "/")
                            .replace("[", "{")
                            .replace("]", "}")
                            + "/",
                            self.processor(
                                getattr(module, self.callable), processor_list
                            ),
                        )
                    )
        return router

    def processor(self, func, processor_list: list[BaseProcessor]) -> Any:
        """
        Decorator that wraps a function to be used as a processor.

        Args:
            func (Callable): The function to be wrapped.

        Returns:
            Callable: The wrapped function.

        """

        async def wrapper(request: Request):
            try:
                if iscoroutinefunction(func):
                    response = await func(
                        **(await encode_request(request, func, processor_list))
                    )
                else:
                    response = func(
                        **(await encode_request(request, func, processor_list))
                    )
                return await decode_response(request, response, processor_list)
            except Exception as e:
                response: Response | None = await exception_response(
                    request, e, processor_list
                )
                if not response:
                    raise e
                return response

        wrapper.__annotations__ = func.__annotations__
        return wrapper


class HTTPConvetion(BaseConvention):
    """Represents a convention for HTTP endpoints.

    Args:
        BaseConvention (type): The base convention class.

    Attributes:
        name (str): The name of the convention.
        protocol (str): The protocol used by the convention.
        files (List[str]): The list of files associated with the convention.
        endpoint_type (str): The type of endpoint.
        directory (str): The directory where the convention is defined.
    """

    def __init__(
        self,
        directory: str,
    ) -> None:
        super().__init__(
            "HTTPConvention",
            "http",
            {
                "get.py": "GET",
                "post.py": "POST",
                "put.py": "PUT",
                "delete.py": "DELETE",
                "patch.py": "PATCH",
                "head.py": "HEAD",
                "options.py": "OPTIONS",
            },
            "endpoint",
            directory,
        )


class WebsocketConvention(BaseConvention):
    """
    A class representing a websocket convention.

    Args:
        BaseConvention (type): The base convention class.

    Attributes:
        directory (str): The directory where the convention is located.

    """

    def __init__(
        self,
        directory: str,
    ) -> None:
        """
        Initializes a new instance of the WebsocketConvention class.

        Args:
            directory (str): The directory where the convention is located.

        """
        super().__init__(
            "WebsocketConvention",
            "websocket",
            {"websocket.py": "WEBSOCKET"},
            "endpoint",
            directory,
        )


class HTMXConvention(BaseConvention):
    """
    A class representing the HTMX convention.

    Args:
        BaseConvention (type): The base convention class.
    """

    def __init__(self, directory: str) -> None:
        super().__init__(
            "HTMXConvention",
            "http",
            {"htmx.py": "GET"},
            "endpoint",
            directory,
        )
