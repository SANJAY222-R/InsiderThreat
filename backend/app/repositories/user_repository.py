from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.schemas.user_schema import UserCreate
from backend.app.auth.auth_handler import get_password_hash
import uuid

class UserRepository:
    def get_user(self, db: Session, user_id: str):
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(
            id=str(uuid.uuid4()),
            username=user.username,
            hashed_password=hashed_password,
            role=user.role,
            is_active=user.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
