# Project name: agentic-soc-triage
# Security Fusion Centre: Incident Triage & Operational Analytics Engine

An automated incident triage, SLA routing, and operational analytics pipeline modeled for modern **Security Fusion Centres** protecting **Financial Markets Infrastructure (FMI)**. 

This engine ingests multi-source security feeds across **Cyber Security, Financial Crime, Physical Security, and Threat Intelligence**, evaluates compound threat risk against business asset criticality, dynamically routes incidents to Tier 1 (L1) or Tier 2 (L2) queues with risk-based SLAs, and generates both an auditable compliance log (`.csv`) and an executive operational insight report (`.json`).

---

## 🎯 Project Overview & Business Value
In high-consequence, regulated financial institutions (such as the London Stock Exchange Group), operational resilience requires a converged Fusion view. Disjointed alert queues and manual triage slow down Mean Time to Respond (MTTR) and obscure multi-vector attacks.

This project addresses those challenges by providing:
* **Multi-Discipline Fusion Triage:** Ingests and correlates events across Cyber Security, Financial Crime / Fraud, Physical Security (badge access anomalies), and External Threat Intelligence.
* **Context-Aware FMI Escalation:** Protects critical financial assets (e.g., FIX trading gateways, settlement networks) by auto-escalating medium-severity anomalies into Tier 2 queues when critical infrastructure is targeted.
* **Operational SLA Capacity Management:** Quantifies analyst workload commitments in real-time ($15\text{m} \rightarrow 120\text{m}$ SLA brackets) to assist SOC leadership in queue balancing and shift staffing.
* **Regulatory Compliance & Auditability:** Produces an immutable, structured decision log supporting audits under **DORA**, **FCA / PRA**, and **SOC 2 Type II**.

---

## 🏗️ Architecture & Pipeline Flow

```
[ sample_alerts.json ] ── Multi-Discipline Feeds (Cyber, FinCrime, Physical, Threat Intel)
         │
         ▼
[ load_alerts() ]       ── Defensive parsing, schema verification, and exception handling
         │
         ▼
[ triage_alerts() ]     ── Multi-factor evaluation (Severity + FMI Asset Criticality)
         │                 Assigns: Assigned Tier, Target SLA, Contextual Rationale
         ├──► [ export_decision_log() ]           ── Auditable CSV (triage_decision_log.csv)
         │
         └──► [ generate_operational_insights() ] ── Analytics JSON (fusion_operational_insights.json)
                         │
                         ▼
             [ Executive Terminal Dashboard ]    ── Real-time Fusion metrics & action recommendations
```

---

## ⚙️ Multi-Discipline Triage & SLA Matrix

| Discipline | Severity | Critical Asset (FMI) | Assigned Tier | Target SLA | Operational Triage Rationale |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Cyber Security** | Critical | **Yes** | **Tier 2 (L2)** | **15 mins** | Immediate containment of high-consequence asset threats |
| **Financial Crime** | High | **Yes** | **Tier 2 (L2)** | **30 mins** | Urgent wire / settlement transaction fraud escalation |
| **Physical Security** | High | **Yes** | **Tier 2 (L2)** | **30 mins** | Physical badge access correlated with active remote sessions |
| **Cyber Security** | Medium | **Yes** | **Tier 2 (L2)** | **60 mins** | **Escalated:** Medium severity targeting critical trading system |
| **Threat Intel** | Medium | No | **Tier 1 (L1)** | **60 mins** | Standard external credential leak validation playbook |
| **Cyber Security** | Low | No | **Tier 1 (L1)** | **120 mins** | Standard baseline false-positive filtering / port scan review |

---

## 📁 Repository Structure

```text
agentic-soc-triage/
├── sample_alerts.json                # Multi-discipline Fusion Centre mock feed
├── triage_engine.py                  # Core engine: Ingestion, Triage, CSV Log, and Analytics
├── triage_decision_log.csv           # Immutable audit log with full operational decision rationale
├── fusion_operational_insights.json  # Machine-readable executive operational analytics report
└── README.md                         # Project documentation and architecture guide
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8+ (Zero external dependencies; uses standard library modules `json`, `csv`, `os`).

### Running the Pipeline
```bash
# Clone the repository
git clone https://github.com/usman-masthan/agentic-soc-triage.git
cd agentic-soc-triage

# Run the complete triage and analytics pipeline
python3 triage_engine.py
```

### Live Terminal Output
```text
[Debug] Starting file ingestion for sample_alerts.json
[Debug] Successfully loaded 8 alerts from sample_alerts.json

[DEBUG] Starting triage evaluation for 8 Fusion alerts...
[DEBUG] [Cyber Security] FUS-001 -> Assigned: Tier 2 (L2) | SLA: 15 mins
[DEBUG] [Cyber Security] FUS-002 -> Assigned: Tier 2 (L2) | SLA: 30 mins
[DEBUG] [Cyber Security] FUS-003 -> Assigned: Tier 2 (L2) | SLA: 15 mins
[DEBUG] [Financial Crime] FUS-004 -> Assigned: Tier 2 (L2) | SLA: 30 mins
[DEBUG] [Physical Security] FUS-005 -> Assigned: Tier 2 (L2) | SLA: 30 mins
[DEBUG] [Cyber Security] FUS-006 -> Assigned: Tier 2 (L2) | SLA: 60 mins
[DEBUG] [Threat Intelligence] FUS-007 -> Assigned: Tier 1 (L1) | SLA: 60 mins
[DEBUG] [Cyber Security] FUS-008 -> Assigned: Tier 1 (L1) | SLA: 120 mins

[DEBUG] Exporting decision log to: triage_decision_log.csv...
[DEBUG] Success: Safely wrote 8 audit rows to 'triage_decision_log.csv'.

[DEBUG] Computing Fusion operational analytics and workload metrics...
[DEBUG] Operational insights saved to 'fusion_operational_insights.json'.

=======================================================
      LSEG SECURITY FUSION CENTRE - OPERATIONAL INSIGHTS      
=======================================================
 Total Alerts Processed       : 8
 Tier 1 (L1) Queue Routed     : 2
 Tier 2 (L2) Queue Escalated  : 6 (75.0%)
 Critical FMI Asset Incidents : 5 (62.5%)
 Total Committed SLA Capacity : 6.0 analyst-hours
-------------------------------------------------------
 Discipline Breakdown:
   • Cyber Security            : 5 alert(s)
   • Financial Crime           : 1 alert(s)
   • Physical Security         : 1 alert(s)
   • Threat Intelligence       : 1 alert(s)
-------------------------------------------------------
 Key Actionable Insights:
   [!] Allocate immediate L2 staffing: 6 incidents (75.0%) require senior response within expedited SLAs.
   [!] FMI Safeguard: 5 incidents target critical financial assets, requiring joint review with Infrastructure Engineering.
   [!] Cross-Discipline Alignment: Review alerts originating from Cyber Security, Financial Crime, Physical Security, Threat Intelligence.
=======================================================
 Audit Log File               : triage_decision_log.csv
 Analytics Report File        : fusion_operational_insights.json
=======================================================
```

---

## 🛡️ Future Roadmap
* **Threat Intelligence API Integration:** Query VirusTotal / AbuseIPDB endpoints to enrich IOCs dynamically.
* **SOAR Webhook Dispatch:** Emulate Splunk SOAR / Tines webhook actions to push escalated incidents directly into Jira Service Management or PagerDuty.
* **Unit Testing Suite:** Implement automated tests with `pytest` to continuously validate routing boundaries and edge cases.