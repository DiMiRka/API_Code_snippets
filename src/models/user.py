import enum
from sqlalchemy import String, Integer, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

# from src.models.snippet import SnippetCode
from src.models.base import Base


class RoleEnum(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str]
    salt: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True, index=True)
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.USER, server_default=text("'USER'"))
    snippet: Mapped[list["SnippetCode"]] = relationship(
        "SnippetCode", back_populates="user", cascade="all, delete-orphan")
