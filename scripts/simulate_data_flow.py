"""
Data Flow Simulation
====================

Reads CERT r4.2 dataset CSVs and simulates how real employee behavioral data
flows through the threat detection pipeline. Outputs predictions and XAI
explanations for each user batch. Optionally posts results to the running API.

Usage:
    python scripts/simulate_data_flow.py                    # dry run, print only
    python scripts/simulate_data_flow.py --api              # post to running API
    python scripts/simulate_data_flow.py --users 20         # simulate 20 users
    python scripts/simulate_data_flow.py --api --users 50   # both
"""

import argparse
import csv
import json
import os
import sys
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.inference.predictor import Predictor
from ai.explainability.feature_importance import FeatureImportance
from ai.explainability.gnn_explainer import GNNExplainerWrapper
from ai.explainability.attention_explainer import AttentionExplainer

DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataset", "processed")
API_BASE = "http://localhost:8000"


def load_cert_events(max_users: int = 50) -> Dict[str, Dict[str, Any]]:
    """Load CERT CSV events and aggregate per-user behavioral features."""
    logon_path = os.path.join(DATASET_DIR, "clean_logon.csv")
    device_path = os.path.join(DATASET_DIR, "clean_device.csv")
    http_path = os.path.join(DATASET_DIR, "clean_http.csv")
    file_path = os.path.join(DATASET_DIR, "clean_file.csv")
    email_path = os.path.join(DATASET_DIR, "clean_email.csv")

    user_data: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "total_logons": 0,
        "after_hours_logons": 0,
        "failed_logons": 0,
        "usb_connects": 0,
        "external_http": 0,
        "file_bytes": 0.0,
        "external_emails": 0,
        "total_emails": 0,
    })

    print(f"Loading logon events from {logon_path}...")
    if os.path.exists(logon_path):
        with open(logon_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                u = row["user"]
                user_data[u]["total_logons"] += 1
                hour = int(row.get("Hour", 9))
                is_bh = row.get("IsBusinessHours", "true").lower() == "true"
                if not is_bh or hour < 7 or hour > 19:
                    user_data[u]["after_hours_logons"] += 1
                if row.get("activity", "").lower().startswith("fail"):
                    user_data[u]["failed_logons"] += 1

    print(f"Loading device events from {device_path}...")
    if os.path.exists(device_path):
        with open(device_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("activity", "").lower() == "connect":
                    user_data[row["user"]]["usb_connects"] += 1

    print(f"Loading HTTP events from {http_path}...")
    if os.path.exists(http_path):
        with open(http_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get("url", "")
                if any(kw in url for kw in ["megaupload", "gmail", "dropbox", "mediafire", "4shared", "wikileaks"]):
                    user_data[row["user"]]["external_http"] += 1

    print(f"Loading file events from {file_path}...")
    if os.path.exists(file_path):
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                content_len = len(row.get("content", ""))
                user_data[row["user"]]["file_bytes"] += content_len

    print(f"Loading email events from {email_path}...")
    if os.path.exists(email_path):
        with open(email_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                u = row["user"]
                user_data[u]["total_emails"] += 1
                to_addr = row.get("to", "")
                frm_addr = row.get("from", "")
                # External if to address is outside company domain
                if "@dtaa.com" not in to_addr:
                    user_data[u]["external_emails"] += 1

    users = list(user_data.keys())[:max_users]
    result = {}
    for u in users:
        d = user_data[u]
        total = max(1, d["total_logons"])
        result[u] = {
            "is_after_hours": float(d["after_hours_logons"] / total > 0.3),
            "failed_login_ratio": round(min(1.0, d["failed_logons"] / total * 5), 4),
            "usb_insertion_count": float(min(10, d["usb_connects"])),
            "file_download_bytes_mb": round(min(1000.0, d["file_bytes"] / (1024 * 1024)), 4),
            "sensitive_resource_access": float(min(10, d["external_http"])),
            "email_external_ratio": round(min(1.0, d["external_emails"] / max(1, d["total_emails"])), 4),
            "device_switching_count": round(min(5.0, d["usb_connects"] / total * 3), 4),
        }

    print(f"\nLoaded behavioral profiles for {len(result)} users\n")
    return result


def simulate_pipeline(
    user_contexts: Dict[str, Dict[str, Any]],
    post_to_api: bool = False,
) -> List[Dict[str, Any]]:
    predictor = Predictor()
    feat_explainer = FeatureImportance()
    gnn_explainer = GNNExplainerWrapper()
    attn_explainer = AttentionExplainer()

    results = []
    total = len(user_contexts)

    print(f"{'='*70}")
    print(f"SIMULATING DATA FLOW: {total} employees through THGNN pipeline")
    print(f"{'='*70}\n")

    for i, (employee_id, context) in enumerate(user_contexts.items(), 1):
        print(f"[{i:>3}/{total}] Processing: {employee_id}", end="  ")

        prediction = predictor.predict(employee_id, context=context)
        risk = prediction["risk_score"]
        level = prediction["threat_level"]

        feat_result = feat_explainer.explain(employee_id, context={"risk_score": risk})
        gnn_result = gnn_explainer.explain(employee_id, context={"risk_score": risk})
        attn_result = attn_explainer.explain(employee_id, context={"risk_score": risk})

        record = {
            "employee_id": employee_id,
            "risk_score": risk,
            "threat_level": level,
            "confidence": prediction["confidence"],
            "context": context,
            "explanation": {
                "feature_importance": feat_result.get("feature_attributions", {}),
                "counterfactuals": feat_result.get("counterfactuals", []),
                "subgraph_nodes": len(gnn_result.get("nodes", [])),
                "subgraph_edges": len(gnn_result.get("edges", [])),
                "attention_heads": len(attn_result.get("attention_heads", [])),
            },
        }
        results.append(record)

        level_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(level, "⚪")
        print(f"Risk={risk:5.1f}  Level={level_emoji} {level:<8}")

        if post_to_api:
            _post_prediction(employee_id, context)

        time.sleep(0.05)  # small delay to avoid overwhelming output

    print(f"\n{'='*70}")
    print(f"PIPELINE COMPLETE: {total} users processed")
    return results


def _post_prediction(employee_id: str, context: Dict[str, Any]) -> None:
    try:
        import urllib.request
        import urllib.error

        # First login to get token
        login_data = json.dumps({"username": "admin", "password": "admin123"}).encode()
        req = urllib.request.Request(
            f"{API_BASE}/api/v1/auth/login",
            data=login_data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            token = json.loads(resp.read())["access_token"]

        # Post prediction
        payload = json.dumps({"employee_id": employee_id, "context": context}).encode()
        pred_req = urllib.request.Request(
            f"{API_BASE}/api/v1/predictions/predict",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(pred_req, timeout=5) as resp:
            result = json.loads(resp.read())
            print(f"    -> API: prediction ID {result.get('id')} saved")
    except Exception as e:
        print(f"    -> API: skipped ({e})")


def print_summary(results: List[Dict[str, Any]]) -> None:
    print("\nRISK LEVEL DISTRIBUTION")
    print("-" * 40)
    counts: Dict[str, int] = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for r in results:
        counts[r["threat_level"]] = counts.get(r["threat_level"], 0) + 1

    for level, count in counts.items():
        bar = "█" * count
        print(f"  {level:<10} {count:>4}  {bar}")

    total = len(results)
    avg_risk = sum(r["risk_score"] for r in results) / max(1, total)
    print(f"\n  Total users : {total}")
    print(f"  Average risk: {avg_risk:.1f}")

    print("\nTOP 10 HIGHEST RISK EMPLOYEES")
    print("-" * 40)
    top10 = sorted(results, key=lambda x: x["risk_score"], reverse=True)[:10]
    for r in top10:
        print(f"  {r['employee_id']:<15} Risk={r['risk_score']:5.1f}  {r['threat_level']}")


def save_results(results: List[Dict[str, Any]], output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate CERT data flow through threat detection pipeline")
    parser.add_argument("--api", action="store_true", help="Post predictions to running API")
    parser.add_argument("--users", type=int, default=30, help="Number of users to simulate (default: 30)")
    parser.add_argument("--output", type=str, default="data/simulation_results.json", help="Output JSON path")
    args = parser.parse_args()

    user_contexts = load_cert_events(max_users=args.users)
    results = simulate_pipeline(user_contexts, post_to_api=args.api)
    print_summary(results)
    save_results(results, args.output)
