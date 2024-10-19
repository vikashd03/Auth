from typing import Awaitable, Callable
from fastapi import Request, Response


Middlware_Call_Next = Callable[[Request], Awaitable[Response]]
