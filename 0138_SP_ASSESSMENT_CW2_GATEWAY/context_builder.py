from storage import get_patient_baseline, get_recent_history


def build_agent_input(payload):
    baseline = get_patient_baseline(payload.patient_id)
    recent_history = get_recent_history(payload.patient_id)

    agent_input = {
        "request_id": f"req_{payload.device_id}_{payload.seq_no}",
        "current_payload": {
            "device_id": payload.device_id,
            "patient_id": payload.patient_id,
            "timestamp": payload.timestamp,
            "metrics": {
                "heart_rate": payload.metrics.heart_rate,
                "spo2": payload.metrics.spo2,
                "systolic_bp": payload.metrics.systolic_bp,
                "diastolic_bp": payload.metrics.diastolic_bp
            },
            "signal_quality": payload.signal_quality,
            "battery_level": payload.battery_level,
            "seq_no": payload.seq_no
        },
        "baseline_summary": baseline,
        "recent_history": recent_history
    }

    return agent_input