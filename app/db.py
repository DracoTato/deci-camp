from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash


class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    deleted_at: Mapped[datetime | None]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    birthdate: Mapped[date]

    devices: Mapped[list["Device"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        email: str,
        password: str,
        birthdate: date,
    ):
        self.email = email
        self.birthdate = birthdate
        self.__set_password(password)

    def __set_password(self, value: str):
        self.password_hash = generate_password_hash(value)

    def check_password(self, value: str):
        return check_password_hash(self.password_hash, value)


class Device(Base):
    __tablename__ = "devices"
    __table_args__ = (UniqueConstraint("user_id", "user_agent"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_agent: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="devices")

    def __init__(self, user: User, user_agent: str):
        self.user = user
        self.user_agent = user_agent
