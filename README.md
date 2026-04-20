# ELEC0138 Security and Privacy: Healthcare IoMT Pipeline

This repository contains the Proof-of-Concept (PoC) code and data analysis for our ELEC0138 Project: **Resilient Security in Home Healthcare IoMT: "Cry Wolf" Attacks vs. AI Dual-Layer Gateways**.

## 📁 Repository Structure

*   `/Red_Team_Attack/`
    *   Contains the Python scripts used to simulate the Adversarial Data Poisoning ("Cry Wolf") and Privilege Escalation (BOLA) attacks.
*   `/Blue_Team_Defense/`
    *   Contains the FastAPI-based Dual-Layer Sanitization Gateway, including Zero-Trust access controls and the lightweight ML anomaly detection logic.
*   `/Data_Analysis/`
    *   Contains the feature extraction scripts and Jupyter notebooks used for evaluating the baseline dataset and the Latency vs. Accuracy trade-offs.

## 🚀 How to Run the Simulation

1.  **Start the Blue Team Gateway:**
    Navigate to the `/Blue_Team_Defense/` directory and run the FastAPI server.
2.  **Launch the Red Team Attack:**
    Navigate to the `/Red_Team_Attack/` directory and execute `final_attack.py` to inject the adversarial payloads (280 BPM) into the pipeline.
3.  **View the Audit Logs:**
    The gateway console will display the interception logs (e.g., `[BLOCKED] Semantic Anomaly Detected`).

*Disclaimer: All attacks simulated in this repository were performed in an isolated, local localhost environment in strict accordance with the ethical hacking guidelines provided in Week 1 of ELEC0138.*
