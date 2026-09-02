
"""
Prediction ORM Model
====================

Stores threat prediction results from the THGNN model.

Phase 0: Schema stub only.
"""

__all__ = ["Prediction"]


class Prediction:
    """
    Prediction database model.

    Attributes:
        id: Primary key.
        user_id: Reference to the enterprise user being evaluated.
        risk_score: Normalized threat score [0.0, 1.0].
        threat_level: Categorical level (low, medium, high, critical).
        model_version: Version of the model that produced this prediction.
        explanation: JSON blob with XAI feature attributions.
        timestamp: Prediction generation time.

    TODO (Phase 3): Implement with SQLAlchemy mapped columns.
    """
    pass
