"""
Training Callbacks
==================

Callback hooks for training events:
- on_epoch_start / on_epoch_end
- on_batch_start / on_batch_end
- on_train_end
- Early stopping
- Model checkpointing
- Metric logging

Phase 0: Stub only.

TODO (Phase 5): Implement callback system.
"""

__all__ = ["EarlyStopping", "ModelCheckpoint", "MetricLogger"]


class EarlyStopping:
    """Stop training when validation metric stops improving."""
    pass


class ModelCheckpoint:
    """Save model checkpoints during training."""
    pass


class MetricLogger:
    """Log training metrics to file and console."""
    pass
