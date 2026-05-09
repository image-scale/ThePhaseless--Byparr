import time
from http import HTTPStatus

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from byparr.helpers import logger
from byparr.schemas import SolveRequest


class RequestLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path != "/v1" or request.method != "POST":
            return await call_next(request)

        start = time.perf_counter()
        body = SolveRequest.model_validate(await request.json())
        client_host = request.client.host if request.client else "unknown"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"From: {client_host} at {timestamp}: {body.url}")

        response = await call_next(request)

        duration = time.perf_counter() - start
        if response.status_code == HTTPStatus.OK:
            logger.info(f"Done {body.url} in {duration:.2f}s")
        else:
            logger.warning(f"Failed {body.url} in {duration:.2f}s")

        return response
