from main_gateway import DualLayerDefenseGateway

gateway = DualLayerDefenseGateway(llm_model_name="qwen2.5:1.5b")

payload = {
    # 把你 DEBUG 打印出来的 teammate_payload 原样贴进来
    "status": "processed",
  "request_id": "req_dev_001_1544",
  "device_id": "dev_001",
  "agent_decision": {
    "request_id": "req_dev_001_1544",
    "device_id": "dev_001",
    "is_attack": 'false',
    "risk_level": "low",
    "recommended_action": "allow",
    "confidence_score": 0.85,
    "caught_by": "none",
    "latency_ms": 6615.6397,
    "reasoning_log": "The physiological events observed in the current data (heart rate of 220, SpO2 at 97%) and signal quality (0.94) do not match any biologically impossible scenarios reported with sudden changes in blood pressure or oxygen saturation levels without corresponding heart rate fluctuations within a short time frame. The retention of this data is justified as it aligns with the patient's typical physiological patterns."
  },
  "policy_result": {
    "final_action": "allow",
    "quarantine_applied": 'false'
  },
  "log_written": 'true',
  "log_preview": {
    "logged_at": "2026-04-05T23:06:06.717969Z",
    "request_id": "req_dev_001_1544",
    "device_id": "dev_001",
    "patient_id": "pt_001",
    "timestamp": "2026-03-25T13:46:00Z",
    "metrics": {
      "heart_rate": 220,
      "spo2": 97,
      "systolic_bp": 118,
      "diastolic_bp": 76
    },
    "signal_quality": 0.94,
    "battery_level": 81,
    "seq_no": 1544,
    "agent_decision": {
      "is_attack": 'false',
      "risk_level": "low",
      "recommended_action": "allow",
      "confidence_score": 0.85,
      "caught_by": "none",
      "latency_ms": 6615.6397,
      "reasoning_log": "The physiological events observed in the current data (heart rate of 220, SpO2 at 97%) and signal quality (0.94) do not match any biologically impossible scenarios reported with sudden changes in blood pressure or oxygen saturation levels without corresponding heart rate fluctuations within a short time frame. The retention of this data is justified as it aligns with the patient's typical physiological patterns."
    },
    "policy_result": {
      "final_action": "allow",
      "quarantine_applied": 'false'
    }
}
}

result = gateway.evaluate_telemetry(payload)
print(result)