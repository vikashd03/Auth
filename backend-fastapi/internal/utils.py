from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def _(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        fields_not_found = []
        for err in errors:
            fields_not_found.append(err["loc"][1])
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": f"{','.join(fields_not_found)} not found in request body"
            },
        )

    @app.exception_handler(HTTPException)
    async def _(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": exc.detail},
        )
