# Clinic Booking System

A RESTful Clinic Booking System built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Alembic**. The system enables clinic staff to manage doctors, patients, and appointments while enforcing scheduling rules that prevent double-booking and support appointment cancellation and rescheduling.

## Live Demo

**API Base URL**

https://clinic-booking-system-3z3x.onrender.com/

**Swagger Documentation**

https://clinic-booking-system-3z3x.onrender.com/docs

**ReDoc Documentation**

https://clinic-booking-system-3z3x.onrender.com/redoc

---

## Features

- Manage doctor records
- Manage patient records
- Book appointments
- Cancel appointments
- Reschedule appointments
- Check doctor availability
- Prevent double-booking of doctors
- PostgreSQL database integration
- Alembic database migrations
- Interactive API documentation with Swagger UI and ReDoc

---

## Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Alembic
- Uvicorn
- Pydantic

---

## Project Structure

```text
clinic-booking-system/
│
├── alembic/                 # Database migrations
├── app/
│   ├── api/                 # API routes
│   ├── core/                # Configuration and database setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── main.py              # FastAPI application entry point
│
├── tests/
├── requirements.txt
├── README.md
└── alembic.ini
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Mica2000/Clinic-Booking_system.git
```

### 2. Navigate into the project

```bash
cd Clinic-Booking_system
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
APP_NAME=Clinic Booking System
DATABASE_URL=postgresql://username:password@localhost:5432/clinic_booking_db
```

Replace:

- `username` with your PostgreSQL username
- `password` with your PostgreSQL password

---

## Database Setup

Run all database migrations:

```bash
alembic upgrade head
```

---

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## API Documentation

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Doctors

| Method | Endpoint                            | Description               |
| ------ | ----------------------------------- | ------------------------- |
| POST   | `/doctors/`                         | Create a doctor           |
| GET    | `/doctors/`                         | List all doctors          |
| GET    | `/doctors/{doctor_id}`              | Get doctor by ID          |
| GET    | `/doctors/{doctor_id}/availability` | Check doctor availability |

### Patients

| Method | Endpoint                 | Description       |
| ------ | ------------------------ | ----------------- |
| POST   | `/patients/`             | Create a patient  |
| GET    | `/patients/`             | List all patients |
| GET    | `/patients/{patient_id}` | Get patient by ID |

### Appointments

| Method | Endpoint                                    | Description               |
| ------ | ------------------------------------------- | ------------------------- |
| POST   | `/appointments/`                            | Book an appointment       |
| PATCH  | `/appointments/{appointment_id}/cancel`     | Cancel an appointment     |
| PATCH  | `/appointments/{appointment_id}/reschedule` | Reschedule an appointment |

---

## Business Rules

The system enforces the following scheduling rules:

- A doctor cannot have overlapping appointments.
- Cancelled appointments are marked with a `cancelled` status.
- Rescheduled appointments are automatically updated to `scheduled`.
- Doctor availability is validated before an appointment is created.
- Appointment conflicts return an appropriate error response.

---

## Example Workflow

1. Create a doctor.
2. Create a patient.
3. Book an appointment.
4. Check the doctor's availability.
5. Reschedule or cancel the appointment if needed.

---

## Author

**David Maina**

---
