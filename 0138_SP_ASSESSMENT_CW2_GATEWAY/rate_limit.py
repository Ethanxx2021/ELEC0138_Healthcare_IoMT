import time
from fastapi import HTTPException

# record of request timestamps for each device_id
REQUEST_LOG = {}

# configurable rate limit parameters
RATE_LIMIT_WINDOW = 10
RATE_LIMIT_MAX_REQUESTS = 5


def check_rate_limit(device_id: str):
    current_time = time.time()

    if device_id not in REQUEST_LOG:
        REQUEST_LOG[device_id] = []

    # only keep timestamps within the rate limit window
    REQUEST_LOG[device_id] = [
        ts for ts in REQUEST_LOG[device_id]
        if current_time - ts < RATE_LIMIT_WINDOW
    ]

    # check if the number of requests in the current window exceeds the limit
    if len(REQUEST_LOG[device_id]) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # record this request
    REQUEST_LOG[device_id].append(current_time)


def reset_rate_limit(device_id: str | None = None):
    if device_id is None:
        REQUEST_LOG.clear()
    else:
        REQUEST_LOG.pop(device_id, None)