# API Endpoint Documentation (v1)

This document provides the details of all API endpoints, including request parameters, headers, and response formats for both Student and Admin roles.

## Base URL
`http://127.0.0.1:8000/api/v1`

---

## 1. Authentication

### POST `/register`
Register a new user (Admin or Student).

- **Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "email": "user@example.com",
  "name": "Full Name",
  "password": "strongpassword",
  "role": "student", // or "admin"
  "cgpa": 8.5,       // Student only
  "department": "CSE", // Student only
  "year": 2024,      // Student only
  "backlogs": 0      // Student only
}
```
- **Response (200 OK)**:
```json
{
  "email": "user@example.com",
  "name": "Full Name",
  "role": "student",
  "id": 1,
  "cgpa": 8.5,
  "department": "CSE",
  "year": 2024,
  "backlogs": 0,
  "resume_url": null,
  "created_at": "2024-04-23T12:00:00"
}
```

### POST `/login`
Authenticate and receive a JWT token.

- **Headers**: `Content-Type: application/x-www-form-urlencoded`
- **Request Body (Form Data)**:
  - `username`: email@example.com
  - `password`: password
- **Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 2. Admin Endpoints
*Requires Header: `Authorization: Bearer <ADMIN_TOKEN>`*

### POST `/admin/jobs`
Create a new job posting.

- **Request Body**:
```json
{
  "company_name": "Google",
  "role": "Software Engineer",
  "description": "Job description here...",
  "min_cgpa": 8.0,
  "allowed_departments": ["CSE", "ECE"],
  "allowed_years": [2024, 2025],
  "max_backlogs": 0,
  "deadline": "2026-12-31T23:59:59"
}
```
- **Response (200 OK)**: Returns the created Job object with `id`.

### GET `/admin/jobs/{job_id}/applicants`
List all students who applied for a specific job.

- **Response (200 OK)**: Array of Application objects including student profiles.

### PATCH `/admin/applications/{application_id}/status`
Update the status of a student's application.

- **Request Body**:
```json
{
  "status": "Shortlisted" // Options: "Applied", "Shortlisted", "Selected", "Rejected"
}
```
- **Response (200 OK)**: Updated Application object.

---

## 3. Student Endpoints
*Requires Header: `Authorization: Bearer <STUDENT_TOKEN>`*

### GET `/student/jobs`
List all available job drives.

- **Response (200 OK)**: Array of Job objects.

### POST `/student/jobs/{job_id}/apply`
Apply for a specific job drive. 
*Note: Requires a resume to be uploaded first.*

- **Response (200 OK)**: Application confirmation object.

### GET `/student/applications`
Track statuses of all your applications.

- **Response (200 OK)**: Array of your applications with current status.

### POST `/student/upload-resume`
Upload resume in PDF format.

- **Request Body**: `multipart/form-data`
  - `file`: (Binary PDF)
- **Response (200 OK)**:
```json
{
  "message": "Resume uploaded successfully",
  "path": "uploads/resumes/2.pdf"
}
```

---

## 🔒 Security & RBAC
- **JWT**: Tokens expire in 30 minutes.
- **Admin**: Can create jobs and update status. Accesses `/api/v1/admin/*`.
- **Student**: Can view jobs and apply. Accesses `/api/v1/student/*`.
- **Validation**: CGPA must be 0-10, deadlines must be in the future, backlogs must be non-negative.
