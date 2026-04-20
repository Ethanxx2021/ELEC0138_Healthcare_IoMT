from main_gateway import DualLayerDefenseGateway

gateway = DualLayerDefenseGateway(llm_model_name="qwen2.5:1.5b")

payload = {
    "request_id": "req_001",
    "device_id": "dev_001",
    "current_data": {
        "metrics": {"heart_rate": 185, "spo2": 98},
        "signal_quality": 0.95
    },
    "history_window": [
        {"heart_rate": 72, "spo2": 98},
        {"heart_rate": 74, "spo2": 98}
    ]
}

result = gateway.evaluate_telemetry(payload)
print(result)