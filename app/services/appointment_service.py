from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient


def create_appointment(db: Session, doctor_id: int, patient_id: int, appointment_time):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise ValueError("Doctor not found")

    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise ValueError("Patient not found")

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
        raise ValueError("Doctor is already booked at this time.")

    appointment = Appointment(
        doctor_id=doctor_id,
        patient_id=patient_id,
        appointment_time=appointment_time,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment


def cancel_appointment(db: Session, appointment_id: int, reason: str):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise ValueError("Appointment not found")

    appointment.status = "cancelled"
    appointment.cancellation_reason = reason

    db.commit()
    db.refresh(appointment)

    return appointment


def reschedule_appointment(db: Session, appointment_id: int, new_time):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise ValueError("Appointment not found")

    existing = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_time == new_time,
            Appointment.status == "scheduled",
        )
        .first()
    )

    if existing:
        raise ValueError("Doctor is already booked at this time.")

    appointment.appointment_time = new_time
    appointment.status = "scheduled"
    appointment.cancellation_reason = None

    db.commit()
    db.refresh(appointment)

    return appointment


def get_available_slots(db: Session, doctor_id: int):
    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "scheduled",
        )
        .all()
    )

    return appointments