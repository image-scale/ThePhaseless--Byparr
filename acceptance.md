# Acceptance Criteria

## Task 1: Core API with challenge bypass functionality

### Acceptance Criteria
- [ ] GET / redirects to /docs with 301 status
- [ ] GET /health returns 200 OK with JSON containing msg, version, and userAgent fields
- [ ] POST /v1 with valid URL navigates to the page and returns cookies, content, headers, userAgent
- [ ] POST /v1 response includes status, message, solution object, startTimestamp, endTimestamp, version
- [ ] POST /v1 detects "Just a moment..." title as Cloudflare challenge and attempts to solve
- [ ] POST /v1 with timeout returns 408 status when challenge solving exceeds max_timeout
- [ ] Request logging middleware logs incoming /v1 POST requests with client IP and URL
- [ ] Configuration reads from environment: HOST, PORT, LOG_LEVEL, VERSION, PROXY_SERVER/USERNAME/PASSWORD
- [ ] Proxy can be overridden per-request via X-Proxy-Server, X-Proxy-Username, X-Proxy-Password headers
- [ ] JSON responses use camelCase field names (e.g., userAgent, startTimestamp)
- [ ] Invalid request to /v1 returns error response with status "error"
