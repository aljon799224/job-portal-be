"""User Schema."""

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """User Base Class."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    username: str
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class UserIn(UserBase):
    """User In Class."""

    password: str


class UserUpdate(UserBase):
    """User Patch Class."""

    pass


class UserOut(UserBase):
    """User Out Class."""

    id: int
