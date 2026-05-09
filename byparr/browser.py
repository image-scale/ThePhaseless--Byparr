from __future__ import annotations

import sys
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Annotated, NamedTuple, cast

from camoufox import AsyncCamoufox
from fastapi import Header
from playwright.async_api import Browser, BrowserContext, Page
from playwright_captcha import ClickSolver, FrameworkType
from playwright_captcha.utils.camoufox_add_init_script.add_init_script import get_addon_path

from byparr.config import PROXY_PASSWORD, PROXY_SERVER, PROXY_USERNAME


class BrowserSession(NamedTuple):
    page: Page
    solver: ClickSolver
    context: BrowserContext


async def create_browser_session(
    x_proxy_server: Annotated[
        str | None,
        Header(
            alias="X-Proxy-Server",
            description="Override proxy server for this request (protocol://host:port format).",
        ),
    ] = None,
    x_proxy_username: Annotated[
        str | None,
        Header(alias="X-Proxy-Username"),
    ] = None,
    x_proxy_password: Annotated[
        str | None,
        Header(alias="X-Proxy-Password"),
    ] = None,
) -> AsyncGenerator[BrowserSession]:
    proxy = None
    if x_proxy_server:
        proxy = {
            "server": x_proxy_server,
            "username": x_proxy_username,
            "password": x_proxy_password,
        }
    elif PROXY_SERVER:
        proxy = {
            "server": PROXY_SERVER,
            "username": PROXY_USERNAME,
            "password": PROXY_PASSWORD,
        }

    addon_path = str(Path(get_addon_path()).absolute())

    async with AsyncCamoufox(
        main_world_eval=True,
        addons=[addon_path],
        geoip=True,
        proxy=proxy,
        locale="en-US",
        headless=True,
        humanize=True,
        i_know_what_im_doing=True,
        config={"forceScopeAccess": True},
        disable_coop=True,
    ) as browser_raw:
        browser = cast("Browser", browser_raw)
        context = await browser.new_context()
        page = await context.new_page()
        async with ClickSolver(
            framework=FrameworkType.CAMOUFOX,
            page=page,
            max_attempts=sys.maxsize,
            attempt_delay=1,
        ) as solver:
            yield BrowserSession(page, solver, context)
