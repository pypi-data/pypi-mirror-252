# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import typing
import signal
import socket
import grpc
import msgpack

from pydantic import BaseModel

from ...extend.asyncio.base import Utils


UNARY_UNARY_MODE = grpc.unary_unary_rpc_method_handler
UNARY_STREAM_MODE = grpc.unary_stream_rpc_method_handler
STREAM_UNARY_MODE = grpc.stream_unary_rpc_method_handler
STREAM_STREAM_MODE = grpc.stream_stream_rpc_method_handler


class Router:

    def __init__(self, service: str):

        self._service: str = service
        self._handlers: typing.Dict[str, typing.Callable] = {}

    @property
    def service(self) -> str:
        return self._service

    @property
    def handlers(self) -> typing.List[typing.Callable]:
        return list(self._handlers.values())

    def register(self, func: typing.Callable) -> typing.Callable:

        if func.__name__ in self._handlers:
            raise ValueError(f'{func.__name__} has exists')

        self._handlers[func.__name__] = func

        return func

    def __call__(self, model: typing.Type[BaseModel]) -> typing.Callable:

        def wrapper(func: typing.Callable):

            if func.__name__ in self._handlers:
                raise ValueError(f'{func.__name__} has exists')

            @Utils.func_wraps(func)
            async def _wrapper(request, context):
                return await func(model(**request), context)

            self._handlers[func.__name__] = _wrapper

            return _wrapper

        return wrapper


class GRPCServer:

    def __init__(
            self,
            interceptors: typing.Optional[typing.Sequence[typing.Any]] = None,
            options: typing.Optional[grpc.aio.ChannelArgumentType] = None,
            maximum_concurrent_rpcs: typing.Optional[int] = None,
            compression: typing.Optional[grpc.Compression] = None,
            request_deserializer: typing.Callable = msgpack.loads,
            response_serializer: typing.Callable = msgpack.dumps
    ):

        self._server: grpc.aio.Server = grpc.aio.server(
            interceptors=interceptors,
            options=options,
            maximum_concurrent_rpcs=maximum_concurrent_rpcs,
            compression=compression
        )

        self._request_deserializer: typing.Callable = request_deserializer
        self._response_serializer: typing.Callable = response_serializer

        signal.signal(signal.SIGINT, self._exit)
        signal.signal(signal.SIGTERM, self._exit)

    def _exit(self, *_):

        Utils.call_soon(self.stop)

    @property
    def server(self) -> grpc.aio.Server:

        return self._server

    def register(self, service: str, handlers: typing.List[typing.Callable], *, mode: typing.Callable = UNARY_UNARY_MODE):

        generic_handlers = []

        for handler in handlers:
            generic_handlers.append(
                grpc.method_handlers_generic_handler(
                    service,
                    {
                        handler.__name__: mode(
                            handler,
                            request_deserializer=self._request_deserializer,
                            response_serializer=self._response_serializer,
                        )
                    }
                )
            )

        self._server.add_generic_rpc_handlers(generic_handlers)

    def bind_router(self, router: Router, *, mode: typing.Callable = UNARY_UNARY_MODE):
        self.register(router.service, router.handlers, mode=mode)

    async def start(
            self,
            address: typing.Optional[str, typing.Tuple[str, int]],
            family: int = socket.AF_INET,
            server_credentials: typing.Optional[grpc.ServerCredentials] = None
    ):

        if family == socket.AF_INET:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _address = f'{address[0]}:{address[1]}'
        elif family == socket.AF_INET6:
            _socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            _address = f'[{address[0]}]:{address[1]}'
        elif family == socket.AF_UNIX:
            _socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            _address = f'unix:{address}'
        else:
            raise ValueError(r'family invalid')

        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, True)
        _socket.bind(address)

        if server_credentials is None:
            self._server.add_insecure_port(_address)
        else:
            self._server.add_secure_port(_address, server_credentials)

        await self._server.start()

        Utils.log.success(f'grpc server [pid:{Utils.getpid()}] startup complete: {address}')

    async def stop(self, grace: typing.Optional[float] = None):

        await self._server.stop(grace)

    async def wait(self, timeout: typing.Optional[float] = None):

        return await self._server.wait_for_termination(timeout)
