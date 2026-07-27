# Clinic Booking System

A RESTful Clinic Booking System built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Alembic**.

The system enables clinic staff to manage doctors, patients, and appointments while enforcing scheduling rules such as doctor working hours, 30-minute appointment slots, double-booking prevention, appointment cancellation, and rescheduling.

---

# Live Application

### API Base URL

https://clinic-booking-system-3z3x.onrender.com/

### Swagger UI

https://clinic-booking-system-3z3x.onrender.com/docs

### ReDoc

https://clinic-booking-system-3z3x.onrender.com/redoc

---

# Features

- Create and manage doctors
- Create and manage patients
- Book appointments
- Cancel appointments with a mandatory reason
- Reschedule appointments
- View doctor availability
- View upcoming patient appointments
- Prevent double-booking
- Enforce doctor working hours
- Enforce 30-minute appointment slots
- Prevent appointments in the past
- Prevent bookings within one hour of the current time
- PostgreSQL database
- Alembic database migrations
- Interactive API documentation
- CI/CD using GitHub Actions
- Cloud deployment on Render

---

# Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy ORM
- PostgreSQL (Neon)
- Alembic
- Uvicorn
- Pydantic
- GitHub Actions
- Render

---

# System Design

## Database Models

### Doctor

| Field           |
| --------------- |
| id              |
| first_name      |
| last_name       |
| email           |
| phone_number    |
| specialization  |
| work_start_time |
| work_end_time   |
| is_active       |
| created_at      |

### Patient

| Field        |
| ------------ |
| id           |
| first_name   |
| last_name    |
| email        |
| phone_number |
| created_at   |

### Appointment

| Field               |
| ------------------- |
| id                  |
| doctor_id           |
| patient_id          |
| appointment_time    |
| status              |
| cancellation_reason |

Relationships

- One Doctor → Many Appointments
- One Patient → Many Appointments

---

# Appointment Scheduling Strategy

Appointments are dynamically validated instead of pre-generating appointment slots.

Whenever a booking request is received, the system verifies:

- the doctor exists
- the patient exists
- the appointment is not in the past
- the appointment is at least one hour ahead of the current time
- the appointment begins on a 30-minute interval
- the appointment falls within the doctor's working hours
- the requested slot has not already been booked

Doctor availability is calculated dynamically by generating every 30-minute slot within the doctor's working hours for a selected date and removing any booked appointments.

---

# Architectural Decisions

### Modular Architecture

The project separates responsibilities into:

- API routes
- Database models
- Schemas
- Business services
- Database configuration

This keeps business logic separate from HTTP endpoints and improves maintainability.

### Service Layer

Appointment validation is handled inside the service layer rather than inside API routes, making the code easier to test and reuse.

### SQL Database

PostgreSQL was selected because appointment scheduling requires:

- relational data
- transactions
- constraints
- reliable querying
- future scalability

---

# Engineering Trade-offs

## SQL vs NoSQL

PostgreSQL was chosen because appointments have strong relationships between doctors and patients, and transactional consistency is important for preventing double-booking.

## Dynamic Availability vs Stored Slots

Instead of storing every possible appointment slot, available slots are generated dynamically.

Advantages:

- less storage
- no synchronization issues
- reflects doctor working hours automatically

Trade-off:

- slightly more computation during availability requests

---

# Project Structure

```text
clinic-booking-system/

├── .github/
│   └── workflows/
│       └── ci.yml
│
├── alembic/
│
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
├── REFLECTION.md
└── alembic.ini
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/Mica2000/Clinic-Booking_system.git
```

Move into the project.

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

# Environment Variables

Create a `.env` file.

```env
APP_NAME=Clinic Booking System
DATABASE_URL=postgresql://username:password@host/database
```

---

# Database Migration

Run all migrations.

```bash
alembic upgrade head
```

---

# Run the Application

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

Swagger

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## Doctors

| Method | Endpoint                                            | Description                    |
| ------ | --------------------------------------------------- | ------------------------------ |
| POST   | `/doctors/`                                         | Create doctor                  |
| GET    | `/doctors/`                                         | List doctors                   |
| GET    | `/doctors/{doctor_id}`                              | Get doctor                     |
| GET    | `/doctors/{doctor_id}/availability?date=YYYY-MM-DD` | View available 30-minute slots |

---

## Patients

| Method | Endpoint                              | Description                |
| ------ | ------------------------------------- | -------------------------- |
| POST   | `/patients/`                          | Create patient             |
| GET    | `/patients/`                          | List patients              |
| GET    | `/patients/{patient_id}`              | Get patient                |
| GET    | `/patients/{patient_id}/appointments` | View upcoming appointments |

---

## Appointments

| Method | Endpoint                                    | Description            |
| ------ | ------------------------------------------- | ---------------------- |
| POST   | `/appointments/`                            | Book appointment       |
| PATCH  | `/appointments/{appointment_id}/cancel`     | Cancel appointment     |
| PATCH  | `/appointments/{appointment_id}/reschedule` | Reschedule appointment |

---

# Business Rules

The system enforces the following rules:

- Doctors cannot be double-booked.
- Appointments must occur during a doctor's configured working hours.
- Appointments must start on 30-minute intervals.
- Appointments cannot be scheduled in the past.
- New appointments must be booked at least one hour in advance.
- Cancelled appointments cannot be cancelled twice.
- Cancelled appointments cannot be rescheduled.
- Doctor availability returns all free 30-minute appointment blocks for a selected date.
- Upcoming patient appointments are returned in chronological order.

---

# Testing

The repository includes automated tests covering the appointment booking logic.

Tests can be executed using:

```bash
pytest
```

---

# CI/CD

GitHub Actions automatically runs the project's test suite whenever changes are pushed or a Pull Request is opened.

The production application is deployed on **Render**.

Deployment is triggered from the **main** branch after successful integration.

---

# Author

**David Maina**
