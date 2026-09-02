"""
Training Metrics
================

Metric computation for model evaluation during training.

Metrics:
    - AUC-ROC
    - AUC-PR (Precision-Recall)
    - F1 Score (macro, micro, weighted)
    - Precision / Recall at threshold
    - False Positive Rate
    - Detection Rate

Phase 0: Stub only.

TODO (Phase 5): Implement with scikit-learn and torchmetrics.
"""

__all__ = ["compute_metrics", "MetricTracker"]


def compute_metrics(y_true: list, y_pred: list, y_prob: list) -> dict:
    """
    Compute all evaluation metrics.

    Args:
        y_true: Ground truth labels.
        y_pred: Predicted labels.
        y_prob: Prediction probabilities.

    Returns:
        Dictionary of metric name → value.

    TODO (Phase 5): Implement.
    """
    raise NotImplementedError("Phase 5: Metric computation")


class MetricTracker:
    """Tracks and aggregates metrics across training epochs."""
    pass
