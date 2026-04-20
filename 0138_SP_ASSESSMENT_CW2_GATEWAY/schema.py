from pydantic import BaseModel


class Metrics(BaseModel):
    heart_rate: int
    spo2: int
    systolic_bp: int
    diastolic_bp: int


class HealthDataPayload(BaseModel):
    device_id: str
    patient_id: str
    timestamp: str
    metrics: Metrics
    signal_quality: float
    battery_level: int
    seq_no: int
    token: str


class AgentDecision(BaseModel):
    request_id: str
    device_id: str
    is_attack: bool
    risk_level: str
    recommended_action: str
    confidence_score: float
    caught_by: str
    latency_ms: float
    reasoning_log: str