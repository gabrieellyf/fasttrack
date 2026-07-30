import logging
import time
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("fasttrack.http")


class ResponseLoggerMiddleware(BaseHTTPMiddleware):
    """ASGI middleware that logs HTTP method, path, status code, and duration.

    Example log line::

        POST /routes → 200 (42.3 ms)
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process the request, delegate to the next handler, and log the result.

        Args:
            request: The incoming HTTP request.
            call_next: Callable that forwards the request to the next middleware or route.

        Returns:
            The HTTP response returned by the handler.
        """
        start = time.monotonic()
        response = await call_next(request)
        duration_ms = (time.monotonic() - start) * 1000

        logger.info(
            "%s %s → %d (%.1f ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
