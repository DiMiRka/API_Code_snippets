import uuid
from datetime import datetime
from sqlalchemy import TIMESTAMP, ForeignKey, Column, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.base import Base
# from src.models.user import User


class SnippetCode(Base):
    __tablename__ = "snippet"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    code: Mapped[str]
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="snippet")

    share_id = Column(String, unique=True, default=lambda: str(uuid.uuid4()), index=True)
