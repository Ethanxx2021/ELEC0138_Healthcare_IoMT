# 🛡️ ELEC0138 Security and Privacy: Healthcare IoMT Pipeline

> **Project Title:** Resilient Security in Home Healthcare IoMT: "Cry Wolf" Attacks vs. AI Dual-Layer Gateways  
> **Course:** ELEC0138 Security and Privacy (2025/2026) — University College London

## 📖 Executive Summary

This repository contains the full Red/Blue Team simulation codebase for our project. We demonstrate the critical vulnerabilities inherent in Medical IoMT data ingestion pipelines—specifically **Information Disclosure**, **Broken Object Level Authorization (BOLA)**, and **Adversarial Data Poisoning**—and propose a robust, GDPR-compliant **Dual-Layer Offline Sanitization Gateway** to mitigate these threats without compromising clinical availability.

---

## 📁 Repository Architecture

Our codebase is strictly segregated into three modular components to reflect the adversarial simulation workflow:

### 🔴 `/01_Red_Team_Attack/`

Contains the custom Python exploit suite developed to validate the STRIDE threat model.

- **`final_attack.py`** — Executes a multi-stage automated attack including Phase 1 (Baseline Ingestion), Phase 2 (BOLA / Privilege Escalation), and Phase 3 (High-frequency "Cry Wolf" Data Poisoning).
- **`poisoning_payload.json` & `sample_payload.json`** — Crafted adversarial and benign telemetry JSON payloads.

### 🔵 `/02_Blue_Team_Gateway_Tier1/`

The FastAPI-based Zero-Trust orchestration layer. It acts as the first line of defence.

- **Core Logic** — Handles schema validation (Pydantic), strict Device-to-Patient JWT binding, rate limiting, and blacklist/quarantine control.
- **Mitigation** — Directly neutralises the BOLA attacks demonstrated by the Red Team by verifying identity schemas before database ingestion.

### 🧠 `0138_SP_ASSESSMENT_CW2_AI`

The offline semantic sanitisation engine combining rule-based heuristics and local Large Language Models (LLMs) to ensure GDPR data sovereignty.

- **Tier 1.5 (`pre_filter.py`)** — An O(1) high-speed rule engine validating human physiological limits (e.g., dropping 280 BPM payloads in ~0.02 ms).
- **Tier 2 (`ai_agent.py`)** — A lightweight local LLM agent (`Qwen 2.5: 1.5B`) that cross-validates temporal sliding windows to detect stealthy data poisoning and prevent algorithmic hallucination in downstream Medical LLMs.

---

## ⚙️ Environment Setup & Dependencies

This system is designed to be lightweight and strictly localised for privacy compliance.

### 1. Install Python Dependencies

Requires Python 3.9 or higher.

```bash
pip install fastapi uvicorn requests pydantic
```

### 2. Deploy Local AI Engine (Ollama)

To ensure GDPR data minimisation and prevent PHI leakage to third-party clouds, Tier 2 requires a localised Ollama instance.

1. [Install Ollama](https://ollama.com/).
2. Pull and run the lightweight model:

```bash
ollama run qwen2.5:1.5b
```

> Type `/bye` to exit interactive mode. Ollama will continue running in the background at `http://localhost:11434`.

---

## 🚀 How to Run the Red/Blue Simulation

Follow these steps to reproduce the end-to-end attack and defence simulation.

### Step 1: Spin Up the Defence Gateway (Blue Team)

Open **Terminal 1** and navigate to the Gateway directory:

```bash
cd 02_Blue_Team_Gateway_Tier1
uvicorn app:app --reload
```

The Secure API Gateway is now listening on `http://127.0.0.1:8000`.

### Step 2: Launch the Exploit Suite (Red Team)

Open **Terminal 2** and navigate to the Attack directory:

```bash
cd 01_Red_Team_Attack
python final_attack.py
```

### Step 3: Observe the Interception (Audit Logs)

In **Terminal 1** (Gateway), observe the defensive routing in action:

| Phase | Behaviour | Response |
|-------|-----------|----------|
| Phase 1 — Normal | Benign payload ingested | `200 OK` |
| Phase 2 — BOLA | Intercepted at Tier 1 | `403 Forbidden: Device-Patient Mismatch` |
| Phase 3 — Poisoning | Blatant anomalies (e.g., 280 BPM) dropped by Tier 1.5 Pre-filter | Quarantined |

Sanitised audit logs are generated in JSON format, indicating the `confidence_score` and `reasoning_log` for quarantined malicious nodes.

---

## ⚖️ Ethical Disclaimer

All penetration testing, packet sniffing, and adversarial injections simulated in this repository were strictly confined to an isolated localhost environment. No real medical devices, hospital networks, or genuine patient data were targeted or compromised, fully adhering to the ethical hacking guidelines outlined in ELEC0138.
