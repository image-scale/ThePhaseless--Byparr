import logging
import time

from pydantic import BaseModel, Field

from byparr.config import LOG_LEVEL

solver_logger = logging.getLogger("playwright_captcha")
solver_logger.handlers.clear()
if LOG_LEVEL == logging.DEBUG:
    solver_logger.addHandler(logging.StreamHandler())
    solver_logger.setLevel(LOG_LEVEL)
else:
    solver_logger.handlers.append(logging.NullHandler())

logger = logging.getLogger("uvicorn.error")
logger.setLevel(LOG_LEVEL)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())


class CountdownTimer(BaseModel):
    duration: int
    start_time: float = Field(default_factory=time.perf_counter)

    def time_left(self) -> float:
        elapsed = time.perf_counter() - self.start_time
        return max(0, self.duration - elapsed)
