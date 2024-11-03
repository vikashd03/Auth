from typing import Callable, Optional
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.datastructures import State
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from apps.auth.schemas import UserModel
from config import GENERAL_API_ERROR_RESPONSE


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def _(request: Request, exce: RequestValidationError):
        errors = exce.errors()
        fields_not_found = []
        for err in errors:
            fields_not_found.append(err["loc"][1])
        print(
            "RequestValidationError -",
            f"{','.join(fields_not_found)} not found in request body",
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": f"{','.join(fields_not_found)} not found in request body"
            },
        )

    @app.exception_handler(HTTPException)
    async def _(request: Request, exce: HTTPException):
        print("HTTPException -", exce)
        return JSONResponse(
            status_code=exce.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": exce.detail},
        )

    @app.exception_handler(WebSocketException)
    async def _(websocket: WebSocket, exce: WebSocketException):
        print("WebSocketException -", exce)
        await websocket.send("connect_error", exce)
        await websocket.close(**exce)

    @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    @app.exception_handler(Exception)
    async def _(request: Request, exce: Exception):
        print("Other Exception -", exce)
        if isinstance(exce, HTTPException) or isinstance(exce, RequestValidationError):
            return await app.exception_handlers[type(exce)](request, exce)
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": GENERAL_API_ERROR_RESPONSE},
            )


def handle_error(
    app: FastAPI,
    request: Request,
    error_type: Optional[str],
):
    def handle_error_decorator(func: Callable):
        async def try_except_wrapper(*args, **kwargs):
            error_title = (
                func.__name__.replace("_", " ") if not error_type else error_type
            )
            try:
                return func(*args, **kwargs)
            except (HTTPException, RequestValidationError) as exce:
                print(f"{error_title} http Exception: {exce}")
                return await app.exception_handlers[type(exce)](request, exce)
            except Exception as exce:
                print(f"{error_title} Exception: {exce}")
                return await app.exception_handlers[Exception](request, exce)

        return try_except_wrapper

    return handle_error_decorator


class RequestState(State):
    user: UserModel


class AppRequest(Request):
    state: RequestState
