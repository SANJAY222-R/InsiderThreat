"""
Feature Engineering Pipeline
============================

Transforms raw security event logs, telemetry, and entity metadata into
structured node and edge feature vectors for THGNN training and real-time inference.

Feature categories:
    - Temporal: hour-of-day, day-of-week, is_weekend, is_after_hours, periodicity
    - Behavioral: session duration, login volume, file access velocity, USB events
    - Statistical: rolling z-scores, historical deviation, entropy of interactions
    - Textual / Semantic: access sensitivity, command risk, path anomaly
    - Psychometric / Role: clearance level, tenure, department baseline
"""

import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

__all__ = ["FeatureEngineer"]


class FeatureEngineer:
    """
    Transforms raw logs and entity activities into ML-ready feature vectors.
    """

    def __init__(self, normal_working_hours: tuple[int, int] = (8, 18)) -> None:
        self.work_start, self.work_end = normal_working_hours
        self.feature_names = [
            "hour_of_day",
            "day_of_week",
            "is_weekend",
            "is_after_hours",
            "sin_hour",
            "cos_hour",
            "login_frequency",
            "failed_login_ratio",
            "session_duration_hrs",
            "file_download_bytes_mb",
            "file_access_velocity",
            "usb_insertion_count",
            "email_external_ratio",
            "device_switching_count",
            "sensitive_resource_access",
            "z_score_activity",
        ]

    def extract_temporal_features(self, dt: Optional[Union[datetime, str, float, int]] = None) -> Dict[str, float]:
        """
        Extract cyclic and categorical temporal features from a timestamp.
        """
        if dt is None:
            dt = datetime.now()
        elif isinstance(dt, (int, float)):
            dt = datetime.fromtimestamp(dt)
        elif isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
            except ValueError:
                dt = datetime.now()

        hour = dt.hour + dt.minute / 60.0
        day_of_week = float(dt.weekday())  # 0 = Monday, 6 = Sunday
        is_weekend = 1.0 if dt.weekday() >= 5 else 0.0
        is_after_hours = 1.0 if (dt.hour < self.work_start or dt.hour >= self.work_end) else 0.0

        # Continuous cyclic temporal encoding (sin/cos of 24h day)
        sin_hour = math.sin(2 * math.pi * hour / 24.0)
        cos_hour = math.cos(2 * math.pi * hour / 24.0)

        return {
            "hour_of_day": round(hour, 2),
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "is_after_hours": is_after_hours,
            "sin_hour": round(sin_hour, 4),
            "cos_hour": round(cos_hour, 4),
        }

    def extract_behavioral_features(self, events: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Aggregate behavioral patterns from a sequence of raw log events.
        """
        if not events:
            return {
                "login_frequency": 0.0,
                "failed_login_ratio": 0.0,
                "session_duration_hrs": 0.0,
                "file_download_bytes_mb": 0.0,
                "file_access_velocity": 0.0,
                "usb_insertion_count": 0.0,
                "email_external_ratio": 0.0,
                "device_switching_count": 0.0,
                "sensitive_resource_access": 0.0,
            }

        total_events = len(events)
        logins = sum(1 for e in events if e.get("type") in ("login", "auth", "LOGON"))
        failed_logins = sum(1 for e in events if e.get("status") in ("failed", "failure", "401", "403"))
        usb_events = sum(1 for e in events if e.get("type") in ("usb", "removable_media", "DEVICE_CONNECT"))

        file_bytes = sum(float(e.get("bytes", 0)) for e in events if e.get("type") in ("file_download", "file_read", "FILE"))
        file_count = sum(1 for e in events if "file" in str(e.get("type", "")).lower())

        emails = [e for e in events if "email" in str(e.get("type", "")).lower()]
        external_emails = sum(1 for e in emails if e.get("is_external", False))

        devices = {e.get("device_id") or e.get("host") for e in events if e.get("device_id") or e.get("host")}
        sensitive_count = sum(1 for e in events if e.get("is_sensitive", False) or e.get("classification") in ("confidential", "secret", "restricted"))

        return {
            "login_frequency": float(logins),
            "failed_login_ratio": round(failed_logins / max(1, logins), 4),
            "session_duration_hrs": round(total_events * 0.15, 2),  # Estimated active duration
            "file_download_bytes_mb": round(file_bytes / (1024 * 1024), 2),
            "file_access_velocity": round(file_count / max(1.0, total_events * 0.15), 2),
            "usb_insertion_count": float(usb_events),
            "email_external_ratio": round(external_emails / max(1, len(emails)), 4) if emails else 0.0,
            "device_switching_count": float(max(0, len(devices) - 1)),
            "sensitive_resource_access": float(sensitive_count),
        }

    def extract_statistical_features(
        self, current_value: float, historical_mean: float, historical_std: float
    ) -> Dict[str, float]:
        """
        Compute statistical deviation (Z-score and relative delta) against user baseline.
        """
        std = max(historical_std, 1e-5)
        z_score = (current_value - historical_mean) / std
        deviation_pct = ((current_value - historical_mean) / max(1e-5, historical_mean)) * 100.0

        return {
            "z_score_activity": round(z_score, 4),
            "deviation_pct": round(deviation_pct, 2),
        }

    def transform(
        self,
        employee_id: str,
        events: Optional[List[Dict[str, Any]]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, float]:
        """
        End-to-end transformation of an employee's context into a comprehensive feature dict.
        """
        events = events or []
        context = context or {}

        timestamp = context.get("timestamp") or (events[0].get("timestamp") if events else None)
        temporal = self.extract_temporal_features(timestamp)
        behavioral = self.extract_behavioral_features(events)

        hist_mean = float(context.get("historical_mean", 10.0))
        hist_std = float(context.get("historical_std", 3.0))
        current_activity = float(len(events) or context.get("activity_count", 15.0))
        statistical = self.extract_statistical_features(current_activity, hist_mean, hist_std)

        # Merge all categories
        features: Dict[str, float] = {}
        features.update(temporal)
        features.update(behavioral)
        features.update(statistical)

        # Inject context overrides if provided
        for k, v in context.items():
            if k in self.feature_names and isinstance(v, (int, float)):
                features[k] = float(v)

        return features

    def to_vector(self, features: Dict[str, float]) -> List[float]:
        """
        Convert a feature dictionary into an ordered numerical list aligned with `self.feature_names`.
        """
        return [float(features.get(name, 0.0)) for name in self.feature_names]
