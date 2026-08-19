from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient


def normalize_datetime(value: datetime) -> datetime:
    """
    Normalize an incoming datetime to a naive datetime.

    Seconds and microseconds are removed because the system
    schedules appointments in 30-minute slots.
    """
    if value.tzinfo is not None:
        value = value.astimezone(timezone.utc).replace(tzinfo=None)

    return value.replace(second=0, microsecond=0)


def create_appointment(
    db: Session,
    doctor_id: int,
    patient_id: int,
    appointment_time: datetime,
):
    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .first()
    )

    if not doctor:
        raise ValueError("Doctor not found")

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise ValueError("Patient not found")

    # Normalize the incoming datetime before validation/storage.
    appointment_time = normalize_datetime(appointment_time)

    now = datetime.utcnow()

    if appointment_time <= now:
        raise ValueError(
            "Appointments cannot be booked in the past."
        )

    if appointment_time < now + timedelta(hours=1):
        raise ValueError(
            "Appointments must be booked at least 1 hour in advance."
        )

    if appointment_time.minute not in (0, 30):
        raise ValueError(
            "Appointments must start on a 30-minute boundary."
        )

    appointment_time_only = appointment_time.time()

    if (
        appointment_time_only < doctor.work_start_time
        or appointment_time_only >= doctor.work_end_time
    ):
        raise ValueError(
            "Appointment is outside the doctor's working hours."
        )

    existing = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_time == appointment_time,
            Appointment.status == "scheduled",
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Doctor is already booked at this time."
        )

    appointment = Appointment(
        doctor_id=doctor_id,
        patient_id=patient_id,
        appointment_time=appointment_time,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment


def cancel_appointment(
    db: Session,
    appointment_id: int,
    reason: str,
):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise ValueError("Appointment not found")

    if appointment.status == "cancelled":
        raise ValueError(
            "Appointment has already been cancelled."
        )

    appointment.status = "cancelled"
    appointment.cancellation_reason = reason

    db.commit()
    db.refresh(appointment)

    return appointment


def reschedule_appointment(
    db: Session,
    appointment_id: int,
    new_time: datetime,
):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise ValueError("Appointment not found")

    if appointment.status == "cancelled":
        raise ValueError(
            "Cancelled appointments cannot be rescheduled."
        )

    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == appointment.doctor_id)
        .first()
    )

    if not doctor:
        raise ValueError("Doctor not found")

    # Normalize the new appointment time.
    new_time = normalize_datetime(new_time)

    now = datetime.utcnow()

    if new_time <= now:
        raise ValueError(
            "Appointments cannot be rescheduled to the past."
        )

    if new_time < now + timedelta(hours=1):
        raise ValueError(
            "Appointments must be booked at least 1 hour in advance."
        )

    if new_time.minute not in (0, 30):
        raise ValueError(
            "Appointments must start on a 30-minute boundary."
        )

    new_time_only = new_time.time()

    if (
        new_time_only < doctor.work_start_time
        or new_time_only >= doctor.work_end_time
    ):
        raise ValueError(
            "Appointment is outside the doctor's working hours."
        )

    existing = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_time == new_time,
            Appointment.status == "scheduled",
            Appointment.id != appointment.id,
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Doctor is already booked at this time."
        )

    appointment.appointment_time = new_time
    appointment.status = "scheduled"
    appointment.cancellation_reason = None

    db.commit()
    db.refresh(appointment)

    return appointment


def get_available_slots(
    db: Session,
    doctor_id: int,
    appointment_date,
):
    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .first()
    )

    if not doctor:
        raise ValueError("Doctor not found")

    # Get all scheduled appointments for this doctor on this date.
    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "scheduled",
            func.date(Appointment.appointment_time)
            == appointment_date,
        )
        .all()
    )

    # Convert booked times to naive datetimes for comparison.
    booked_slots = {
        normalize_datetime(appointment.appointment_time)
        for appointment in appointments
    }

    slots = []

    current = datetime.combine(
        appointment_date,
        doctor.work_start_time,
    )

    end = datetime.combine(
        appointment_date,
        doctor.work_end_time,
    )

    while current < end:

        if current not in booked_slots:
            slots.append(current.isoformat())

        current += timedelta(minutes=30)

    return {
        "doctor_id": doctor_id,
        "date": appointment_date,
        "available_slots": slots,
    }