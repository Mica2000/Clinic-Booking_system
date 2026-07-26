from fastapi import FastAPI

app = FastAPI(
    title="Clinic Appointment Booking API",
    description="Backend API for managing doctors, patients, and appointments.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Clinic Appointment Booking API!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }