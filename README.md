# Clinic Booking System

A RESTful Clinic Booking System built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Alembic**.

The application enables clinic staff to manage doctors, patients, and appointments while enforcing scheduling rules that prevent double-booking and support appointment cancellation and rescheduling.

---

# Live Demo

## API

https://clinic-booking-system-3z3x.onrender.com/

## Swagger UI

https://clinic-booking-system-3z3x.onrender.com/docs

## ReDoc

https://clinic-booking-system-3z3x.onrender.com/redoc

---

# Features

- Manage doctors
- Manage patients
- Book appointments
- Cancel appointments
- Reschedule appointments
- Check doctor availability
- Prevent double-booking
- PostgreSQL database
- Alembic database migrations
- Interactive API documentation
- Cloud deployment on Render
- GitHub Actions CI pipeline

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

# Project Structure

```text
clinic-booking-system/
│
├── alembic/
│   └── versions/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── main.py
│
├── tests/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt
├── alembic.ini
├── README.md
└── REFLECTION.md
```

---

# System Design

The system follows a layered architecture that separates API endpoints, business logic, database models, and data validation.

The architecture is organized into:

- API Layer – Handles HTTP requests and responses.
- Service Layer – Implements appointment booking and scheduling rules.
- Database Layer – SQLAlchemy ORM models for persistence.
- Schema Layer – Pydantic models for validation and serialization.

This separation improves maintainability, readability, and future scalability.

---

# Database Models

## Doctor

Stores doctor information including:

- Name
- Email
- Phone number
- Specialization
- Working hours
- Active status

---

## Patient

Stores patient information including:

- Name
- Email
- Phone number
- Date of birth

---

## Appointment

Stores appointment details including:

- Doctor
- Patient
- Appointment date
- Appointment time
- Status
- Cancellation reason
- Creation timestamp

Appointments are linked to both doctors and patients through foreign key relationships.

---

# Appointment Scheduling Strategy

Appointments are scheduled in **30-minute intervals**.

During booking, the application validates:

- Appointment is within the doctor's working hours.
- Appointment is not in the past.
- Doctor is available.
- Requested slot has not already been booked.

Doctor availability is calculated dynamically based on:

- Doctor working hours
- Existing appointments
- Appointment duration (30 minutes)

This approach avoids storing thousands of unused time slots inside the database.

---

# Architectural Decisions

## Why PostgreSQL?

PostgreSQL was selected because it offers:

- Strong ACID compliance
- Reliable transactional integrity
- Excellent support for relational data
- Mature SQLAlchemy integration

Healthcare scheduling requires consistency, making PostgreSQL a suitable choice.

---

## Why Dynamic Availability?

Instead of pre-generating appointment slots, availability is calculated dynamically.

Advantages include:

- Less storage
- Easier schedule updates
- No synchronization problems
- Better scalability

---

## Layered Project Structure

Business logic is separated from API endpoints.

Benefits include:

- Easier testing
- Better code organization
- Higher maintainability
- Cleaner separation of responsibilities

---

# Engineering Trade-offs

| Decision      | Selected            | Alternative           | Reason                                         |
| ------------- | ------------------- | --------------------- | ---------------------------------------------- |
| Database      | PostgreSQL          | MongoDB               | Strong relational integrity                    |
| Scheduling    | Dynamic calculation | Pre-generated slots   | More flexible and less storage                 |
| ORM           | SQLAlchemy          | Raw SQL               | Cleaner and easier maintenance                 |
| API Framework | FastAPI             | Django REST Framework | Automatic validation and OpenAPI documentation |

---

# Getting Started

## Clone Repository

```bash
git clone https://github.com/Mica2000/Clinic-Booking_system.git
```

```bash
cd Clinic-Booking_system
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
APP_NAME=Clinic Booking System

DATABASE_URL=postgresql://username:password@localhost:5432/clinic_booking_db
```

---

# Database Setup

Run database migrations.

```bash
alembic upgrade head
```

---

# Run the Application

```bash
uvicorn app.main:app --reload
```

The application will be available at

```
http://127.0.0.1:8000
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

| Method | Endpoint                     | Description          |
| ------ | ---------------------------- | -------------------- |
| POST   | `/doctors/`                  | Create doctor        |
| GET    | `/doctors/`                  | List doctors         |
| GET    | `/doctors/{id}`              | Get doctor           |
| GET    | `/doctors/{id}/availability` | View available slots |

---

## Patients

| Method | Endpoint         | Description    |
| ------ | ---------------- | -------------- |
| POST   | `/patients/`     | Create patient |
| GET    | `/patients/`     | List patients  |
| GET    | `/patients/{id}` | Get patient    |

---

## Appointments

| Method | Endpoint                        | Description            |
| ------ | ------------------------------- | ---------------------- |
| POST   | `/appointments/`                | Book appointment       |
| PATCH  | `/appointments/{id}/cancel`     | Cancel appointment     |
| PATCH  | `/appointments/{id}/reschedule` | Reschedule appointment |

---

# Business Rules

The application enforces the following rules:

- Doctors cannot be double-booked.
- Appointments cannot be scheduled in the past.
- Appointments must fall within doctor working hours.
- Cancelled appointments cannot be cancelled again.
- Rescheduling validates the new appointment before releasing the old slot.
- Cancelled appointments free their booked time slot.
- Appropriate HTTP status codes and descriptive error messages are returned for validation failures.

---

# Testing

The project includes automated tests covering core appointment booking validation.

Tests focus on:

- Double-booking prevention
- Working hour validation
- Appointment scheduling rules

Run the tests using:

```bash
pytest
```

---

# Deployment

The application is deployed on **Render** using a **Neon PostgreSQL** database.

## Live URL

https://clinic-booking-system-3z3x.onrender.com/

---

# CI/CD

The project includes a GitHub Actions workflow located at:

```
.github/workflows/ci.yml
```

The workflow automatically:

- Checks out the repository
- Sets up Python
- Installs dependencies
- Runs the test suite
- Verifies the application builds successfully

Render is configured to automatically deploy the latest version whenever changes are merged into the production branch.

---

# Author

**David Maina**
