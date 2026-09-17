"""
Model Evaluator
===============

Comprehensive model evaluation and validation pipeline.
Calculates classification metrics, ROC curves, precision-recall curves,
confusion matrices, and risk calibration metrics without requiring external C extensions.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union

__all__ = ["Evaluator"]


class Evaluator:
    """
    Evaluator for assessing threat detection model performance.

    Computes:
    - Accuracy, Precision, Recall / Sensitivity, Specificity, F1 Score
    - False Positive Rate (FPR), False Negative Rate (FNR)
    - Area Under ROC Curve (AUC-ROC)
    - Area Under PR Curve (AUC-PR)
    - Full Confusion Matrix (TP, FP, TN, FN)
    """

    def __init__(self, threshold: float = 0.5) -> None:
        self.threshold = threshold

    def compute_confusion_matrix(
        self, y_true: List[int], y_pred: List[int]
    ) -> Dict[str, int]:
        """
        Compute true positives, false positives, true negatives, and false negatives.
        """
        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
        tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)

        return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}

    def compute_roc_auc(self, y_true: List[int], y_prob: List[float]) -> float:
        """
        Calculate Area Under the ROC Curve via Mann-Whitney U rank statistic.
        """
        positives = [p for yt, p in zip(y_true, y_prob) if yt == 1]
        negatives = [p for yt, p in zip(y_true, y_prob) if yt == 0]

        n_pos = len(positives)
        n_neg = len(negatives)

        if n_pos == 0 or n_neg == 0:
            return 0.5

        # Pairwise comparison
        concordant = 0.0
        for p in positives:
            for n in negatives:
                if p > n:
                    concordant += 1.0
                elif p == n:
                    concordant += 0.5

        return round(concordant / (n_pos * n_neg), 4)

    def compute_pr_auc(self, y_true: List[int], y_prob: List[float]) -> float:
        """
        Calculate Area Under the Precision-Recall curve using numerical integration.
        """
        if not y_true or sum(y_true) == 0:
            return 0.0

        # Sort by predicted probability descending
        sorted_pairs = sorted(zip(y_prob, y_true), key=lambda x: x[0], reverse=True)

        n_pos = sum(y_true)
        cum_tp = 0
        cum_fp = 0
        precisions = [1.0]
        recalls = [0.0]

        for _, yt in sorted_pairs:
            if yt == 1:
                cum_tp += 1
            else:
                cum_fp += 1
            prec = cum_tp / (cum_tp + cum_fp)
            rec = cum_tp / n_pos
            precisions.append(prec)
            recalls.append(rec)

        # Trapezoidal numerical integration
        auc_pr = 0.0
        for i in range(len(recalls) - 1):
            auc_pr += (recalls[i + 1] - recalls[i]) * ((precisions[i + 1] + precisions[i]) / 2.0)

        return round(min(1.0, max(0.0, auc_pr)), 4)

    def evaluate(
        self,
        y_true: List[int],
        y_prob: List[float],
        threshold: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Compute full suite of classification and calibration metrics.
        """
        thresh = threshold if threshold is not None else self.threshold
        y_pred = [1 if p >= thresh else 0 for p in y_prob]

        cm = self.compute_confusion_matrix(y_true, y_pred)
        tp, fp, tn, fn = cm["tp"], cm["fp"], cm["tn"], cm["fn"]
        total = max(1, len(y_true))

        accuracy = (tp + tn) / total
        precision = tp / max(1, tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / max(1, tp + fn) if (tp + fn) > 0 else 0.0
        specificity = tn / max(1, tn + fp) if (tn + fp) > 0 else 0.0
        fpr = fp / max(1, fp + tn) if (fp + tn) > 0 else 0.0
        fnr = fn / max(1, fn + tp) if (fn + tp) > 0 else 0.0

        if precision + recall > 0:
            f1 = 2 * (precision * recall) / (precision + recall)
        else:
            f1 = 0.0

        auroc = self.compute_roc_auc(y_true, y_prob)
        auprc = self.compute_pr_auc(y_true, y_prob)

        return {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "specificity": round(specificity, 4),
            "f1_score": round(f1, 4),
            "fpr": round(fpr, 4),
            "fnr": round(fnr, 4),
            "auroc": auroc,
            "auprc": auprc,
            "confusion_matrix": cm,
            "threshold": thresh,
            "total_samples": len(y_true),
        }

    def format_report(self, metrics: Dict[str, Any]) -> str:
        """
        Format metrics into a clean text report.
        """
        cm = metrics.get("confusion_matrix", {})
        return (
            f"=== Threat Detection Model Evaluation Report ===\n"
            f"Accuracy:    {metrics.get('accuracy', 0.0):.4f}\n"
            f"Precision:   {metrics.get('precision', 0.0):.4f}\n"
            f"Recall:      {metrics.get('recall', 0.0):.4f}\n"
            f"F1 Score:    {metrics.get('f1_score', 0.0):.4f}\n"
            f"AUC-ROC:     {metrics.get('auroc', 0.0):.4f}\n"
            f"AUC-PR:      {metrics.get('auprc', 0.0):.4f}\n"
            f"False Pos %: {metrics.get('fpr', 0.0) * 100:.2f}%\n"
            f"Confusion:   TP={cm.get('tp', 0)}, FP={cm.get('fp', 0)}, TN={cm.get('tn', 0)}, FN={cm.get('fn', 0)}\n"
        )
