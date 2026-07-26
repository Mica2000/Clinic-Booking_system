from fastapi import FastAPI

from app.api.doctors import router as doctor_router
from app.api.patients import router as patient_router
from app.api.appointments import router as appointment_router

app = FastAPI(
    title="Clinic Appointment Booking API",
    description="Backend API for managing doctors, patients and appointments.",
    version="1.0.0",
)

app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(appointment_router)


@app.get("/")
def root():
    return {"message": "Clinic Booking API"}


@app.get("/health")
def health():
    return {"status": "healthy"}