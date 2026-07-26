# Clinic Booking System

A RESTful Clinic Booking System built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Alembic**.

The system allows clinic staff to manage doctors, patients, and appointments while preventing double-booking and supporting appointment cancellation and rescheduling.

---

## Features

- Create doctors
- View doctor information
- Create patients
- View patient information
- Book appointments
- Cancel appointments
- Reschedule appointments
- Check doctor availability
- PostgreSQL database
- Alembic database migrations
- Interactive Swagger documentation

---

## Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Alembic
- Uvicorn

---

## Project Structure

```
clinic-booking-system/
│
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
├── requirements.txt
├── README.md
└── alembic.ini
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/Mica2000/Clinic-Booking_system.git
```

Enter the project.

```bash
cd Clinic-Booking_system
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
APP_NAME=Clinic Booking System
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/clinic_booking_db
```

---

## Database

Run migrations.

```bash
python -m alembic upgrade head
```

---

## Start the API

```bash
python -m uvicorn app.main:app --reload
```

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Available Endpoints

### Doctors

- POST /doctors
- GET /doctors
- GET /doctors/{id}
- GET /doctors/{id}/availability

### Patients

- POST /patients
- GET /patients
- GET /patients/{id}

### Appointments

- POST /appointments
- PATCH /appointments/{id}/cancel
- PATCH /appointments/{id}/reschedule

---

## Business Rules

- Doctors cannot be double-booked.
- Cancelled appointments are marked as `cancelled`.
- Rescheduled appointments automatically become `scheduled`.
- Appointment availability is checked before booking.

---

## Future Improvements

- Authentication and authorization
- Email notifications
- Appointment reminders
- Docker support
- Automated testing
- CI/CD deployment pipeline

---

## Author

David Maina
