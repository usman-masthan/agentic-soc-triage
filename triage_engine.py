import json # Import the built in json library to read and write json files
import os # Import the built in os library to interact with the operating system
import csv  # Imports Python's built-in CSV module for handling tabular data exports

def load_alerts(file_path):
    """
    load and parse alerts from json file"""

    print(f"[Debug] Starting file ingestion for {file_path}")

    try:
        with open(
            file_path, "r", encoding="utf-8"
        )as f:
            alerts = (json.load(f))
            print(f"[Debug] Successfully loaded {len(alerts)} alerts from {file_path}")

        if not isinstance(alerts, list):
            print(f"[Error] The loaded data is not a list. Please check the file format.")
            return ([])

        return (alerts)
    
    except FileNotFoundError:
        print(f"[Error] File not found: {file_path}")
        return ([])
    except json.JSONDecodeError:
        print(f"[Error] Failed to decode JSON from file: {file_path}")
        return ([])
    except Exception as e:
        print(f"[Error] An unexpected error occurred while loading alerts: {e}")
        return ([])
    
def triage_alerts(alerts_list):  # Defines the triage function and accepts a list of alert dictionaries
    """
    Evaluates multi-discipline Fusion alerts, assigns L1/L2 routing, target SLA, and contextual rationale.
    """
    print(f"\n[DEBUG] Starting triage evaluation for {len(alerts_list)} Fusion alerts...")
    triaged_records = []

    for alert in alerts_list:
        alert_copy = alert.copy()
        discipline = alert_copy.get("discipline", "General Security")
        severity = alert_copy.get("severity", "").upper()
        is_critical = alert_copy.get("is_critical_asset", False)
        alert_id = alert_copy.get("alert_id", "UNKNOWN")

        # 1. Routing & Rationale Determination (Context-Aware Fusion Logic)
        if severity in ["CRITICAL", "HIGH"]:
            tier = "Tier 2 (L2)"
            if is_critical:
                reason = f"Critical FMI Asset alert ({discipline}): {severity.capitalize()} severity requires immediate L2 escalation."
            else:
                reason = f"{discipline} alert: {severity.capitalize()} severity requires senior analyst investigation."
        elif severity == "MEDIUM" and is_critical:
            tier = "Tier 2 (L2)"
            reason = f"Escalated: Medium severity {discipline} event directly impacting critical FMI infrastructure."
        else:
            tier = "Tier 1 (L1)"
            reason = f"Standard baseline triage for {discipline.lower()} event."

        # 2. SLA Assignment based on urgency
        if severity == "CRITICAL":
            sla = "15 mins"
            sla_mins = 15
        elif severity == "HIGH":
            sla = "30 mins"
            sla_mins = 30
        elif severity == "MEDIUM":
            sla = "60 mins"
            sla_mins = 60
        else:
            sla = "120 mins"
            sla_mins = 120

        # Inject enriched metadata
        alert_copy["assigned_tier"] = tier
        alert_copy["target_sla"] = sla
        alert_copy["sla_minutes"] = sla_mins
        alert_copy["triage_reason"] = reason

        print(f"[DEBUG] [{discipline}] {alert_id} -> Assigned: {tier} | SLA: {sla}")
        triaged_records.append(alert_copy)

    return triaged_records


def export_decision_log(triaged_data, output_file_path):
    """Exports triaged alerts into a structured, auditable CSV log file."""
    print(f"\n[DEBUG] Exporting decision log to: {output_file_path}...")

    if not triaged_data:
        print("[WARNING] No triaged records provided to export. Aborting write operation.")
        return False

    fieldnames = [
        "alert_id",
        "timestamp",
        "discipline",
        "rule_name",
        "severity",
        "is_critical_asset",
        "source_ip",
        "target_user",
        "assigned_tier",
        "target_sla",
        "triage_reason",
    ]

    try:
        with open(output_file_path, mode="w", newline="", encoding="utf-8") as f:
            # We exclude helper calculations like 'sla_minutes' from raw audit log
            filtered_rows = [
                {k: row.get(k, "") for k in fieldnames} for row in triaged_data
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)

        print(f"[DEBUG] Success: Safely wrote {len(triaged_data)} audit rows to '{output_file_path}'.")
        return True

    except (IOError, OSError) as e:
        print(f"[ERROR] Failed to write decision log to disk.\nDetails: {e}")
        return False


def generate_operational_insights(triaged_data, report_file_path="fusion_operational_insights.json"):
    """
    Transforms triage data into high-level operational trends, SLA workloads,
    and actionable Fusion Centre insights for executive reporting.
    """
    print(f"\n[DEBUG] Computing Fusion operational analytics and workload metrics...")

    total_alerts = len(triaged_data)
    if total_alerts == 0:
        return {}

    # Discipline Breakdown
    discipline_counts = {}
    for alert in triaged_data:
        disc = alert.get("discipline", "Unknown")
        discipline_counts[disc] = discipline_counts.get(disc, 0) + 1

    # Tier Routing Breakdown
    t1_count = sum(1 for a in triaged_data if "Tier 1" in a.get("assigned_tier", ""))
    t2_count = sum(1 for a in triaged_data if "Tier 2" in a.get("assigned_tier", ""))
    escalation_rate = round((t2_count / total_alerts) * 100, 1)

    # Critical Infrastructure Exposure
    critical_asset_count = sum(1 for a in triaged_data if a.get("is_critical_asset") is True)
    fmi_exposure_rate = round((critical_asset_count / total_alerts) * 100, 1)

    # Workload / SLA Capacity Calculation (in hours)
    total_sla_minutes = sum(a.get("sla_minutes", 60) for a in triaged_data)
    total_sla_hours = round(total_sla_minutes / 60, 2)

    insights_summary = {
        "summary_metadata": {
            "total_alerts_ingested": total_alerts,
            "tier_1_l1_routed": t1_count,
            "tier_2_l2_escalated": t2_count,
            "escalation_rate_percent": f"{escalation_rate}%",
            "critical_asset_exposure_count": critical_asset_count,
            "critical_asset_exposure_rate": f"{fmi_exposure_rate}%",
            "total_sla_workload_hours": total_sla_hours
        },
        "discipline_breakdown": discipline_counts,
        "actionable_recommendations": [
            f"Allocate immediate L2 staffing: {t2_count} incidents ({escalation_rate}%) require senior response within expedited SLAs.",
            f"FMI Safeguard: {critical_asset_count} incidents target critical financial assets, requiring joint review with Infrastructure Engineering.",
            f"Cross-Discipline Alignment: Review alerts originating from {', '.join(discipline_counts.keys())}."
        ]
    }

    # Export insights JSON for reporting integrations / dashboards
    try:
        with open(report_file_path, "w", encoding="utf-8") as f:
            json.dump(insights_summary, f, indent=2)
        print(f"[DEBUG] Operational insights saved to '{report_file_path}'.")
    except Exception as e:
        print(f"[ERROR] Could not write operational insights report: {e}")

    return insights_summary


def main():
    """Orchestrates the end-to-end Security Fusion Triage & Analytics Pipeline."""
    input_file = "sample_alerts.json"
    audit_output_file = "triage_decision_log.csv"
    analytics_output_file = "fusion_operational_insights.json"

    # Step 1: Ingest Data
    alerts = load_alerts(input_file)
    if not alerts:
        print("[ABORT] Pipeline terminated early due to ingestion failure.")
        return

    # Step 2: Triage Evaluation across disciplines
    triaged = triage_alerts(alerts)

    # Step 3: Export Compliance Audit Log
    export_decision_log(triaged, audit_output_file)

    # Step 4: Generate Operational Analytics & Metrics
    insights = generate_operational_insights(triaged, analytics_output_file)

    # Step 5: Render Executive Operations Summary
    meta = insights.get("summary_metadata", {})
    disc = insights.get("discipline_breakdown", {})

    print("\n" + "=" * 55)
    print("      LSEG SECURITY FUSION CENTRE - OPERATIONAL INSIGHTS      ")
    print("=" * 55)
    print(f" Total Alerts Processed       : {meta.get('total_alerts_ingested', 0)}")
    print(f" Tier 1 (L1) Queue Routed     : {meta.get('tier_1_l1_routed', 0)}")
    print(f" Tier 2 (L2) Queue Escalated  : {meta.get('tier_2_l2_escalated', 0)} ({meta.get('escalation_rate_percent', '0%')})")
    print(f" Critical FMI Asset Incidents : {meta.get('critical_asset_exposure_count', 0)} ({meta.get('critical_asset_exposure_rate', '0%')})")
    print(f" Total Committed SLA Capacity : {meta.get('total_sla_workload_hours', 0)} analyst-hours")
    print("-" * 55)
    print(" Discipline Breakdown:")
    for d_name, count in disc.items():
        print(f"   • {d_name:<26}: {count} alert(s)")
    print("-" * 55)
    print(" Key Actionable Insights:")
    for rec in insights.get("actionable_recommendations", []):
        print(f"   [!] {rec}")
    print("=" * 55)
    print(f" Audit Log File               : {audit_output_file}")
    print(f" Analytics Report File        : {analytics_output_file}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()