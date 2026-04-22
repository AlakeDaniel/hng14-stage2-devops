# FIXES.md — Bug Report for HNG Stage 2

## Bug 1
- **File:** api/main.py
- **Line:** 6
- **Problem:** Redis host hardcoded as `localhost` — fails inside Docker network where Redis is reachable by service name
- **Fix:** Changed to `os.environ.get("REDIS_HOST", "redis")`

## Bug 2
- **File:** api/main.py
- **Line:** 6
- **Problem:** Redis port hardcoded as `6379` — not configurable via environment
- **Fix:** Changed to `int(os.environ.get("REDIS_PORT", 6379))`

## Bug 3
- **File:** api/main.py
- **Problem:** No `/health` endpoint — required for Docker healthcheck and CI/CD pipeline
- **Fix:** Added `GET /health` endpoint that pings Redis and returns `{"status": "healthy"}`

## Bug 4
- **File:** api/main.py
- **Problem:** No error handling — missing jobs returned no HTTP status code, just a plain dict
- **Fix:** Added `HTTPException` with 404 status for missing jobs

## Bug 5
- **File:** api/main.py
- **Problem:** `decode_responses` not set on Redis client — required `.decode()` calls manually
- **Fix:** Added `decode_responses=True` to Redis client initialization

## Bug 6
- **File:** worker/worker.py
- **Line:** 4
- **Problem:** Redis host hardcoded as `localhost` — fails inside Docker network
- **Fix:** Changed to `os.environ.get("REDIS_HOST", "redis")`

## Bug 7
- **File:** worker/worker.py
- **Line:** 4
- **Problem:** Redis port hardcoded as `6379` — not configurable via environment
- **Fix:** Changed to `int(os.environ.get("REDIS_PORT", 6379))`

## Bug 8
- **File:** worker/worker.py
- **Problem:** Infinite loop with no signal handling — container could not shut down gracefully
- **Fix:** Added `signal.signal(SIGTERM)` and `signal.signal(SIGINT)` handlers with a `running` flag

## Bug 9
- **File:** frontend/app.js
- **Line:** 5
- **Problem:** API URL hardcoded as `http://localhost:8000` — fails inside Docker network
- **Fix:** Changed to `process.env.API_URL || "http://api:8000"`

## Bug 10
- **File:** frontend/app.js
- **Problem:** No `/health` endpoint — required for Docker healthcheck
- **Fix:** Added `GET /health` endpoint returning `{"status": "healthy"}`

## Bug 11
- **File:** api/.env
- **Problem:** `.env` file containing `REDIS_PASSWORD=supersecretpassword123` was committed to the repository — critical security issue
- **Fix:** Removed from git tracking with `git rm --cached api/.env`, added to `.gitignore`

## Bug 12
- **File:** api/requirements.txt
- **Problem:** Dependencies had no pinned versions — non-reproducible builds
- **Fix:** Pinned all versions: fastapi==0.104.1, uvicorn[standard]==0.24.0, redis==5.0.1, python-dotenv==1.0.0

## Bug 13
- **File:** worker/requirements.txt
- **Problem:** Missing `python-dotenv` dependency needed for environment variable loading
- **Fix:** Added `python-dotenv==1.0.0`

## Bug 14
- **File:** frontend/ (missing file)
- **Problem:** No `package-lock.json` present — `npm ci` requires a lockfile
- **Fix:** Changed Dockerfile to use `npm install --omit=dev` instead of `npm ci`

## Bug 15
- **File:** api/Dockerfile
- **Problem:** Multi-stage build copied packages from `/root/.local` to `/home/appuser/.local` but Python could not find them — `ModuleNotFoundError: No module named 'uvicorn'`
- **Fix:** Switched to single-stage build and used `python -m uvicorn` to invoke uvicorn as a module
