# 🏛️ Project Sovereign: The Autonomous Supply Chain Boardroom

### 🏆 Built for the IBM watsonx Challenge
**Powered by IBM Granite-4-h-small**

---

## 📖 The Problem
Modern supply chains are fragile. Decisions about logistics, budget, and code integration often take days because they require coordination between different human departments (Finance, Operations, Engineering). This latency causes delays and financial loss.

## 💡 The Solution
**Project Sovereign** is an autonomous "AI Boardroom" that replaces slow manual coordination with intelligent multi-agent debate. 

Instead of a single chatbot, Sovereign instantiates **three distinct AI Agents** using the **IBM Granite-4-h-small** model. They analyze every proposal in real-time:

1.  **👨‍💻 Chief Architect:** Analyzes code stability, security, and technical debt.
2.  **💰 CFO (Finance):** Analyzes budget impact, ROI, and financial risk.
3.  **🚚 COO (Operations):** Analyzes logistics speed, supply chain efficiency, and timelines.

Finally, a **👑 CEO Agent** listens to their debate and issues a final, binding **"Executive Decree"** (APPROVED or REJECTED).

---

## ⚙️ How It Works (The Architecture)

The system is built on **IBM watsonx.ai** using the `ibm-watson-machine-learning` SDK.

1.  **Input:** A user submits a supply chain proposal (e.g., "Automate logistics using AI").
2.  **Multi-Agent Debate:** The Python engine cycles through the agent personas, sending the prompt to the **Granite-4-h-small** deployment with specific "System Instructions" for each role.
3.  **Synthesis:** The Agents' responses are collected into a "Meeting Minute" log.
4.  **Decision:** The "CEO" model reads the minutes and makes a logic-based decision based on the consensus or conflict found in the debate.

---

## 📸 Proof of Concept

### Scenario A: Risky Proposal (Rejected)
*Proposal: "Replace all humans with AI immediately."*
* **Architect:** Warns about security risks.
* **CFO:** Warns about high initial cost.
* **CEO Decision:** **REJECTED** due to excessive risk.

### Scenario B: Safe Proposal (Approved)
*Proposal: "Use AI to assist humans with data entry."*
* **Architect:** Approves (low technical risk).
* **COO:** Approves (high efficiency gain).
* **CEO Decision:** **APPROVED** for immediate implementation.

---

## 🛠️ Technology Stack
* **Model:** IBM Granite-4-h-small (v2026-01-30)
* **Platform:** IBM Cloud (watsonx.ai)
* **Language:** Python 3.10
* **Authentication:** IBM Cloud IAM (Identity and Access Management)

## 🚀 How to Run
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set your IBM Cloud API Key in `boardroom.py`.
4. Run the simulation: `python boardroom.py`

---
*Created by Rushikesh Goud for the IBM watsonx Hackathon 2026.*