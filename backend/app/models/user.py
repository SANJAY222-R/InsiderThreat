
"""
User ORM Model
===============

Represents system users (analysts, admins, auditors).

Phase 0: Schema stub only.
"""

__all__ = ["User"]


class User:
    """
    User database model.

    Attributes:
        id: Primary key.
        username: Unique login name.
        email: User email address.
        hashed_password: Bcrypt-hashed password.
        role: User role (admin, analyst, auditor, viewer).
        is_active: Account active flag.
        created_at: Account creation timestamp.
        updated_at: Last update timestamp.

    TODO (Phase 1): Implement with SQLAlchemy mapped columns.
    """
    pass
