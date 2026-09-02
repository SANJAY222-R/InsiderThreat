
"""
Alert ORM Model
================

Stores security alerts triggered by threat predictions.

Phase 0: Schema stub only.
"""

__all__ = ["Alert"]


class Alert:
    """
    Alert database model.

    Attributes:
        id: Primary key.
        prediction_id: FK to triggering prediction.
        severity: Alert severity (info, warning, critical).
        status: Alert status (open, investigating, resolved, false_positive).
        assigned_to: Analyst user ID.
        notes: Investigation notes.
        created_at: Alert creation timestamp.
        resolved_at: Resolution timestamp.

    TODO (Phase 3): Implement with SQLAlchemy mapped columns.
    """
    pass
