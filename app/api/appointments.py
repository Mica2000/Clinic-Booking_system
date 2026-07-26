from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentReschedule,
)
from app.services.appointment_service import (
    create_appointment,
    cancel_appointment,
    reschedule_appointment,
    get_available_slots,
)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.post("/", response_model=AppointmentResponse)
def book_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_appointment(
            db,
            appointment.doctor_id,
            appointment.patient_id,
            appointment.appointment_time,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{appointment_id}/cancel")
def cancel(
    appointment_id: int,
    reason: str,
    db: Session = Depends(get_db),
):
    try:
        return cancel_appointment(
            db,
            appointment_id,
            reason,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{appointment_id}/reschedule")
def reschedule(
    appointment_id: int,
    data: AppointmentReschedule,
    db: Session = Depends(get_db),
):
    try:
        return reschedule_appointment(
            db,
            appointment_id,
            data.appointment_time,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/doctor/{doctor_id}")
def doctor_schedule(
    doctor_id: int,
    db: Session = Depends(get_db),
):
    return get_available_slots(db, doctor_id)