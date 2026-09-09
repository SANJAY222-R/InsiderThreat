import uuid

from sqlalchemy.orm import Session

from backend.app.auth.auth_handler import get_password_hash
from backend.app.models.user import User


class UserRepository:
    def get_user(self, db: Session, user_id: str):
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def count(self, db: Session):
        return db.query(User).count()

    def create_user(
        self,
        db: Session,
        username: str,
        password: str,
        email: str | None = None,
        full_name: str | None = None,
        role: str = "analyst",
        department: str | None = None,
    ):
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

    def update_user(self, db: Session, user_id: str, **kwargs):
        user = self.get_user(db, user_id)
        if not user:
            return None
        for k, v in kwargs.items():
            if v is not None and hasattr(user, k):
                setattr(user, k, v)
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: str):
        user = self.get_user(db, user_id)
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True
