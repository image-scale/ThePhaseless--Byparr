import time
import warnings
from asyncio import wait_for
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from playwright._impl._errors import TimeoutError as PlaywrightTimeout
from playwright_captcha import CaptchaType

from byparr.browser import BrowserSession, create_browser_session
from byparr.config import CLOUDFLARE_CHALLENGE_TITLES
from byparr.helpers import CountdownTimer, logger
from byparr.schemas import HealthStatus, PageSolution, SolveRequest, SolveResponse

warnings.filterwarnings("ignore", category=SyntaxWarning)

api_router = APIRouter()

BrowserDep = Annotated[BrowserSession, Depends(create_browser_session)]


@api_router.get("/", include_in_schema=False)
def redirect_to_docs():
    logger.debug("Redirecting to /docs")
    return RedirectResponse(url="/docs", status_code=301)


@api_router.get("/health")
async def check_health(session: BrowserDep):
    result = await solve_challenge(
        SolveRequest.model_construct(url="https://google.com"),
        session,
    )
    if result.solution.status != HTTPStatus.OK:
        raise HTTPException(status_code=500, detail="Health check failed")
    return HealthStatus(user_agent=result.solution.user_agent)


@api_router.post("/v1")
async def solve_challenge(request: SolveRequest, session: BrowserDep) -> SolveResponse:
    start_time = int(time.time() * 1000)
    timer = CountdownTimer(duration=request.max_timeout)

    url = request.url.replace('"', "").strip()

    try:
        nav_response = await session.page.goto(url, timeout=timer.time_left() * 1000)
        status = nav_response.status if nav_response else HTTPStatus.OK

        await session.page.wait_for_load_state(
            state="domcontentloaded", timeout=timer.time_left() * 1000
        )
        await session.page.wait_for_load_state(
            "networkidle", timeout=timer.time_left() * 1000
        )

        title = await session.page.title()
        if title in CLOUDFLARE_CHALLENGE_TITLES:
            logger.info("Challenge detected, attempting to solve...")
            await wait_for(
                session.solver.solve_captcha(
                    captcha_container=session.page,
                    captcha_type=CaptchaType.CLOUDFLARE_INTERSTITIAL,
                    wait_checkbox_attempts=1,
                    wait_checkbox_delay=0.5,
                ),
                timeout=timer.time_left(),
            )
            status = HTTPStatus.OK
            logger.debug("Challenge solved successfully.")

    except (TimeoutError, PlaywrightTimeout) as e:
        logger.error("Timed out while solving the challenge")
        raise HTTPException(
            status_code=408,
            detail="Timed out while solving the challenge",
        ) from e

    cookies = await session.context.cookies()
    user_agent = await session.page.evaluate("navigator.userAgent")
    content = await session.page.content()
    headers = nav_response.headers if nav_response else {}

    return SolveResponse(
        message="Success",
        solution=PageSolution(
            user_agent=user_agent,
            url=session.page.url,
            status=status,
            cookies=cookies,
            headers=headers,
            response=content,
        ),
        start_timestamp=start_time,
    )
