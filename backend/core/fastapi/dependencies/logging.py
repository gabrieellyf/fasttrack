import logging

from fastapi import BackgroundTasks, Request

logger = logging.getLogger("fasttrack.app")


def log_request(request: Request, background_tasks: BackgroundTasks) -> None:
    """FastAPI dependency that enqueues a debug log entry as a background task.

    Args:
        request: The current HTTP request, used to extract method, path, and client IP.
        background_tasks: FastAPI background task queue to schedule the log write.
    """

    def _log() -> None:
        logger.debug(
            "Request: %s %s | client=%s",
            request.method,
            request.url.path,
            request.client.host if request.client else "unknown",
        )

    background_tasks.add_task(_log)
