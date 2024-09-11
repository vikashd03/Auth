from typing import Optional
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_CREDENTIALS, ACCESS_CONTROL_ALLOW_ORIGIN
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
import json

from .handlers import handle_error
from .config import BASE_ROUTE, UNPROTECTED_ROUTES
from .utils import user_authenticated


class AuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    @handle_error(is_view=True)
    def process_request(self, request: HttpRequest):
        path = request.path
        if path.replace("/" + BASE_ROUTE, "") not in UNPROTECTED_ROUTES:
            print("PROTECTED ROUTE: ", path)
            user_res = user_authenticated(request.headers)
            if isinstance(user_res, HttpResponse):
                return user_res
            request.session["user"] = user_res
        else:
            print("UNPROTECTED ROUTE: ", path)
        return None


class HandleMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def process_request(self, request: HttpRequest):
        pass

    @handle_error(is_view=True)
    def process_response(self, request: HttpRequest, response: Optional[HttpResponse]):
        response.headers[ACCESS_CONTROL_ALLOW_ORIGIN] = '*'
        response.headers[ACCESS_CONTROL_ALLOW_CREDENTIALS] = "true"
        if response["Content-Type"] == "application/json":
            isinstance(json.loads(response.content.decode("utf-8")), dict)
        return response
