from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.doctor import Doctor
from app.schemas.schemas import DoctorCreate, DoctorResponse


router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("/", response_model=DoctorResponse)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
):
    new_doctor = Doctor(**doctor.model_dump())

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor

@router.get("/", response_model=list[DoctorResponse])
def list_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
):
    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .first()
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found",
        )

    return doctor