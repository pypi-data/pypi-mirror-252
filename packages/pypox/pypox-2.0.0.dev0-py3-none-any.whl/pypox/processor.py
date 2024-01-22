"""
This module contains the implementation of various processors used in the pypox framework.
Processors are responsible for encoding and decoding data for API endpoints.

The module includes the following classes:
- BaseProcessor: The base class for processors that handle encoding and decoding of data.
- QueryProcessor: A processor for handling query parameters.
- PathProcessor: A processor for handling path parameters.
- JSONProcessor: A processor for handling JSON data.
- CookieProcessor: A processor for handling cookies.
- HeaderProcessor: A processor for handling headers.
- PydanticProcessor: A processor for handling Pydantic models.
- WebsocketProcessor: A processor for handling WebSocket connections.
- JinjaProcessor: A processor for rendering Jinja templates.

The module also includes helper functions for encoding and decoding data in API endpoints.
"""


from abc import abstractmethod
import inspect
from typing import Any, Callable, Mapping
from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.responses import (
    Response,
    JSONResponse,
    HTMLResponse,
    RedirectResponse,
    PlainTextResponse,
    StreamingResponse,
    FileResponse,
)
from starlette.requests import Request
from starlette.websockets import WebSocket
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

STARLETTE_RESPONSE = {
    Response,
    JSONResponse,
    HTMLResponse,
    RedirectResponse,
    PlainTextResponse,
    StreamingResponse,
    FileResponse,
}


class BaseProcessor:
    """
    Base class for processors that handle encoding and decoding of data.

    Args:
        types (list[type] | type): The types of data that the processor can handle.
            If a single type is provided, it will be converted to a list.
        response_class (type[Response] | None, optional): The response class to be used
            for decoding the response data. Defaults to None.

    Attributes:
        types (list[type]): The types of data that the processor can handle.
        response_class (type[Response] | None): The response class to be used for
            decoding the response data.
    """

    def __init__(
        self, types: list[type] | type, response_class: type[Response] | None = None
    ):
        if isinstance(types, type):
            types = [types]
        self.types = types
        self.response_class: type[Response] | None = response_class

    @abstractmethod
    async def encode(self, request: Request | WebSocket, name: str, annotation: type):
        """
        Transform the request data into usable endpoint data.

        Args:
            request (Request): The request object.
            name (str): The name of the data.
            annotation (type): The type annotation of the data.

        Returns:
            dict: A dictionary containing the name and the transformed data.
        """
        return None

    @abstractmethod
    async def decode(self, request: Request, response: Any):
        """
        Transform the response data into usable response data.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response: A response class that can be used by the starlette app.
        """
        if type(response) in STARLETTE_RESPONSE:
            return response
        if type(response) in [int, float, str, bool]:
            return Response(content=response)
        return None

    @abstractmethod
    async def exception(self, request: Request, exception: Exception):
        """
        Transform the exception data into usable response data.

        Args:
            request (Request): The request object.
            exception (Exception): The exception data.

        Returns:
            Response: A response class that can be used by the starlette app.
        """
        return None


class QueryProcessor(BaseProcessor):
    """
    Processor class for handling query parameters in requests.
    """

    def __init__(
        self,
        types: list[type] | None = None,
        response_class: type[Response] | None = None,
    ):
        if types is None:
            types = []
        super().__init__(types + [int, float, str, bool], response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """
        Encodes the query parameter value based on the provided annotation.

        Args:
            request (Request): The request object.
            name (str): The name of the query parameter.
            annotation (type): The type annotation of the query parameter.

        Returns:
            dict[str, Any] | None:
        """
        if annotation in self.types and name in request.query_params:
            return {name: annotation(request.query_params[name])}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        """
        Decodes the response data based on the provided annotation.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response | None: A response class that can be used by the starlette app.
        """
        return await super().decode(request, response)

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)


class PathProcessor(BaseProcessor):
    """
    A processor that extracts and encodes path parameters from a request.
    """

    def __init__(
        self,
        types: list[type] | None = None,
        response_class: type[Response] | None = None,
    ):
        if not types:
            types = []
        super().__init__([int, float, str, bool] + types, response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encode the request parameter with the given name and annotation.

        This method checks if the annotation is supported by the processor and if the
        parameter with the given name exists in the request's path parameters. If both
        conditions are met, it returns a dictionary containing the parameter name as the
        key and the converted value as the value. Otherwise, it returns None.

        Args:
            request (Request): The request object.
            name (str): The name of the parameter.
            annotation (type): The type annotation of the parameter.

        Returns:
            dict[str, Any] | None: A dictionary containing the parameter name and value,
            or None if the parameter is not found or the annotation is not supported.
        """
        if annotation in self.types and name in request.path_params:
            return {name: annotation(request.path_params[name])}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        """
        Decodes the response data based on the provided annotation.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response | None: A response class that can be used by the starlette app.
        """
        return await super().decode(request, response)

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)


class JSONProcessor(BaseProcessor):
    """
    A processor for handling JSON data.

    This processor is responsible for encoding and decoding JSON data.

    Args:
        BaseProcessor (type): The base processor class.

    Attributes:
        types (list[type]): A list of types that can be encoded/decoded.
        response_class (type[Response] | None): The response class to use for decoding.
    """

    def __init__(
        self,
        types: list[type] | None = None,
        response_class: type[Response] | None = JSONResponse,
    ) -> None:
        if not types:
            types = []
        super().__init__([list, dict] + types, response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encode the request data.

        Args:
            request (Request): The request object.
            name (str): The name of the data.
            annotation (type): The type annotation of the data.

        Returns:
            dict[str, Any] | None: The encoded data or None if encoding is not possible.

        """
        if annotation in self.types:
            return {name: annotation(await request.json())}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        """Decode the response data.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response | None: The decoded response or None if decoding is not possible.

        """
        if type(response) in self.types:
            if self.response_class:
                return self.response_class(content=response)
        return None

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)


class CookieProcessor(BaseProcessor):
    """A processor for encoding and decoding cookies.

    This processor is responsible for encoding and decoding cookies in HTTP requests.

    Args:
        BaseProcessor (type): The base processor class.

    """

    def __init__(self, response_class: type[Response] | None = None):
        super().__init__([str], response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encode a cookie value.

        This method encodes a cookie value from the given request object.

        Args:
            request (Request): The HTTP request object.
            name (str): The name of the cookie.
            annotation (type): The type of the cookie value.

        Returns:
            dict[str, Any] | None: The encoded cookie value, or None if the cookie is not found.

        """
        if annotation in self.types and name in request.cookies:
            return {name: annotation(request.cookies[name])}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        """
        Decodes the response data based on the provided annotation.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response | None: A response class that can be used by the starlette app.
        """
        return await super().decode(request, response)

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)


class HeaderProcessor(BaseProcessor):
    """
    A processor that handles headers in a request.
    """

    def __init__(self, response_class: type[Response] | None = None):
        super().__init__([str], response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encode the request header value based on the given annotation.

        Args:
            request (Request): The request object.
            name (str): The name of the header.
            annotation (type): The type annotation for the header value.

        Returns:
            dict[str, Any] | None: A dictionary containing the encoded header value,
                or None if the annotation or header is not found.
        """
        if annotation in self.types and name in request.headers:
            return {name.replace("-", "_"): annotation(request.headers[name])}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        """
        Decodes the response data based on the provided annotation.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response | None: A response class that can be used by the starlette app.
        """
        return await super().decode(request, response)

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)


class PydanticProcessor(BaseProcessor):
    """
    A processor that handles Pydantic models in a request.
    """

    def __init__(
        self,
        response_class: type[Response] | None = JSONResponse,
    ):
        super().__init__([BaseModel], response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encode the request data based on the provided annotation.

        Args:
            request (Request): The request object containing the data to be encoded.
            name (str): The name of the data field.
            annotation (type): The type annotation of the data field.

        Returns:
            dict[str, Any] | None:
            The encoded data as a dictionary, or None if the annotation is not a subclass of BaseModel.
        """
        if issubclass(annotation, BaseModel):
            return {name: annotation(**(await request.json()))}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        """Decodes the response object.

        Args:
            request (Request): The request object.
            response (Any): The response object.

        Returns:
            Response | None: The decoded response object, or None if decoding is not applicable.
        """
        if issubclass(type(response), BaseModel) and self.response_class:
            return self.response_class(content=response.model_dump())

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)


class WebsocketProcessor(BaseProcessor):
    """
    A processor that handles WebSocket connections.
    """

    def __init__(self, response_class: type[Response] | None = None):
        super().__init__([WebSocket], response_class)

    async def encode(
        self, request: WebSocket, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encodes the request data.

        Args:
            request (WebSocket): The WebSocket object representing the request.
            name (str): The name of the request.
            annotation (type): The type annotation of the request.

        Returns:
            dict[str, Any] | None: The encoded data as a dictionary, or None if the annotation is not supported.
        """
        if annotation in self.types:
            return {name: request}

    async def decode(self, request: Request, response: Any) -> Response | None:
        """
        Decodes the response data based on the provided annotation.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response | None: A response class that can be used by the starlette app.
        """
        return await super().decode(request, response)

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)


class JinjaProcessor(BaseProcessor):
    """
    A processor that renders Jinja templates.
    """

    def __init__(
        self, template_dir: str, response_class: type[Response] | None = HTMLResponse
    ):
        super().__init__([], response_class)
        self.environment = Environment(
            loader=FileSystemLoader(template_dir),
            line_statement_prefix="#",
            line_comment_prefix="##",
            enable_async=True,
        )
        self.convention: dict = {
            "page": "page.html",
            "layout": "layout.html",
            "error": "error.html",
        }

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        return await super().encode(request, name, annotation)

    async def decode(self, request: Request, response: Any):
        """Decodes the request and generates a response.

        Args:
            request (Request): The request object.
            response (Any): The response object.

        Returns:
            The generated response object.
        """
        if "text/html" in request.headers.get("accept", "").split(","):
            page: Template = self.environment.get_template(
                request.url.path + self.convention["page"]
            )
            if self.response_class:
                return self.response_class(content=page.render(**self.convention))
        return None

    async def exception(self, request: Request, exception: Exception):
        return await super().exception(request, exception)


class HTMXResponse:
    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        self.content = content
        self.status_code = status_code
        self.headers = headers
        self.media_type = media_type
        self.background = background


class HTMXProcessor(BaseProcessor):
    """
    A processor that renders HTMX templates.
    """

    def __init__(
        self, template_dir: str, response_class: type[Response] | None = HTMLResponse
    ):
        super().__init__([], response_class)
        self.environment = Environment(
            loader=FileSystemLoader(template_dir),
            line_statement_prefix="#",
            line_comment_prefix="##",
            enable_async=True,
        )
        self.convention: dict = {
            "page": "page.html",
            "layout": "layout.html",
            "error": "error.html",
        }

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        return await super().encode(request, name, annotation)

    async def decode(self, request: Request, response: Any):
        """Decodes the request and generates a response.

        Args:
            request (Request): The request object.
            response (Any): The response object.

        Returns:
            The generated response object.
        """
        if not isinstance(response, HTMXResponse):
            return None

        if not isinstance(response.content, dict) or isinstance(response.content, str):
            if self.response_class:
                return self.response_class(
                    content=response.content,
                    status_code=response.status_code,
                    headers=response.headers,
                    media_type=response.media_type,
                    background=response.background,
                )

        page: str = await self.environment.get_template(
            request.url.path + self.convention["page"]
        ).render_async(**response.content)

        routes: list[str] = [x for x in request.url.path.split("/") if x]

        html: str = ""

        for index in reversed(range(len(routes))):
            if not index:
                path = "/" + "/".join(routes[:-1] + [routes[-1]]) + "/"
            else:
                path = "/" + "/".join(routes[:-index]) + "/"
            try:
                print(path)
                layout: Template = self.environment.get_template(
                    path + self.convention["layout"]
                )
                if not html:
                    html = await layout.render_async(slot=page)
                if html:
                    html = await layout.render_async(slot=html)
            except TemplateNotFound:
                continue
        try:
            if not html:
                html = await self.environment.get_template(
                    self.convention["layout"]
                ).render_async(slot=page)
        except TemplateNotFound:
            html = page

        if self.response_class:
            return self.response_class(
                content=html,
                status_code=response.status_code,
                headers=response.headers,
                media_type=response.media_type,
                background=response.background,
            )

        return None

    async def exception(self, request: Request, exception: Exception):
        return await super().exception(request, exception)


async def encode_request(
    request: Request | WebSocket,
    endpoint_func: Callable,
    processor_func: list[BaseProcessor],
):
    """
    Encodes the request data for an endpoint.
    """
    data = {}

    params = inspect.signature(endpoint_func).parameters

    for name, annotation in params.items():
        if annotation.annotation in [Request]:
            data.update({name: request})
        for processor in processor_func:
            processed = await processor.encode(request, name, annotation.annotation)
            if processed:
                data.update(processed)

    return data


async def decode_response(
    request: Request, response: Any, processor_func: list[BaseProcessor]
) -> Response | None:
    """
    Decodes the response data for an endpoint.

    Args:
        request (Request): The request object.
        response (Any): The response object.
        processor_func (list[BaseProcessor]): A list of processor functions.

    Returns:
        Response | None:
    """
    for processor in processor_func:
        decoded = await processor.decode(request, response)
        if decoded:
            return decoded
    return None


async def exception_response(
    request: Request, exception: Exception, processor_func: list[BaseProcessor]
) -> Response | None:
    """Handles exceptions by passing them to a list of processor functions.

    Args:
        request (Request): The request object.
        exception (Exception): The exception that occurred.
        processor_func (list[BaseProcessor]): A list of processor functions.

    Returns:
        Response | None:
    """
    for processor in processor_func:
        decoded = await processor.exception(request, exception)
        if decoded:
            return decoded
    return None
