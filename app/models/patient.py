from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.models.appointment import Appointment


class Patient(Base):
    __tablename__ = "patients"

    appointments: Mapped[list["Appointment"]] = relationship(
    back_populates="patient",
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

    date_of_birth: Mapped[date] = mapped_column(Date)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

from app.models.appointment import Appointment