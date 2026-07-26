from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, EmailStr


# Doctor
class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    specialization: str
    work_start_time: time
    work_end_time: time

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

# Patient
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    date_of_birth: date

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Appointment
class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_time: datetime

class AppointmentReschedule(BaseModel):
    appointment_time: datetime

class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_time: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)