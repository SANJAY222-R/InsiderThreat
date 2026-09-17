"""
Real-Time Data Feed
===================

Reads CERT r4.2 processed CSVs and emits live threat events via WebSocket broadcast.
Groups events by user within a rolling window, runs them through the Predictor,
and pushes JSON payloads to all connected WebSocket clients.
"""

import asyncio
import csv
import logging
import os
import random
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

from ai.inference.predictor import Predictor

logger = logging.getLogger(__name__)

DATASET_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "dataset", "processed")
)

_predictor = Predictor()

# Pre-loaded employee event batches: employee_id -> list of context dicts
_event_pool: List[Dict[str, Any]] = []
_pool_index = 0
_pool_loaded = False


def _load_pool(max_users: int = 200) -> None:
    global _event_pool, _pool_loaded
    if _pool_loaded:
        return

    logon_path = os.path.join(DATASET_DIR, "clean_logon.csv")
    device_path = os.path.join(DATASET_DIR, "clean_device.csv")
    http_path = os.path.join(DATASET_DIR, "clean_http.csv")
    file_path = os.path.join(DATASET_DIR, "clean_file.csv")

    user_logons: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    user_devices: Dict[str, int] = defaultdict(int)
    user_http_external: Dict[str, int] = defaultdict(int)
    user_files: Dict[str, float] = defaultdict(float)

    if os.path.exists(logon_path):
        with open(logon_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_logons[row["user"]].append(row)

    if os.path.exists(device_path):
        with open(device_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("activity", "").lower() == "connect":
                    user_devices[row["user"]] += 1

    if os.path.exists(http_path):
        with open(http_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get("url", "")
                if any(kw in url for kw in ["megaupload", "gmail", "dropbox", "mediafire", "4shared"]):
                    user_http_external[row["user"]] += 1

    if os.path.exists(file_path):
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                content = row.get("content", "")
                user_files[row["user"]] += max(1.0, len(content) / 1024.0)

    users = list(user_logons.keys())[:max_users]
    for user in users:
        logons = user_logons[user]
        after_hours_logons = [
            r for r in logons
            if int(r.get("IsBusinessHours", "1") == "false")
            or int(r.get("Hour", "9")) < 7
            or int(r.get("Hour", "9")) > 19
        ]
        total_logons = max(1, len(logons))
        after_hours_ratio = len(after_hours_logons) / total_logons

        failed = sum(1 for r in logons if r.get("activity", "").lower().startswith("fail"))
        failed_ratio = failed / total_logons

        context = {
            "is_after_hours": float(after_hours_ratio > 0.3),
            "failed_login_ratio": round(min(1.0, failed_ratio * 5), 3),
            "usb_insertion_count": float(min(10, user_devices.get(user, 0))),
            "file_download_bytes_mb": round(min(1000.0, user_files.get(user, 0.0) / 100.0), 2),
            "sensitive_resource_access": float(min(10, user_http_external.get(user, 0))),
            "email_external_ratio": round(min(1.0, user_http_external.get(user, 0) / max(1, total_logons)), 3),
            "device_switching_count": round(min(5.0, user_devices.get(user, 0) / max(1, total_logons) * 3), 2),
        }
        _event_pool.append({"employee_id": user, "context": context})

    # Shuffle so we cycle through varied risk levels
    random.shuffle(_event_pool)
    _pool_loaded = True
    logger.info(f"Data pool loaded: {len(_event_pool)} users from CERT dataset")


def _next_event() -> Dict[str, Any]:
    """Return next employee context from the circular pool."""
    global _pool_index
    if not _event_pool:
        # Fallback synthetic event if CSVs not available
        synthetic_users = ["MOH0273", "LAP0338", "CEL0561", "HPH0075", "ASD0577"]
        user = random.choice(synthetic_users)
        return {
            "employee_id": user,
            "context": {
                "is_after_hours": random.uniform(0, 1),
                "failed_login_ratio": random.uniform(0, 0.8),
                "usb_insertion_count": random.uniform(0, 5),
                "file_download_bytes_mb": random.uniform(0, 600),
                "sensitive_resource_access": random.uniform(0, 8),
                "email_external_ratio": random.uniform(0, 0.9),
                "device_switching_count": random.uniform(0, 4),
            },
        }
    event = _event_pool[_pool_index % len(_event_pool)]
    _pool_index += 1
    return event


async def stream_threat_events(manager: Any, interval_seconds: float = 4.0) -> None:
    """
    Background task: stream real threat predictions to WebSocket clients.

    Loads CERT event pool once, then every `interval_seconds` picks the next
    employee, runs the predictor, and broadcasts a structured JSON payload.
    """
    _load_pool()

    while True:
        await asyncio.sleep(interval_seconds)

        if not manager.has_connections:
            continue

        try:
            event = _next_event()
            prediction = _predictor.predict(
                event["employee_id"],
                context=event["context"],
            )

            payload = {
                "type": "threat_prediction",
                "timestamp": datetime.now().isoformat(),
                "employee_id": prediction["employee_id"],
                "risk_score": prediction["risk_score"],
                "threat_level": prediction["threat_level"],
                "confidence": prediction["confidence"],
                "top_features": prediction["explanation"].get("top_features", [])[:3],
                "alert": _build_alert(prediction),
            }

            await manager.broadcast_json(payload)
        except Exception as exc:
            logger.warning(f"Real-time broadcast error: {exc}")


def _build_alert(prediction: Dict[str, Any]) -> Dict[str, Any] | None:
    if prediction["threat_level"] in ("CRITICAL", "HIGH"):
        top = prediction["explanation"].get("top_features", [])
        reason = top[0]["name"].replace("_", " ").title() if top else "Anomalous activity"
        return {
            "severity": prediction["threat_level"],
            "title": f"{prediction['threat_level']} Risk: {prediction['employee_id']}",
            "description": f"Elevated risk detected. Primary indicator: {reason}",
            "risk_score": prediction["risk_score"],
        }
    return None
