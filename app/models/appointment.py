from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.doctor import Doctor
    from app.models.patient import Patient


class Appointment(Base):
    __tablename__ = "appointments"

    doctor: Mapped["Doctor"] = relationship(
    back_populates="appointments"
    )

    patient: Mapped["Patient"] = relationship(
        back_populates="appointments"
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id"),
        nullable=False,
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
    )

    appointment_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="scheduled",
    )

    cancellation_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )