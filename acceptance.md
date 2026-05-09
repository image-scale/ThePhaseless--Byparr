# Acceptance Criteria

## Task 1: Core API with challenge bypass functionality

### Acceptance Criteria
- [x] GET / redirects to /docs with 301 status
- [x] GET /health returns 200 OK with JSON containing msg, version, and userAgent fields
- [x] POST /v1 with valid URL navigates to the page and returns cookies, content, headers, userAgent
- [x] POST /v1 response includes status, message, solution object, startTimestamp, endTimestamp, version
- [x] POST /v1 detects "Just a moment..." title as Cloudflare challenge and attempts to solve
- [x] POST /v1 with timeout returns 408 status when challenge solving exceeds max_timeout
- [x] Request logging middleware logs incoming /v1 POST requests with client IP and URL
- [x] Configuration reads from environment: HOST, PORT, LOG_LEVEL, VERSION, PROXY_SERVER/USERNAME/PASSWORD
- [x] Proxy can be overridden per-request via X-Proxy-Server, X-Proxy-Username, X-Proxy-Password headers
- [x] JSON responses use camelCase field names (e.g., userAgent, startTimestamp)
- [x] Invalid request to /v1 returns error response with status "error"
