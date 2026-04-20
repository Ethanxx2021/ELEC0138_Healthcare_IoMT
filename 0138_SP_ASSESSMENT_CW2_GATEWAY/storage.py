PATIENT_BASELINES = {
    "pt_001": {
        "avg_heart_rate": 78,
        "avg_spo2": 97,
        "avg_systolic_bp": 121,
        "avg_diastolic_bp": 79
    },
    "pt_002": {
        "avg_heart_rate": 72,
        "avg_spo2": 98,
        "avg_systolic_bp": 118,
        "avg_diastolic_bp": 76
    }
}


PATIENT_RECENT_HISTORY = {
    "pt_001": [
        {
            "heart_rate": 79,
            "spo2": 97,
            "systolic_bp": 120,
            "diastolic_bp": 80
        },
        {
            "heart_rate": 81,
            "spo2": 97,
            "systolic_bp": 119,
            "diastolic_bp": 78
        },
        {
            "heart_rate": 80,
            "spo2": 98,
            "systolic_bp": 121,
            "diastolic_bp": 79
        }
    ],
    "pt_002": [
        {
            "heart_rate": 71,
            "spo2": 98,
            "systolic_bp": 117,
            "diastolic_bp": 75
        },
        {
            "heart_rate": 73,
            "spo2": 99,
            "systolic_bp": 118,
            "diastolic_bp": 76
        }
    ]
}


def get_patient_baseline(patient_id: str):
    return PATIENT_BASELINES.get(patient_id)


def get_recent_history(patient_id: str):
    return PATIENT_RECENT_HISTORY.get(patient_id, [])