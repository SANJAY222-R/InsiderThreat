"""
Batch Prediction Engine
=======================

Handles batch threat predictions across multiple enterprise users.
Provides parallel inference execution, distribution statistics, and
export capabilities to JSON and CSV formats.
"""

import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ai.inference.predictor import Predictor

__all__ = ["BatchPredictor"]


class BatchPredictor:
    """
    Batch threat evaluation engine for enterprise-wide scheduled scanning.
    """

    def __init__(self, predictor: Optional[Predictor] = None) -> None:
        self.predictor = predictor or Predictor()

    def predict_batch(
        self,
        employee_ids: List[str],
        contexts: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute batch prediction across an array of employee IDs.
        """
        results: List[Dict[str, Any]] = []
        contexts = contexts or [{}] * len(employee_ids)

        for i, emp_id in enumerate(employee_ids):
            ctx = contexts[i] if i < len(contexts) else {}
            pred = self.predictor.predict(emp_id, context=ctx)
            results.append(pred)

        return results

    def summarize_batch(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute high-level summary metrics across a batch prediction set.
        """
        total = len(predictions)
        if total == 0:
            return {
                "total_entities": 0,
                "critical_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0,
                "mean_risk_score": 0.0,
                "high_risk_entities": [],
            }

        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        total_risk = 0.0
        high_risk_list: List[Dict[str, Any]] = []

        for p in predictions:
            lvl = p.get("threat_level", "LOW")
            counts[lvl] = counts.get(lvl, 0) + 1
            score = float(p.get("risk_score", 0.0))
            total_risk += score

            if lvl in ("CRITICAL", "HIGH"):
                high_risk_list.append({
                    "employee_id": p.get("employee_id"),
                    "risk_score": score,
                    "threat_level": lvl,
                })

        high_risk_list.sort(key=lambda x: x["risk_score"], reverse=True)

        return {
            "total_entities": total,
            "critical_count": counts.get("CRITICAL", 0),
            "high_count": counts.get("HIGH", 0),
            "medium_count": counts.get("MEDIUM", 0),
            "low_count": counts.get("LOW", 0),
            "mean_risk_score": round(total_risk / total, 2),
            "high_risk_entities": high_risk_list,
        }

    def export_results(
        self,
        predictions: List[Dict[str, Any]],
        output_path: Union[str, Path],
        file_format: str = "json",
    ) -> str:
        """
        Export batch predictions to JSON or CSV file on disk.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if file_format.lower() == "json":
            with open(path, "w", encoding="utf-8") as f:
                json.dump(predictions, f, indent=2)
        elif file_format.lower() == "csv":
            if not predictions:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("employee_id,risk_score,threat_level,confidence,evaluated_at\n")
            else:
                fieldnames = ["employee_id", "risk_score", "threat_level", "confidence", "evaluated_at"]
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                    writer.writeheader()
                    for p in predictions:
                        writer.writerow(p)
        else:
            raise ValueError(f"Unsupported export format: {file_format}")

        return str(path)
