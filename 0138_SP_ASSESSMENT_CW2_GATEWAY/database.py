import sqlite3

DB_NAME = "gateway.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        logged_at TEXT,
        request_id TEXT,
        device_id TEXT,
        patient_id TEXT,
        payload_timestamp TEXT,
        heart_rate INTEGER,
        spo2 INTEGER,
        systolic_bp INTEGER,
        diastolic_bp INTEGER,
        signal_quality REAL,
        battery_level INTEGER,
        seq_no INTEGER,
        is_attack INTEGER,
        risk_level TEXT,
        recommended_action TEXT,
        confidence_score REAL,
        caught_by TEXT,
        latency_ms REAL,
        reasoning_log TEXT,
        final_action TEXT,
        quarantine_applied INTEGER
    )
    """)

    conn.commit()
    conn.close()