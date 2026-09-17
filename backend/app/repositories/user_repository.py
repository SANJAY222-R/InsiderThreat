import uuid
from typing import Any, List, Optional

from sqlalchemy.orm import Session

from backend.app.auth.auth_handler import get_password_hash
from backend.app.models.user import User


class UserRepository:
    def get_user(self, db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def count(self, db: Session) -> int:
        return db.query(User).count()

    def create_user(
        self,
        db: Session,
        username: str,
        password: str,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
        role: str = "analyst",
        department: Optional[str] = None,
    ) -> User:
        hashed_password = get_password_hash(password)
        db_user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            department=department,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_user(self, db: Session, user_id: str, **kwargs: Any) -> Optional[User]:
        user = self.get_user(db, user_id)
        if not user:
            return None
        for k, v in kwargs.items():
            if v is not None and hasattr(user, k):
                setattr(user, k, v)
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: str) -> bool:
        user = self.get_user(db, user_id)
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True
