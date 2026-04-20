from datetime import datetime
from database import get_connection

REQUEST_LOGS = []


def write_log(payload, agent_decision, policy_result):
    log_entry = {
        "logged_at": datetime.utcnow().isoformat() + "Z",
        "request_id": agent_decision.request_id,
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
        "seq_no": payload.seq_no,
        "agent_decision": {
            "is_attack": agent_decision.is_attack,
            "risk_level": agent_decision.risk_level,
            "recommended_action": agent_decision.recommended_action,
            "confidence_score": agent_decision.confidence_score,
            "caught_by": agent_decision.caught_by,
            "latency_ms": agent_decision.latency_ms,
            "reasoning_log": agent_decision.reasoning_log
        },
        "policy_result": policy_result
    }

    REQUEST_LOGS.append(log_entry)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO audit_logs (
        logged_at, request_id, device_id, patient_id, payload_timestamp,
        heart_rate, spo2, systolic_bp, diastolic_bp,
        signal_quality, battery_level, seq_no,
        is_attack, risk_level, recommended_action, confidence_score,
        caught_by, latency_ms, reasoning_log,
        final_action, quarantine_applied
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        log_entry["logged_at"],
        log_entry["request_id"],
        log_entry["device_id"],
        log_entry["patient_id"],
        log_entry["timestamp"],
        log_entry["metrics"]["heart_rate"],
        log_entry["metrics"]["spo2"],
        log_entry["metrics"]["systolic_bp"],
        log_entry["metrics"]["diastolic_bp"],
        log_entry["signal_quality"],
        log_entry["battery_level"],
        log_entry["seq_no"],
        int(log_entry["agent_decision"]["is_attack"]),
        log_entry["agent_decision"]["risk_level"],
        log_entry["agent_decision"]["recommended_action"],
        log_entry["agent_decision"]["confidence_score"],
        log_entry["agent_decision"]["caught_by"],
        log_entry["agent_decision"]["latency_ms"],
        log_entry["agent_decision"]["reasoning_log"],
        log_entry["policy_result"]["final_action"],
        int(log_entry["policy_result"]["quarantine_applied"])
    ))

    conn.commit()
    conn.close()

    return log_entry


def get_all_logs():
    return REQUEST_LOGS

def clear_logs():
    REQUEST_LOGS.clear()