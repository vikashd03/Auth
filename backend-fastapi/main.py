import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from apps.auth.main import app as auth_app
from internal.utils import register_exception_handlers

app = FastAPI()

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
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2)) + "s"
    return response


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    response = await call_next(request)
    print("auth middleware")
    return response


@app.get("/")
async def root():
    return {"message": "Main"}
