#!/usr/bin/env python3
"""
Enterprise Insider Threat Detection - Test Data & Scenario Injector
===================================================================

This utility lets you inject security log streams, simulate realistic insider threat attack scenarios,
and test the THGNN inference engine and Cytoscape graph explorer.

Usage:
  python simulate_data.py --scenario exfiltration --user MOH0273
  python simulate_data.py --scenario email_leak --user LAP0338
  python simulate_data.py --scenario auth_spike --user CEL0561
  python simulate_data.py --scenario custom --user EMP_CUSTOM --events 10
  python simulate_data.py --stream-cert --limit 50
"""

import argparse
import sys
import os
import json
import time
from datetime import datetime, timezone
import requests

# Default API URL
DEFAULT_API_URL = "http://localhost:8000/api/v1"


def get_auth_token(api_url: str, username: str = "analyst", password: str = "password123") -> str:
    """Authenticate with backend and retrieve access token."""
    login_url = f"{api_url}/auth/login"
    try:
        res = requests.post(login_url, data={"username": username, "password": password}, timeout=5)
        if res.status_code == 200:
            return res.json()["access_token"]
        print(f"[-] Authentication failed ({res.status_code}): {res.text}")
    except Exception as e:
        print(f"[-] Could not connect to backend at {login_url}: {e}")
    return ""


def inject_event(api_url: str, token: str, user_id: str, event_type: str, target: str, target_type: str = "device", meta: dict = None):
    """Inject a dynamic event into the live enterprise graph."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "user_id": user_id,
        "event_type": event_type,
        "target_entity": target,
        "target_type": target_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": meta or {},
    }
    res = requests.post(f"{api_url}/graphs/event", json=payload, headers=headers)
    if res.status_code == 200:
        print(f"  [+] Injected Graph Event: ({user_id}) -[{event_type}]-> ({target})")
    else:
        print(f"  [-] Failed to inject event: {res.text}")


def run_prediction(api_url: str, token: str, user_id: str):
    """Run real-time THGNN inference for target user."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    res = requests.post(f"{api_url}/predictions/", json={"employee_id": user_id}, headers=headers)
    if res.status_code == 201:
        data = res.json()
        print(f"\n  =======================================================")
        print(f"  [*] INFERENCE RESULT FOR ENTITY: {data['employee_id']}")
        print(f"  -------------------------------------------------------")
        print(f"  * Threat Level    : {data['threat_level']}")
        print(f"  * Risk Score      : {data['risk_score']} / 100")
        print(f"  * Confidence      : {round(data['confidence'] * 100, 1)}%")
        print(f"  * Model Version   : {data['model_version']}")
        print(f"  * Method          : {data.get('explanation', {}).get('method', 'THGNN')}")
        print(f"  =======================================================\n")
        return data
    else:
        print(f"  [-] Inference failed: {res.text}")
    return None


def create_alert(api_url: str, token: str, user_id: str, title: str, severity: str, desc: str):
    """Trigger a SOC incident alert."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "employee_id": user_id,
        "severity": severity,
        "title": title,
        "description": desc,
        "notes": "Automated scenario trigger",
    }
    res = requests.post(f"{api_url}/alerts/", json=payload, headers=headers)
    if res.status_code == 201:
        print(f"  [!] Triggered SOC Alert: [{severity.upper()}] {title}")


def simulate_scenario_exfiltration(api_url: str, token: str, user_id: str):
    """Scenario 1: USB Removable Media Exfiltration."""
    print(f"\n[*] Simulating Removable Media Exfiltration Scenario for: {user_id}")
    inject_event(api_url, token, user_id, "uses", f"PC-{user_id[:4]}", "device", {"label": "Late-Night Logon"})
    time.sleep(0.5)
    inject_event(api_url, token, user_id, "accessed", "FINANCIAL_LEDGER_Q4_CONFIDENTIAL.xlsx", "file", {"label": "File Read"})
    time.sleep(0.5)
    inject_event(api_url, token, user_id, "accessed", "CUSTOMER_CREDIT_CARDS_RAW.csv", "file", {"label": "Mass Download"})
    time.sleep(0.5)
    inject_event(api_url, token, user_id, "usb_connect", "SANDISK-ULTRA-64GB-UNAUTHORIZED", "usb", {"label": "Mass Copy"})
    time.sleep(0.5)

    create_alert(
        api_url,
        token,
        user_id,
        "Critical Removable Media Exfiltration Anomaly",
        "critical",
        f"Employee {user_id} inserted an unauthorized USB drive after hours and transferred confidential financial ledgers.",
    )
    run_prediction(api_url, token, user_id)


def simulate_scenario_email_leak(api_url: str, token: str, user_id: str):
    """Scenario 2: Abnormal Outbound Communications & Data Leak."""
    print(f"\n[*] Simulating External Email Data Leak Scenario for: {user_id}")
    inject_event(api_url, token, user_id, "uses", f"PC-{user_id[:4]}", "device", {"label": "Logon"})
    time.sleep(0.5)
    inject_event(api_url, token, user_id, "accessed", "PROPRIETARY_ALGO_SOURCE.zip", "file", {"label": "Archive Access"})
    time.sleep(0.5)
    inject_event(api_url, token, user_id, "sent_email", "shadow-drop@protonmail-external.com", "email", {"label": "Outbound Leak"})
    time.sleep(0.5)

    create_alert(
        api_url,
        token,
        user_id,
        "High Outbound External Email Anomaly",
        "high",
        f"Employee {user_id} transmitted archive attachments to external domain protonmail-external.com.",
    )
    run_prediction(api_url, token, user_id)


def simulate_scenario_auth_spike(api_url: str, token: str, user_id: str):
    """Scenario 3: Authentication Anomaly & Lateral Workstation Probing."""
    print(f"\n[*] Simulating Authentication Spike & Lateral Movement for: {user_id}")
    for i in range(1, 4):
        inject_event(api_url, token, user_id, "uses", f"PC-CORE-SERVER-0{i}", "device", {"label": "Failed Auth"})
        time.sleep(0.3)

    create_alert(
        api_url,
        token,
        user_id,
        "Multiple Workstation Authentication Failures",
        "high",
        f"Employee {user_id} exhibited abnormal authentication attempts across server clusters.",
    )
    run_prediction(api_url, token, user_id)


def main():
    parser = argparse.ArgumentParser(description="Enterprise Insider Threat Test Data & Scenario Injector")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help="Backend API base URL")
    parser.add_argument(
        "--scenario",
        choices=["exfiltration", "email_leak", "auth_spike", "custom"],
        default="exfiltration",
        help="Attack scenario type to simulate",
    )
    parser.add_argument("--user", default="MOH0273", help="Target user ID (e.g. MOH0273, LAP0338, CEL0561)")
    parser.add_argument("--events", type=int, default=5, help="Number of custom events to generate")
    args = parser.parse_args()

    print("================================================================")
    print("   ENTERPRISE INSIDER THREAT DETECTION - DATA INJECTOR")
    print("================================================================")
    print(f"Connecting to Backend: {args.api_url} ...")

    token = get_auth_token(args.api_url)
    if not token:
        print("\n[!] Could not authenticate. Ensure backend is running (`uvicorn backend.app.main:app --port 8000`).")
        sys.exit(1)

    print("[+] Successfully authenticated as SOC Analyst.")

    if args.scenario == "exfiltration":
        simulate_scenario_exfiltration(args.api_url, token, args.user)
    elif args.scenario == "email_leak":
        simulate_scenario_email_leak(args.api_url, token, args.user)
    elif args.scenario == "auth_spike":
        simulate_scenario_auth_spike(args.api_url, token, args.user)
    elif args.scenario == "custom":
        print(f"\n[*] Injecting {args.events} custom test events for {args.user}...")
        for i in range(1, args.events + 1):
            inject_event(
                args.api_url,
                token,
                args.user,
                "accessed",
                f"CUSTOM_RESOURCE_{i:03d}.dat",
                "file",
                {"label": f"Custom Op {i}"},
            )
            time.sleep(0.2)
        run_prediction(args.api_url, token, args.user)

    print("\n[✓] Simulation completed. Open the UI at http://localhost:5173/graph to view the updated graph topology!")


if __name__ == "__main__":
    main()
