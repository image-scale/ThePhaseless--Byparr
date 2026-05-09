import logging
import os

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8191"))
LOG_LEVEL = logging.getLevelNamesMapping().get(os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)
VERSION = os.getenv("VERSION", "unknown").removeprefix("v")

PROXY_SERVER = os.getenv("PROXY_SERVER")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")

CLOUDFLARE_CHALLENGE_TITLES = ["Just a moment..."]
