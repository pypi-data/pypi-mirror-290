import asyncio
import json
import logging
from typing import Callable, Awaitable

import websockets
from websockets.frames import CloseCode

import xraptor
from xraptor.connection import Connection
from xraptor.domain.methods import MethodType
from xraptor.domain.request import Request
from xraptor.domain.response import Response


class Handler:

    @staticmethod
    async def watch(websocket: websockets.WebSocketServerProtocol):
        connection = Connection.from_ws(websocket)
        close_code: CloseCode = CloseCode.NORMAL_CLOSURE
        try:
            async for message in connection.ws:
                await Handler._handle_request(message, connection)
        except websockets.exceptions.ConnectionClosed as e:
            logging.error(e)
            close_code = CloseCode.GOING_AWAY
        except websockets.exceptions.InvalidHandshake as e:
            logging.error(e)
            close_code = CloseCode.TLS_HANDSHAKE
        except websockets.exceptions.WebSocketException as e:
            logging.error(e)
            close_code = CloseCode.PROTOCOL_ERROR
        except Exception as e:
            logging.error(e)
            close_code = CloseCode.ABNORMAL_CLOSURE
        finally:
            await connection.close(close_code=close_code)
            del connection

    @staticmethod
    async def _handle_request(message: str | bytes, connection: Connection):
        try:
            request = Request.from_message(message)
        except AssertionError:
            return

        try:
            result = '{message: "Not registered"}'
            if fn := xraptor.XRaptor.route_matcher(request.method, request.route):
                if (
                        request.method == MethodType.GET
                        or request.method == MethodType.POST
                ):
                    result = await fn(request.payload)
                if request.method == MethodType.SUB:
                    result = await Handler._subscribe(request, connection, fn)
                if request.method == MethodType.UNSUB:
                    result = await fn(request.payload, request.request_id)
                    connection.unregister_response_receiver(request)
            if result:
                _response = Response.from_message(
                    request_id=request.request_id,
                    header={},
                    payload=result
                )
                await connection.ws.send(_response.json())
        except Exception as e:
            logging.error(e)
            _response = Response.from_message(
                request_id=request.request_id,
                header={},
                payload='{"message": "fail"}'
            )
            await connection.ws.send(_response.json())

    @staticmethod
    async def _subscribe(request: Request, connection: Connection, fn: Callable) -> Awaitable:
        try:
            connection.register_response_receiver(request)
            await asyncio.sleep(0)
            result = await fn(request.payload, request.request_id)
            return result
        except Exception as e:
            logging.error(e)
            connection.unregister_response_receiver(request)
