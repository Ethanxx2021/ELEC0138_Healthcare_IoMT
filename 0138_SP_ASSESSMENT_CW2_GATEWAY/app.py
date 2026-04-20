from fastapi import FastAPI
from schema import HealthDataPayload
from auth import verify_device_and_token
from rate_limit import check_rate_limit, reset_rate_limit
from blacklist import check_blacklist, remove_from_blacklist, clear_blacklist
from context_builder import build_agent_input
from agent_adapter import call_agent
from policy import execute_policy
from logs import write_log, get_all_logs, clear_logs
from agent_adapter import call_agent, get_agent_mode, set_agent_mode
from test_cases import TEST_CASES
from database import init_db

app = FastAPI(title="IoMT AI Security Gateway")

init_db()

@app.get("/")
def root():
    return {"message": "Gateway is running"}


@app.get("/logs")
def read_logs():
    return {"logs": get_all_logs()}

@app.get("/log-summary")
def log_summary():
    logs = get_all_logs()

    summary = []
    for entry in logs:
        summary.append({
            "request_id": entry["request_id"],
            "device_id": entry["device_id"],
            "heart_rate": entry["metrics"]["heart_rate"],
            "spo2": entry["metrics"]["spo2"],
            "is_attack": entry["agent_decision"]["is_attack"],
            "risk_level": entry["agent_decision"]["risk_level"],
            "recommended_action": entry["agent_decision"]["recommended_action"],
            "final_action": entry["policy_result"]["final_action"],
            "latency_ms": entry["agent_decision"]["latency_ms"]
        })

    return {"summary": summary}

@app.get("/test-cases")
def list_test_cases():
    return {"test_cases": TEST_CASES}

@app.get("/agent-mode")
def read_agent_mode():
    return {"agent_mode": get_agent_mode()}

@app.post("/agent-mode/{mode}")
def update_agent_mode(mode: str):
    set_agent_mode(mode)
    return {"agent_mode": get_agent_mode()}


@app.post("/admin/unblacklist/{device_id}") ##临时测试接口，实际部署时需要更严格的权限控制
def unblacklist_device(device_id: str): #POST /admin/unblacklist/dev_001
    remove_from_blacklist(device_id)
    return {
        "status": "removed_from_blacklist",
        "device_id": device_id
    }

@app.post("/admin/reset-state")
def reset_state():
    clear_blacklist()
    reset_rate_limit()
    clear_logs()
    return {"status": "reset_done"}

@app.post("/api/v1/health-data")
def receive_health_data(payload: HealthDataPayload):
    # 1. Blacklist check
    check_blacklist(payload.device_id)

    # 2. identity and token verification
    verify_device_and_token(
        device_id=payload.device_id,
        patient_id=payload.patient_id,
        token=payload.token
    )

    # 3. Rate limit check
    check_rate_limit(payload.device_id)

    # 4. Build Agent input
    agent_input = build_agent_input(payload)

    # 5. Call Agent
    agent_decision = call_agent(agent_input)

    # 6. Execute policy
    policy_result = execute_policy(agent_decision)

    # 7. Write log
    log_entry = write_log(payload, agent_decision, policy_result)

    return {
        "status": "processed",
        "request_id": agent_decision.request_id,
        "device_id": agent_decision.device_id,
        "agent_decision": agent_decision.dict(),
        "policy_result": policy_result,
        "log_written": True,
        "log_preview": log_entry
    }