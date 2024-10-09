from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_validation_exception_handler(app):
    @app.exception_handler(RequestValidationError)
    async def _(request: Request, exc: RequestValidationError):
        error = exc.errors()[0]
        loc: tuple = error["loc"]
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"{loc[1]} not found in request {loc[0]}"},
        )
