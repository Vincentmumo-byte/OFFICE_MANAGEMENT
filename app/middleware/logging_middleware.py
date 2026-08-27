import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


logger = logging.getLogger("CreatingHumanity.middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            duration_ms = (
                time.perf_counter() - start_time
            ) * 1000

            logger.info(
                "%s %s -> %s (%.2f ms)",
                request.method,
                request.url.path,
                response.status_code,
                duration_ms,
            )

            return response

        except Exception:
            duration_ms = (
                time.perf_counter() - start_time
            ) * 1000

            logger.exception(
                "%s %s -> ERROR (%.2f ms)",
                request.method,
                request.url.path,
                duration_ms,
            )

            raise