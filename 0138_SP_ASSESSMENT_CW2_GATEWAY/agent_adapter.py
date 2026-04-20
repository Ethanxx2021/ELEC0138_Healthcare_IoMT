import time
from schema import AgentDecision

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
target_path = os.path.join(repo_root, "0138_SP_ASSESSMENT_CW2_AI")

if target_path not in sys.path:
    sys.path.append(target_path)

# 
from main_gateway import DualLayerDefenseGateway


def load_agent_mode():
    try:
        with open("agent_mode.txt", "r", encoding="utf-8") as f:
            mode = f.read().strip()
            if mode in ["mock", "external"]:
                return mode
    except FileNotFoundError:
        pass
    return "mock"

# Current mode： "mock" or "external"
AGENT_MODE = load_agent_mode()

def save_agent_mode(mode: str):
    with open("agent_mode.txt", "w", encoding="utf-8") as f:
        f.write(mode)

# External model instance, avoiding re-initialization on every request.
external_gateway = None


def get_agent_mode():
    return AGENT_MODE


def set_agent_mode(mode: str):
    global AGENT_MODE
    if mode not in ["mock", "external"]:
        raise ValueError("mode must be 'mock' or 'external'")
    AGENT_MODE = mode
    save_agent_mode(mode)


def call_agent(agent_input: dict) -> AgentDecision:
    if AGENT_MODE == "mock":
        return call_mock_agent(agent_input)
    elif AGENT_MODE == "external":
        return call_external_agent(agent_input)
    else:
        raise ValueError(f"Unsupported AGENT_MODE: {AGENT_MODE}")


def call_mock_agent(agent_input: dict) -> AgentDecision:
    current_metrics = agent_input["current_payload"]["metrics"]
    baseline = agent_input["baseline_summary"]

    heart_rate = current_metrics["heart_rate"]
    spo2 = current_metrics["spo2"]
    baseline_hr = baseline["avg_heart_rate"] if baseline else None

    if baseline_hr is not None and heart_rate >= baseline_hr + 100 and spo2 >= 95:
        return AgentDecision(
            request_id=agent_input["request_id"],
            device_id=agent_input["current_payload"]["device_id"],
            is_attack=True,
            risk_level="high",
            recommended_action="block",
            confidence_score=0.95,
            caught_by="llm_agent_mock",
            latency_ms=1450.2,
            reasoning_log=(
                f"Heart rate spiked from baseline {baseline_hr} BPM to {heart_rate} BPM "
                f"while SpO2 remained stable at {spo2}%, suggesting likely falsified telemetry."
            )
        )

    return AgentDecision(
        request_id=agent_input["request_id"],
        device_id=agent_input["current_payload"]["device_id"],
        is_attack=False,
        risk_level="low",
        recommended_action="allow",
        confidence_score=0.88,
        caught_by="llm_agent_mock",
        latency_ms=920.5,
        reasoning_log="Telemetry appears broadly consistent with recent history and baseline."
    )


def convert_to_teammate_payload(agent_input: dict) -> dict:
    """
    Transfer agent_input to agent need payload
    """
    current_payload = agent_input["current_payload"]
    metrics = current_payload["metrics"]

    history_window = []
    for item in agent_input.get("recent_history", []):
        history_window.append({
            "heart_rate": item.get("heart_rate"),
            "spo2": item.get("spo2"),
            "systolic_bp": item.get("systolic_bp"),
            "diastolic_bp": item.get("diastolic_bp")
        })

    teammate_payload = {
        "request_id": agent_input["request_id"],
        "device_id": current_payload["device_id"],
        "current_data": {
            "metrics": {
                "heart_rate": metrics["heart_rate"],
                "spo2": metrics["spo2"],
                "systolic_bp": metrics["systolic_bp"],
                "diastolic_bp": metrics["diastolic_bp"]
            },
            "signal_quality": current_payload["signal_quality"]
        },
        "history_window": history_window
    }

    return teammate_payload


def convert_from_teammate_result(result: dict) -> AgentDecision:
    """

    """
    external_action = result["recommended_action"]

    # retain / discard -> allow / block
    if external_action == "retain":
        mapped_action = "allow"
    elif external_action == "discard":
        mapped_action = "block"
    else:
        mapped_action = "flag"

    return AgentDecision(
        request_id=result["request_id"],
        device_id=result["device_id"],
        is_attack=result["is_poisoned"],
        risk_level=result["risk_level"],
        recommended_action=mapped_action,
        confidence_score=result["confidence_score"],
        caught_by=result.get("caught_by", "external_model"),
        latency_ms=result["latency_ms"],
        reasoning_log=result["reasoning_log"]
    )


def get_external_gateway():
    global external_gateway
    if external_gateway is None:
        external_gateway = DualLayerDefenseGateway(llm_model_name="qwen2.5:1.5b")
    return external_gateway


def call_external_agent(agent_input: dict) -> AgentDecision:
    """
    Use external model
    """
    teammate_payload = convert_to_teammate_payload(agent_input)
    print("DEBUG teammate_payload =", teammate_payload)

    gateway = get_external_gateway()
    result = gateway.evaluate_telemetry(teammate_payload)
    print("DEBUG teammate_payload =", teammate_payload)

    return convert_from_teammate_result(result)