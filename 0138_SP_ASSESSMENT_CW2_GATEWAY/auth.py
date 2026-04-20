from fastapi import HTTPException
from registry import DEVICE_REGISTRY


def verify_device_and_token(device_id: str, patient_id: str, token: str):
    # 1. Check if the device exists
    if device_id not in DEVICE_REGISTRY:
        raise HTTPException(status_code=403, detail="Unknown device")

    device_info = DEVICE_REGISTRY[device_id]

    # 2. Check if the device is active
    if device_info["status"] != "active":
        raise HTTPException(status_code=403, detail="Device is not active")

    # 3. Check if the patient_id matches
    if device_info["patient_id"] != patient_id:
        raise HTTPException(status_code=403, detail="Patient-device mismatch")

    # 4. Check if the token matches
    if device_info["token"] != token:
        raise HTTPException(status_code=401, detail="Invalid token")

    return True