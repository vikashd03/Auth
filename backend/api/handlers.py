import json
from typing import Any, Callable, Optional
from rest_framework import status
from django.http import HttpResponse

from .config import GENERAL_API_ERROR_RESPONSE

def error_res(error_msg, status):
    return HttpResponse(
        json.dumps({"error": error_msg}),
        content_type="application/json",
        status=status,
    )

def is_http_res(res):
    return isinstance(res, HttpResponse)

def handle_error(
    is_view: bool = False,
    error_type: Optional[str] = None,
    return_type: Any = None,
):
    def handle_error_decorator(func: Callable):
        def try_except_wrapper(*args, **kwargs):
            error_title = (
                func.__name__.replace("_", " ") if not error_type else error_type
            )
            try:
                return func(*args, **kwargs)
            except CustomHTTPException as http_exception:
                print(f"{error_title} http error: {http_exception}")
                return error_res(http_exception.msg, http_exception.status)
            except Exception as e:
                print(f"{error_title} error: {e}")
                if is_view:
                    return error_res(GENERAL_API_ERROR_RESPONSE, status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return return_type

        return try_except_wrapper

    return handle_error_decorator


class CustomHTTPException(Exception):
    def __init__(
        self,
        msg=GENERAL_API_ERROR_RESPONSE,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.msg: str = msg
        self.status: int = status

    def __str__(self):
        return self.msg
