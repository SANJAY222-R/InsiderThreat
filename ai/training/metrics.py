"""
Training Metrics
================

Metric computation and tracking for model training and validation.
Calculates AUC-ROC, AUC-PR, F1 Score, Precision, Recall, and confusion statistics.
"""

from typing import Any, Dict, List, Optional

__all__ = ["compute_metrics", "MetricTracker"]


def compute_metrics(y_true: List[int], y_pred: List[int], y_prob: List[float]) -> Dict[str, float]:
    """
    Compute all standard classification and calibration metrics.

    Args:
        y_true: Ground truth binary labels (0 or 1).
        y_pred: Predicted discrete binary labels (0 or 1).
        y_prob: Predicted continuous probabilities [0.0, 1.0].

    Returns:
        Dictionary of metric name -> computed value.
    """
    total = max(1, len(y_true))
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)

    accuracy = (tp + tn) / total
    precision = tp / max(1, tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / max(1, tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / max(1, tn + fp) if (tn + fp) > 0 else 0.0
    fpr = fp / max(1, fp + tn) if (fp + tn) > 0 else 0.0

    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0.0

    # Fast AUC calculation
    positives = [p for yt, p in zip(y_true, y_prob) if yt == 1]
    negatives = [p for yt, p in zip(y_true, y_prob) if yt == 0]
    if positives and negatives:
        concordant = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in positives for n in negatives)
        auroc = round(concordant / (len(positives) * len(negatives)), 4)
    else:
        auroc = 0.5

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "specificity": round(specificity, 4),
        "f1_score": round(f1, 4),
        "fpr": round(fpr, 4),
        "auroc": auroc,
    }


class MetricTracker:
    """
    Tracks and aggregates batch-level metrics across an entire training or validation epoch.
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Reset all tracked metrics."""
        self.y_true: List[int] = []
        self.y_pred: List[int] = []
        self.y_prob: List[float] = []
        self.losses: List[float] = []

    def update(
        self,
        loss: float,
        targets: Optional[List[int]] = None,
        probs: Optional[List[float]] = None,
        threshold: float = 0.5,
    ) -> None:
        """
        Record a batch's loss and prediction outputs.
        """
        self.losses.append(loss)
        if targets is not None:
            self.y_true.extend([int(t) for t in targets])
        if probs is not None:
            self.y_prob.extend([float(p) for p in probs])
            self.y_pred.extend([1 if p >= threshold else 0 for p in probs])

    def compute(self) -> Dict[str, float]:
        """
        Compute aggregate epoch metrics.
        """
        mean_loss = sum(self.losses) / max(1, len(self.losses))
        res = {"loss": round(mean_loss, 4)}

        if self.y_true and self.y_prob:
            cls_metrics = compute_metrics(self.y_true, self.y_pred, self.y_prob)
            res.update(cls_metrics)

        return res
