"""User Repository."""

from http import HTTPStatus
from typing import Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.password import EmailSchema
from app.schemas.user import UserIn
from exceptions.exceptions import DatabaseException


class UserRepository(BaseRepository[User, UserIn, UserIn]):
    """User Repository Class."""

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[User]:
        """Get by email."""
        return db.query(User).filter(User.email == email).first()

    FAKE_OTP = "111111"

    def send_otp(self, db: Session, email: EmailSchema) -> JSONResponse:
        email = email.email
        user = self.get_by_email(db, email=email)
        if not user:
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={"message": "User not found"},
            )

        # Simulate sending OTP (console log only)
        print(f"[FAKE OTP] Sent OTP to {email}: {self.FAKE_OTP}")
        return JSONResponse(content={"message": "OTP sent"})

    def reset_password_with_otp(
            self, db: Session, email: str, otp: str, new_password: str
    ) -> JSONResponse:
        user = self.get_by_email(db, email=email)
        if not user:
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={"message": "User not found"},
            )

        if otp != self.FAKE_OTP:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={"message": "Invalid OTP"},
            )

        user.hashed_password = get_password_hash(new_password)
        db.add(user)
        db.commit()

        return JSONResponse(content={"message": "Password reset successful!"})

    @staticmethod
    def get_by_username(db: Session, *, username: str) -> Optional[User]:
        """Get by username."""
        return db.query(User).filter(User.username == username).first()

    def create_user_with_password(
        self, db: Session, *, obj_in: UserIn
    ) -> Optional[User]:
        """Create user with password."""
        try:
            obj_in_data = jsonable_encoder(obj_in)

            obj_in_data.update({"hashed_password": get_password_hash(obj_in.password)})
            del obj_in_data["password"]
            db_obj = self.model(**obj_in_data)  # type: ignore
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        except exc.IntegrityError as e:
            error = e.orig.args

            raise DatabaseException(
                status_code=HTTPStatus.CONFLICT, detail=error[0]
            ) from e

        except Exception as e:
            raise DatabaseException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            ) from e

        return db_obj

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        """Authenticate."""
        user = self.get_by_username(db, username=username)  # noqa
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
