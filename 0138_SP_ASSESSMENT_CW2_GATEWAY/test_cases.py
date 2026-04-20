TEST_CASES = [
    {
        "name": "normal_case",
        "description": "Valid telemetry consistent with baseline",
        "payload": {
            "device_id": "dev_001",
            "patient_id": "pt_001",
            "timestamp": "2026-03-25T13:45:00Z",
            "metrics": {
                "heart_rate": 82,
                "spo2": 97,
                "systolic_bp": 118,
                "diastolic_bp": 76
            },
            "signal_quality": 0.94,
            "battery_level": 81,
            "seq_no": 1543,
            "token": "VALID_TOKEN_DEV1"
        },
        "expected": "allow"
    },
    {
        "name": "poisoning_case",
        "description": "Extreme HR spike while other metrics remain stable",
        "payload": {
            "device_id": "dev_001",
            "patient_id": "pt_001",
            "timestamp": "2026-03-25T13:46:00Z",
            "metrics": {
                "heart_rate": 230,
                "spo2": 97,
                "systolic_bp": 118,
                "diastolic_bp": 76
            },
            "signal_quality": 0.94,
            "battery_level": 81,
            "seq_no": 1544,
            "token": "VALID_TOKEN_DEV1"
        },
        "expected": "block_and_quarantine"
    },
    {
        "name": "invalid_token_case",
        "description": "Wrong token for a registered device",
        "payload": {
            "device_id": "dev_001",
            "patient_id": "pt_001",
            "timestamp": "2026-03-25T13:47:00Z",
            "metrics": {
                "heart_rate": 82,
                "spo2": 97,
                "systolic_bp": 118,
                "diastolic_bp": 76
            },
            "signal_quality": 0.94,
            "battery_level": 81,
            "seq_no": 1545,
            "token": "INVALID_TOKEN"
        },
        "expected": "401"
    },
    {
        "name": "unknown_device_case",
        "description": "Unregistered device tries to send telemetry",
        "payload": {
            "device_id": "dev_999",
            "patient_id": "pt_001",
            "timestamp": "2026-03-25T13:48:00Z",
            "metrics": {
                "heart_rate": 82,
                "spo2": 97,
                "systolic_bp": 118,
                "diastolic_bp": 76
            },
            "signal_quality": 0.94,
            "battery_level": 81,
            "seq_no": 1546,
            "token": "some_token"
        },
        "expected": "403"
    },
    {
        "name": "patient_mismatch_case",
        "description": "Registered device bound to wrong patient",
        "payload": {
            "device_id": "dev_001",
            "patient_id": "pt_999",
            "timestamp": "2026-03-25T13:49:00Z",
            "metrics": {
                "heart_rate": 82,
                "spo2": 97,
                "systolic_bp": 118,
                "diastolic_bp": 76
            },
            "signal_quality": 0.94,
            "battery_level": 81,
            "seq_no": 1547,
            "token": "VALID_TOKEN_DEV1"
        },
        "expected": "403"
    }
]