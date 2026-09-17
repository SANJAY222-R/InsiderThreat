"""
Training Callbacks
==================

Callback hooks for training lifecycle events:
- EarlyStopping: halts training when validation metric stops improving
- ModelCheckpoint: saves best and regular epoch checkpoints to disk
- MetricLogger: formats and logs training and validation metrics
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

__all__ = ["EarlyStopping", "ModelCheckpoint", "MetricLogger"]

logger = logging.getLogger(__name__)


class EarlyStopping:
    """
    Early stopping to terminate training when validation loss stops improving.
    """

    def __init__(self, patience: int = 5, min_delta: float = 1e-4, mode: str = "min") -> None:
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best_score: Optional[float] = None
        self.early_stop = False

    def step(self, metric: float) -> bool:
        """
        Check if training should be halted based on new metric value.
        Returns True if early stopping is triggered.
        """
        if self.best_score is None:
            self.best_score = metric
            return False

        if self.mode == "min":
            improved = metric < (self.best_score - self.min_delta)
        else:
            improved = metric > (self.best_score + self.min_delta)

        if improved:
            self.best_score = metric
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
                logger.info(f"EarlyStopping triggered after {self.counter} epochs without improvement.")

        return self.early_stop


class ModelCheckpoint:
    """
    Saves model checkpoints during training epochs.
    """

    def __init__(
        self,
        checkpoint_dir: Union[str, Path] = "ai/checkpoints",
        save_best_only: bool = True,
        monitor: str = "val_loss",
        mode: str = "min",
    ) -> None:
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.save_best_only = save_best_only
        self.monitor = monitor
        self.mode = mode
        self.best_metric: Optional[float] = None

    def save(self, epoch: int, metrics: Dict[str, float], model_state: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Evaluate metric and conditionally save checkpoint to disk.
        """
        current_val = metrics.get(self.monitor)
        if current_val is None:
            return None

        is_best = False
        if self.best_metric is None:
            is_best = True
        elif self.mode == "min" and current_val < self.best_metric:
            is_best = True
        elif self.mode == "max" and current_val > self.best_metric:
            is_best = True

        if is_best:
            self.best_metric = current_val
            filepath = self.checkpoint_dir / f"best_model_epoch_{epoch}.json"
            data = {
                "epoch": epoch,
                "monitor": self.monitor,
                "best_metric": self.best_metric,
                "metrics": metrics,
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return str(filepath)

        return None


class MetricLogger:
    """
    Logs epoch metrics and history to console and JSON lines.
    """

    def __init__(self, log_file: Optional[Union[str, Path]] = None) -> None:
        self.log_file = Path(log_file) if log_file else None
        self.history: List[Dict[str, Any]] = []

    def log_epoch(self, epoch: int, train_metrics: Dict[str, float], val_metrics: Optional[Dict[str, float]] = None) -> None:
        """
        Record and display metrics for an epoch.
        """
        entry = {
            "epoch": epoch,
            "train": train_metrics,
            "val": val_metrics or {},
        }
        self.history.append(entry)

        train_str = " | ".join(f"{k}: {v:.4f}" for k, v in train_metrics.items())
        val_str = " | ".join(f"val_{k}: {v:.4f}" for k, v in (val_metrics or {}).items())
        logger.info(f"[Epoch {epoch:03d}] {train_str} || {val_str}")

        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
