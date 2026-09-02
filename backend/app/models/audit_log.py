
"""
Audit Log ORM Model
====================

Immutable audit trail of system actions.

Phase 0: Schema stub only.
"""

__all__ = ["AuditLog"]


class AuditLog:
    """
    Audit log database model.

    Attributes:
        id: Primary key.
        user_id: Actor user ID.
        action: Action performed (login, predict, export, config_change).
        resource_type: Resource type affected.
        resource_id: Specific resource ID.
        details: JSON action details.
        ip_address: Client IP.
        timestamp: Action timestamp.

    TODO (Phase 2): Implement with SQLAlchemy mapped columns.
    """
    pass
