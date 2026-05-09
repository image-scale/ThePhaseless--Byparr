# Todo

## Plan
First implement configuration and utility modules that provide constants and helpers. Then build the core data models for API requests/responses. Next implement the browser management layer with proxy support. Finally create the FastAPI endpoints with middleware for logging and challenge solving. The test suite will verify endpoints work correctly.

## Tasks
- [x] Task 1: Implement the core API with FastAPI including a health check endpoint that verifies the browser can navigate to a test site (google.com) and a main v1 endpoint that navigates to a given URL, detects Cloudflare challenges, solves them using a captcha solver, and returns cookies, content, headers, and user agent. Include request/response models with camelCase JSON aliases, configuration via environment variables (HOST, PORT, LOG_LEVEL, VERSION, proxy settings), timeout tracking, request logging middleware, and stealth browser integration with Camoufox. The root path should redirect to /docs.
