import time
from fastapi import FastAPI, HTTPException, Request, WebSocketException, status
from fastapi.datastructures import QueryParams
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
import ssl

from apps.auth.main import app as auth_app
from apps.chat.main import app as chat_app
from apps.chat.socket import app as chat_ws_app

from apps.auth.utils import REQUEST_TYPE, TOKEN_TYPE, user_authenticated
from config import ALLOWED_ORIGINS, BASE_DIR, BASE_ROUTE, UNPROTECTED_ROUTES
from internal.utils import AppRequest, register_exception_handlers
from internal.types import Middlware_Call_Next

app = FastAPI(root_path=BASE_ROUTE)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    certfile=BASE_DIR + "/cert.pem", keyfile=BASE_DIR + "/key.pem"
)

app.mount("/data", StaticFiles(directory="data"), name="data")

app.mount("/auth", auth_app)
app.mount("/chat", chat_app)
app.mount("/", chat_ws_app)

register_exception_handlers(app)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Middlware_Call_Next):
    start_time = time.perf_counter()
    # time.sleep(0.5) # for testing purpose
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2)) + "s"
    return response


@app.middleware("http")
async def auth_middleware(request: Request, call_next: Middlware_Call_Next):
    path = request.url.path.replace(BASE_ROUTE + "/", "")
    path = path if path.endswith("/") else path + "/"
    if (
        path not in UNPROTECTED_ROUTES
        and not path.startswith("data/")
        and not path.endswith("docs/")
        and not path.endswith("openapi.json/")
    ):
        print("PROTECTED ROUTE:", path)
        try:
            request.state.user = user_authenticated(
                dict(request.headers), TOKEN_TYPE.ACCESS
            )
        except (HTTPException, RequestValidationError) as exce:
            return await app.exception_handlers[type(exce)](request, exce)
        except Exception as exce:
            return await app.exception_handlers[Exception](request, exce)
    else:
        print("UNPROTECTED ROUTE:", path)
    response = await call_next(request)
    return response


class SocketIOMiddleware(BaseHTTPMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            print("WebSocket ROUTE:", scope["path"])
            query_params = dict(QueryParams(scope.get("query_string")))
            scope["state"] = {}
            try:
                scope["state"]["user"] = user_authenticated(
                    data=query_params,
                    token_type=TOKEN_TYPE.ACCESS,
                    request_type=REQUEST_TYPE.WEBSOCKET,
                )
            except WebSocketException as exce:
                await send({"type": "websocket.close", "code": exce.code})
                return
            except Exception as exce:
                return await app.exception_handlers[Exception](scope, exce)
        await self.app(scope, receive, send)


app.add_middleware(SocketIOMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/root")
async def root(request: AppRequest):
    print("User -", request.state.user)
    return {"message": "Main"}
