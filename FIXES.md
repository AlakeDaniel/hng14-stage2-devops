
## Bug 11
- **File:** frontend/package.json
- **Line:** N/A
- **Problem:** No package-lock.json present — `npm ci` requires a lockfile to work
- **Fix:** Changed Dockerfile to use `npm install --omit=dev` instead of `npm ci --only=production`
