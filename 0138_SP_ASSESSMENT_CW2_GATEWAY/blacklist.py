from fastapi import HTTPException

BLACKLISTED_DEVICES = set()


def check_blacklist(device_id: str):
    if device_id in BLACKLISTED_DEVICES:
        raise HTTPException(status_code=403, detail="Device is blacklisted")


def add_to_blacklist(device_id: str):
    BLACKLISTED_DEVICES.add(device_id)


def remove_from_blacklist(device_id: str):
    BLACKLISTED_DEVICES.discard(device_id)

def clear_blacklist():
    BLACKLISTED_DEVICES.clear()