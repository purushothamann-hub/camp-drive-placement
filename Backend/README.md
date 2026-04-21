# Campus Placement Management System - Backend

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure

- `app/`
  - `main.py`: Entry point and router registration.
  - `core/`: Configuration and Security (JWT, Hashing).
  - `db/`: Database session and engine.
  - `models/`: SQLAlchemy models (User, Job, Application).
  - `schemas/`: Pydantic models for validation and response.
  - `routes/`: API endpoint definitions (Auth, Student, Admin).
  - `services/`: Business logic layer.
  - `utils/`: Utility functions (File upload).
- `uploads/`: Local storage for resumes.
