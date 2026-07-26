from datetime import datetime, time
from sqlalchemy import Boolean, DateTime, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.models.appointment import Appointment

class Doctor(Base):
    __tablename__ = "doctors"

    appointments: Mapped[list["Appointment"]] = relationship(
    back_populates="doctor",
    cascade="all, delete-orphan",
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)

    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(String(20))

    specialization: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    work_start_time: Mapped[time] = mapped_column(
    Time,
    nullable=False,
    )

    work_end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

from app.models.appointment import Appointment