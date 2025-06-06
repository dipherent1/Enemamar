from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, ARRAY
from sqlalchemy.sql import func
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID  # For PostgreSQL
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.model import User

class Update(Base):
    __tablename__ = "updates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    update_counts: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="update", uselist=False)