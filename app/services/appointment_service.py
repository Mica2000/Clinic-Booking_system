from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient


def create_appointment(
    db: Session,
    doctor_id: int,
    patient_id: int,
    appointment_time,
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise ValueError("Doctor not found")

    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise ValueError("Patient not found")

    # Handle timezone-aware and naive datetimes
    if appointment_time.tzinfo:
        now = datetime.now(timezone.utc)
    else:
        now = datetime.now()

    # Cannot book in the past
    if appointment_time <= now:
        raise ValueError("Appointments cannot be booked in the past.")

    # Bonus requirement
    if appointment_time < now + timedelta(hours=1):
        raise ValueError(
            "Appointments must be booked at least 1 hour in advance."
        )

    # Only allow 30-minute slots
    if (
        appointment_time.minute not in (0, 30)
        or appointment_time.second != 0
        or appointment_time.microsecond != 0
    ):
        raise ValueError(
            "Appointments must start on a 30-minute boundary."
        )

    # Check doctor's working hours
    appointment_time_only = appointment_time.time()

    if (
        appointment_time_only < doctor.work_start_time
        or appointment_time_only >= doctor.work_end_time
    ):
        raise ValueError(
            "Appointment is outside the doctor's working hours."
        )

    # Prevent double booking
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
        raise ValueError("Appointment has already been cancelled.")

    appointment.status = "cancelled"
    appointment.cancellation_reason = reason

    db.commit()
    db.refresh(appointment)

    return appointment


def reschedule_appointment(
    db: Session,
    appointment_id: int,
    new_time,
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

    if new_time.tzinfo:
        now = datetime.now(timezone.utc)
    else:
        now = datetime.now()

    if new_time <= now:
        raise ValueError(
            "Appointments cannot be rescheduled to the past."
        )

    if new_time < now + timedelta(hours=1):
        raise ValueError(
            "Appointments must be booked at least 1 hour in advance."
        )

    if (
        new_time.minute not in (0, 30)
        or new_time.second != 0
        or new_time.microsecond != 0
    ):
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
    date,
):
    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .first()
    )

    if not doctor:
        raise ValueError("Doctor not found")

    booked_slots = {
        appointment.appointment_time.replace(
            tzinfo=None
        )
        for appointment in db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "scheduled",
        )
    }

    slots = []

    current = datetime.combine(
        date,
        doctor.work_start_time,
    )

    end = datetime.combine(
        date,
        doctor.work_end_time,
    )

    while current < end:
        if current not in booked_slots:
            slots.append(current)

        current += timedelta(minutes=30)

    return slots