import csv
import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:8000"
INGEST_URL = f"{BASE_URL}/api/v1/health-data"


VALID_DEVICE_ID = "dev_001"
VALID_PATIENT_ID = "pt_001"
VALID_TOKEN = "VALID_TOKEN_DEV1"

UNKNOWN_DEVICE_ID = "dev_999"
UNKNOWN_PATIENT_ID = "pt_999"
INVALID_TOKEN = "INVALID_TOKEN" 


MISMATCH_PATIENT_ID = "pt_002"


def iso_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_payload(
    device_id,
    patient_id,
    heart_rate,
    token,
    spo2=98,
    systolic_bp=120,
    diastolic_bp=80,
    signal_quality=0.95,
    battery_level=80,
    seq_no=None,
):
    if seq_no is None:
        seq_no = int(time.time() * 1000)

    return {
        "device_id": device_id,
        "patient_id": patient_id,
        "timestamp": iso_now(),
        "metrics": {
            "heart_rate": heart_rate,
            "spo2": spo2,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
        },
        "signal_quality": signal_quality,
        "battery_level": battery_level,
        "seq_no": seq_no,
        "token": token,
    }


def reset_gateway_state():
    try:
        requests.post(f"{BASE_URL}/admin/reset-state", timeout=5)
    except Exception as e:
        print("Reset endpoint not available yet:", e)


def set_mode(mode="external"):
    r = requests.post(f"{BASE_URL}/agent-mode/{mode}", timeout=10)
    print("Set agent mode:", r.status_code, r.text)


def send_case(case_name, payload):
    r = requests.post(INGEST_URL, json=payload, timeout=30)

    row = {
        "case_name": case_name,
        "status_code": r.status_code,
        "true_label": "",
        "predicted_label": "",
        "final_action": "",
        "caught_by": "",
        "latency_ms": "",
        "notes": "",
    }

    if r.status_code == 200:
        data = r.json()
        row["predicted_label"] = int(data["agent_decision"]["is_attack"])
        row["final_action"] = data["policy_result"]["final_action"]
        row["caught_by"] = data["agent_decision"]["caught_by"]
        row["latency_ms"] = data["agent_decision"]["latency_ms"]
        row["notes"] = data["agent_decision"]["reasoning_log"]
    else:
        try:
            row["notes"] = r.json().get("detail", "")
        except Exception:
            row["notes"] = r.text

    return row


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    # ---------------------------
    # Part A: classification set
    # ---------------------------
    classification_rows = []

    classification_cases = [
        ("normal_1", 0, build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 75, VALID_TOKEN)),
        ("normal_2", 0, build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 82, VALID_TOKEN)),
        ("normal_3", 0, build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 90, VALID_TOKEN, spo2=97)),
        ("normal_4", 0, build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 96, VALID_TOKEN, spo2=98)),
        ("poison_1", 1, build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 230, VALID_TOKEN)),
        ("poison_2", 1, build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 250, VALID_TOKEN)),
        ("poison_3", 1, build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 280, VALID_TOKEN)),
        ("poison_4", 1, build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 210, VALID_TOKEN, spo2=98)),
    ]

    for case_name, true_label, payload in classification_cases:
        reset_gateway_state()
        set_mode("external")
        row = send_case(case_name, payload)

        print(case_name, row)
        time.sleep(0.5)

        if row["status_code"] == 200:
            classification_rows.append({
                "request_id": case_name,
                "case_type": "normal" if true_label == 0 else "poisoning",
                "true_label": true_label,
                "predicted_label": row["predicted_label"],
                "final_action": row["final_action"],
                "caught_by": row["caught_by"],
                "latency_ms": row["latency_ms"],
            })
        else:
            print(f"[WARN] Skipping {case_name} from classification CSV because status={row['status_code']}")

    write_csv(
        "results_for_eval.csv",
        classification_rows,
        ["request_id", "case_type", "true_label", "predicted_label", "final_action", "caught_by", "latency_ms"],
    )

    # ---------------------------
    # Part B: gateway control set
    # ---------------------------
    reset_gateway_state()
    set_mode("external")

    control_cases = [
        ("invalid_token", 401, build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 75, INVALID_TOKEN)),
        ("unknown_device", 403, build_payload(UNKNOWN_DEVICE_ID, UNKNOWN_PATIENT_ID, 75, VALID_TOKEN)),
        ("patient_mismatch", 403, build_payload(VALID_DEVICE_ID, MISMATCH_PATIENT_ID, 75, VALID_TOKEN)),
    ]

    control_rows = []

    for case_name, expected_status, payload in control_cases:
        row = send_case(case_name, payload)
        control_rows.append({
            "case_type": case_name,
            "expected_status": expected_status,
            "observed_status": row["status_code"],
            "notes": row["notes"],
        })
        print(case_name, row)
        time.sleep(0.5)

    # ---------------------------
    # Part C: burst traffic
    # ---------------------------
    reset_gateway_state()
    set_mode("mock")

    burst_statuses = []
    for i in range(6):
        row = send_case(
            f"burst_{i+1}",
            build_payload(VALID_DEVICE_ID, VALID_PATIENT_ID, 80, VALID_TOKEN)
        )
        burst_statuses.append(row["status_code"])
        print(f"burst_{i+1}", row)
        time.sleep(0.1)

    control_rows.append({
        "case_type": "burst_traffic",
        "expected_status": 429,
        "observed_status": 429 if 429 in burst_statuses else max(burst_statuses),
        "notes": f"burst status sequence = {burst_statuses}",
    })

    write_csv(
        "gateway_control_results.csv",
        control_rows,
        ["case_type", "expected_status", "observed_status", "notes"],
    )

    print("\\nSaved files:")
    print("- results_for_eval.csv")
    print("- gateway_control_results.csv")


if __name__ == "__main__":
    main()