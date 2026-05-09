from __future__ import annotations

import time
from http import HTTPStatus
from typing import Any

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

from byparr.config import VERSION


class SolveRequest(BaseModel):
    cmd: str = Field(
        default="request.get",
        description="Request command type. Only GET requests are supported, this field exists for compatibility.",
    )
    url: str = Field(pattern=r"^https?://", default="https://")
    max_timeout: int = Field(
        default=60,
        description="Maximum time in seconds allowed for solving anti-bot challenges.",
    )


class HealthStatus(BaseModel):
    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    msg: str = "Byparr is working!"
    version: str = VERSION
    user_agent: str


class PageSolution(BaseModel):
    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    url: str
    status: int
    cookies: list[dict[str, Any]] = []
    user_agent: str = ""
    headers: dict[str, Any] = {}
    response: str = ""


class SolveResponse(BaseModel):
    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    status: str = "ok"
    message: str
    solution: PageSolution
    start_timestamp: int
    end_timestamp: int = Field(default_factory=lambda: int(time.time() * 1000))
    version: str = VERSION

    @classmethod
    def error_response(cls, url: str):
        return cls(
            status="error",
            message="Invalid request",
            solution=PageSolution(url=url, status=HTTPStatus.INTERNAL_SERVER_ERROR),
            start_timestamp=int(time.time() * 1000),
        )
