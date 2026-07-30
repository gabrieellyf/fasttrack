from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions.base import CustomException, WeightLimitExceededException


def add_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on a FastAPI application instance.

    All CustomException subclasses are serialised to a consistent JSON body
    with ``error_code`` and ``message``. WeightLimitExceededException also
    includes a ``details`` field with the numeric weight values.

    Args:
        app: The FastAPI application to attach handlers to.
    """

    @app.exception_handler(CustomException)
    async def _handle_custom_exception(
        _request: Request,
        exc: CustomException,
    ) -> JSONResponse:
        body: dict[str, object] = {
            "error_code": exc.error_code,
            "message": exc.message,
        }

        if isinstance(exc, WeightLimitExceededException):
            body["details"] = {
                "total_weight": exc.total_weight,
                "max_weight": exc.max_weight,
            }

        return JSONResponse(status_code=exc.status_code, content=body)
