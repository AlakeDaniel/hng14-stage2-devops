# HNG Stage 2 — Containerize & Ship a Microservices Application

## Overview
A job processing system made up of three services containerized with Docker,
orchestrated with Docker Compose, and shipped with a full CI/CD pipeline
using GitHub Actions.

## Services
| Service  | Language       | Role                              |
|----------|---------------|-----------------------------------|
| frontend | Node.js        | Users submit and track jobs       |
| api      | Python/FastAPI | Creates jobs, serves status       |
| worker   | Python         | Processes jobs from Redis queue   |
| redis    | Redis          | Shared queue between api & worker |

## Prerequisites
- Docker >= 20.x
- Docker Compose >= 2.x
- Git

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/AlakeDaniel/hng14-stage2-devops.git
cd hng14-stage2-devops
```

### 2. Create your environment file
```bash
cp .env.example .env
```

### 3. Bring the full stack up
```bash
docker compose up --build
```

### 4. Verify all services are healthy
```bash
docker ps
```

All four containers should show `(healthy)` status:
frontend   Up (healthy)   0.0.0.0:3000->3000/tcp
worker     Up (healthy)
api        Up (healthy)
redis      Up (healthy)
### 5. Test the application
```bash
# Check frontend is running
curl http://localhost:3000/health

# Submit a job
curl -X POST http://localhost:3000/submit

# Check job status (replace JOB_ID with returned id)
curl http://localhost:3000/status/JOB_ID
```

A successful job flow looks like:
```json
// Submit job
{"job_id": "abc-123"}

// Check status (after ~3 seconds)
{"job_id": "abc-123", "status": "completed"}
```

## Environment Variables
All configuration comes from environment variables. See `.env.example`:

| Variable       | Description                    | Default              |
|----------------|-------------------------------|----------------------|
| REDIS_HOST     | Redis service hostname         | redis                |
| REDIS_PORT     | Redis service port             | 6379                 |
| API_URL        | Internal API URL for frontend  | http://api:8000      |
| FRONTEND_PORT  | Host port for frontend         | 3000                 |
| API_PORT       | Internal API port              | 8000                 |

## Architecture
Internet → Frontend (port 3000)
↓
API (port 8000, internal)
↓
Redis (port 6379, internal)
↓
Worker (no port, internal)
## CI/CD Pipeline
GitHub Actions pipeline runs on every push to `main`:
lint → test → build → security-scan → integration-test → deploy
| Stage            | Description                                          |
|------------------|------------------------------------------------------|
| lint             | flake8 (Python), eslint (JS), hadolint (Dockerfiles) |
| test             | pytest with 4 unit tests and coverage report         |
| build            | Build and push images to local registry              |
| security-scan    | Trivy scan — fails on CRITICAL vulnerabilities       |
| integration-test | Full stack test — submit job and verify completion   |
| deploy           | Rolling update on pushes to main                     |

## Stopping the Stack
```bash
docker compose down

# Remove volumes too
docker compose down -v
```

## Author
**Alake Daniel Adebayo**
- GitHub: [AlakeDaniel](https://github.com/AlakeDaniel)
- Email: danieladebayo78ng@gmail.com

---
*HNG Internship DevOps Track — Stage 2*
