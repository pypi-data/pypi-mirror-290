import typing as t

from ellar.common.interfaces import IHostContext
from ellar.common.types import ASGIApp, TReceive, TScope, TSend
from ellar.core.execution_context import current_connection
from starlette.responses import Response

AwaitableCallable = t.Callable[..., t.Awaitable]
DispatchFunction = t.Callable[
    [IHostContext, AwaitableCallable], t.Awaitable[t.Optional[Response]]
]
T = t.TypeVar("T")


class FunctionBasedMiddleware:
    """
    Converts a function to an ASGI Middleware

    Usage: Example 1 in @Module()
        @middleware()
        async def my_middleware(cls, context: IExecutionContext, call_next):
            print("Called my_middleware")
            request = context.switch_to_http_connection().get_request()
            request.state.my_middleware = True
            await call_next()

    Usage: Example 2
        @middleware()
        async def my_middleware(context: IExecutionContext, call_next):
            print("Called my_middleware")
            response = context.switch_to_http_connection().get_response()
            response.content = "Some Content"
            response.status_code = 200
            return response

    Usage 3: Plain
        async def asgi_middleware(execution_context: IExecutionContext, call_next):
            #Run some actions
            await call_next()

        Middleware(FunctionBasedMiddleware, dispatch=asgi_middleware)
    """

    def __init__(
        self, app: ASGIApp, dispatch: t.Optional[DispatchFunction] = None
    ) -> None:
        self.app = app
        self.dispatch_function = dispatch or self.dispatch

    async def dispatch(
        self, context: IHostContext, call_next: AwaitableCallable
    ) -> Response:
        raise NotImplementedError()  # pragma: no cover

    async def __call__(self, scope: TScope, receive: TReceive, send: TSend) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        async def call_next() -> None:
            await self.app(scope, receive, send)

        response = await self.dispatch_function(current_connection, call_next)

        if response and isinstance(response, Response):
            await response(scope, receive, send)
