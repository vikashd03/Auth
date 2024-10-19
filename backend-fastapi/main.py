import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from apps.auth.main import app as auth_app
from apps.auth.utils import TOKEN_TYPE, user_authenticated
from config import BASE_ROUTE
from internal.utils import register_exception_handlers
from internal.types import Middlware_Call_Next

app = FastAPI(root_path=BASE_ROUTE)

register_exception_handlers(app)

app.mount("/auth", auth_app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Middlware_Call_Next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2)) + "s"
    return response


@app.middleware("http")
async def auth_middleware(request: Request, call_next: Middlware_Call_Next):
    path = str(request.url).replace(str(request.base_url), "")
    if not path.startswith("auth/"):
        print("PROTECTED ROUTE:", path)
        try:
            user = user_authenticated(dict(request.headers), TOKEN_TYPE.ACCESS)
            request.state.user = user
        except (HTTPException, RequestValidationError) as exce:
            return await app.exception_handlers[type(exce)](request, exce)
        except Exception as exce:
            return await app.exception_handlers[Exception](request, exce)
    else:
        print("UNPROTECTED ROUTE:", path)
    response = await call_next(request)
    return response


@app.get("/root")
async def root(request: Request):
    print("User -", request.state.user)
    return {"message": "Main"}
