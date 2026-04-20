# 🛡️ ELEC0138: Resilient Security in Home Healthcare IoMT

> **Project Title:** "Cry Wolf" Attacks vs. AI Dual-Layer Gateways in Medical Data Ingestion Pipelines  
> **Course:** ELEC0138 Security and Privacy (2025/2026) - University College London

## 📖 Executive Summary
This repository contains the full Red/Blue Team simulation codebase for our project. We demonstrate the vulnerabilities inherent in IoMT data ingestion pipelines (e.g., **Information Disclosure**, **BOLA/Privilege Escalation**, and **Adversarial Data Poisoning**) and propose a robust, GDPR-compliant **Dual-Layer Offline Sanitization Gateway** to mitigate these threats without compromising clinical availability.

---

## 📁 Repository Architecture

To reflect the adversarial simulation workflow, our codebase is strictly segregated into three modular components:

### 🔴 1. `/01_Red_Team_Attack/`
Contains the custom Python exploit suite developed to validate the STRIDE threat model.
*   **`final_attack.py`**: Executes a multi-stage attack including Phase 1 (Baseline), Phase 2 (BOLA/Privilege Escalation), and Phase 3 (High-frequency "Cry Wolf" Data Poisoning).
*   **`poisoning_payload.json` & `sample_payload.json`**: Crafted adversarial and benign telemetry payloads.

### 🔵 2. `/02_Blue_Team_Gateway_Tier1/`
The FastAPI-based Zero-Trust orchestration layer. It acts as the first line of defence.
*   **Core Logic**: Handles schema validation (Pydantic), strict Device-to-Patient JWT binding, rate limiting, and blacklist/quarantine control.
*   **Mitigation**: Directly neutralizes the BOLA attacks demonstrated by the Red Team.

### 🧠 3. `/03_Blue_Team_AI_Auditor_Tier2/`
The offline semantic sanitization engine combining rule-based heuristics and local Large Language Models (LLMs) to ensure GDPR data sovereignty.
*   **Tier 1.5 (`pre_filter.py`)**: An $O(1)$ high-speed rule engine validating human physiological limits (e.g., dropping 280 BPM payloads in ~0.02ms).
*   **Tier 2 (`ai_agent.py`)**: A lightweight local LLM agent (`Qwen 2.5 1.5B`) that cross-validates temporal sliding windows to detect stealthy data poisoning.

---

## ⚙️ Environment Setup & Dependencies

This system is designed to be lightweight and strictly localised for privacy compliance.

**1. Install Python Dependencies:**
Requires Python 3.9+.
```bash
pip install fastapi uvicorn requests pydantic

2. Deploy Local AI Engine (Ollama):
To ensure GDPR data minimization and prevent PHI leakage to third-party clouds, Tier 2 requires a localized Ollama instance.

Install Ollama.

Pull and run the lightweight model in your terminal:

code
Bash
download
content_copy
expand_less
ollama run qwen2.5:1.5b

(Type /bye to let it run silently in the background at http://localhost:11434)

🚀 How to Run the Red/Blue Simulation

Follow these steps to reproduce our end-to-end attack and defence simulation:

Step 1: Spin up the Defense Gateway (Blue Team)
Open Terminal 1 and navigate to the Gateway directory:

code
Bash
download
content_copy
expand_less
cd 02_Blue_Team_Gateway_Tier1
uvicorn app:app --reload

The Secure API Gateway is now listening on http://127.0.0.1:8000.

Step 2: Launch the Exploit Suite (Red Team)
Open Terminal 2 and navigate to the Attack directory:

code
Bash
download
content_copy
expand_less
cd 01_Red_Team_Attack
python final_attack.py

Step 3: Observe the Interception (Audit Logs)
In Terminal 1 (Gateway), observe the defensive routing in action:

BOLA attacks will be intercepted at Tier 1 (403 Forbidden: Device-Patient Mismatch).

Blatant Data Poisoning (e.g., 280 BPM) will be instantly dropped by the Tier 1.5 Pre-filter.

The sanitized audit logs will be generated in JSON format, indicating the confidence_score and reasoning_log for quarantined malicious nodes.

⚖️ Ethical Disclaimer

All penetration testing, packet sniffing, and adversarial injections simulated in this repository were strictly confined to a local localhost environment. No real medical devices, hospital networks, or genuine patient data were targeted or compromised, fully adhering to the ethical hacking guidelines outlined in ELEC0138.

3. 传完代码后，点击 GitHub 页面看看效果，这份主页简直是“大厂开源项目”级别的排面！稳了！🍻
