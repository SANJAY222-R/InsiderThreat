"""
Data Simulation & Scenario Injection CLI
========================================

Wrapper around scripts/simulate_data_flow.py providing CERT r4.2 behavioral
data flow simulation and scenario injection into the threat detection pipeline.

Usage:
    python simulate_data.py                     # simulate CERT batch flow (30 users)
    python simulate_data.py --users 50          # simulate 50 users
    python simulate_data.py --api               # post results to running FastAPI backend
    python simulate_data.py --scenario exfiltration --user MOH0273
"""

import sys
import os
import argparse
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.simulate_data_flow import load_cert_events, simulate_pipeline, print_summary, save_results


def run_scenario(scenario: str, user: str, events: int = 10, post_to_api: bool = False) -> List[Dict[str, Any]]:
    scenarios = {
        "exfiltration": {
            "is_after_hours": 1.0,
            "failed_login_ratio": 0.2,
            "usb_insertion_count": 8.0,
            "file_download_bytes_mb": 850.0,
            "sensitive_resource_access": 6.0,
            "email_external_ratio": 0.4,
            "device_switching_count": 3.0,
        },
        "email_leak": {
            "is_after_hours": 0.0,
            "failed_login_ratio": 0.1,
            "usb_insertion_count": 1.0,
            "file_download_bytes_mb": 150.0,
            "sensitive_resource_access": 3.0,
            "email_external_ratio": 0.95,
            "device_switching_count": 1.0,
        },
        "auth_spike": {
            "is_after_hours": 1.0,
            "failed_login_ratio": 0.9,
            "usb_insertion_count": 0.0,
            "file_download_bytes_mb": 20.0,
            "sensitive_resource_access": 2.0,
            "email_external_ratio": 0.05,
            "device_switching_count": 5.0,
        },
        "custom": {
            "is_after_hours": 0.5,
            "failed_login_ratio": 0.3,
            "usb_insertion_count": float(min(10, events // 2)),
            "file_download_bytes_mb": float(events * 50),
            "sensitive_resource_access": float(min(10, events)),
            "email_external_ratio": 0.3,
            "device_switching_count": 2.0,
        },
    }

    ctx = scenarios.get(scenario, scenarios["custom"])
    user_contexts = {user: ctx}
    print(f"\n[Injecting Scenario: '{scenario}' for user '{user}']")
    results = simulate_pipeline(user_contexts, post_to_api=post_to_api)
    print_summary(results)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate CERT data flow and attack scenarios")
    parser.add_argument("--scenario", type=str, choices=["exfiltration", "email_leak", "auth_spike", "custom"], help="Attack scenario to inject")
    parser.add_argument("--user", type=str, default="MOH0273", help="Target user ID for scenario (default: MOH0273)")
    parser.add_argument("--events", type=int, default=10, help="Number of custom events (for --scenario custom)")
    parser.add_argument("--users", type=int, default=30, help="Number of CERT users to simulate (default: 30)")
    parser.add_argument("--api", action="store_true", help="Post predictions to running FastAPI backend")
    parser.add_argument("--output", type=str, default="data/simulation_results.json", help="Output JSON path")
    args = parser.parse_args()

    if args.scenario:
        run_scenario(args.scenario, args.user, args.events, post_to_api=args.api)
    else:
        user_contexts = load_cert_events(max_users=args.users)
        results = simulate_pipeline(user_contexts, post_to_api=args.api)
        print_summary(results)
        save_results(results, args.output)


if __name__ == "__main__":
    main()
