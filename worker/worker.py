import redis
import time
import os
import signal
import sys

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

running = True


def handle_shutdown(signum, frame):
    global running
    print("Shutting down worker gracefully...")
    running = False


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


print("Worker started, waiting for jobs...")
while running:
    job = r.brpop("job", timeout=5)
    if job:
        _, job_id = job
        process_job(job_id)

print("Worker stopped.")
sys.exit(0)
