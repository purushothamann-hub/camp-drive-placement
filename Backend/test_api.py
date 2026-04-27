from fastapi.testclient import TestClient
from app.main import app
import json
import os

client = TestClient(app)
BASE_URL = "/api/v1"

def test_flow():
    results = []

    # 1. Register Admin
    print("Testing Register Admin...")
    admin_data = {
        "email": "admin@example.com",
        "name": "Admin User",
        "password": "adminpassword",
        "role": "admin"
    }
    r = client.post(f"{BASE_URL}/register", json=admin_data)
    results.append({"endpoint": "POST /register (Admin)", "status": r.status_code, "response": r.json()})

    # 2. Register Student
    print("Testing Register Student...")
    student_data = {
        "email": "student@example.com",
        "name": "Student User",
        "password": "studentpassword",
        "role": "student",
        "cgpa": 8.5,
        "department": "CSE",
        "year": 2024,
        "backlogs": 0
    }
    r = client.post(f"{BASE_URL}/register", json=student_data)
    results.append({"endpoint": "POST /register (Student)", "status": r.status_code, "response": r.json()})

    # 3. Login Admin
    print("Testing Login Admin...")
    r = client.post(f"{BASE_URL}/login", data={"username": "admin@example.com", "password": "adminpassword"})
    admin_token = r.json().get("access_token")
    results.append({"endpoint": "POST /login (Admin)", "status": r.status_code, "response": "Token received" if admin_token else "Failed"})

    # 4. Login Student
    print("Testing Login Student...")
    r = client.post(f"{BASE_URL}/login", data={"username": "student@example.com", "password": "studentpassword"})
    student_token = r.json().get("access_token")
    results.append({"endpoint": "POST /login (Student)", "status": r.status_code, "response": "Token received" if student_token else "Failed"})

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    student_headers = {"Authorization": f"Bearer {student_token}"}

    # 5. Admin Create Job
    print("Testing Admin Create Job...")
    job_data = {
        "company_name": "Google",
        "role": "Software Engineer",
        "description": "Develop cool things",
        "min_cgpa": 8.0,
        "allowed_departments": ["CSE", "ECE"],
        "allowed_years": [2024, 2025],
        "max_backlogs": 0,
        "deadline": "2026-12-31T23:59:59"
    }
    r = client.post(f"{BASE_URL}/admin/jobs", json=job_data, headers=admin_headers)
    job_id = r.json().get("id")
    results.append({"endpoint": "POST /admin/jobs", "status": r.status_code, "response": r.json()})

    # 6. Student View Jobs
    print("Testing Student View Jobs...")
    r = client.get(f"{BASE_URL}/student/jobs", headers=student_headers)
    results.append({"endpoint": "GET /student/jobs", "status": r.status_code, "response": f"Found {len(r.json())} jobs"})

    # 7. Student Upload Resume
    print("Testing Student Upload Resume...")
    resume_content = b"%PDF-1.4\n%test resume"
    with open("test_resume.pdf", "wb") as f:
        f.write(resume_content)
    
    with open("test_resume.pdf", "rb") as f:
        r = client.post(f"{BASE_URL}/student/upload-resume", files={"file": f}, headers=student_headers)
    results.append({"endpoint": "POST /student/upload-resume", "status": r.status_code, "response": r.json()})

    # 8. Student Apply for Job
    print("Testing Student Apply for Job...")
    r = client.post(f"{BASE_URL}/student/jobs/{job_id}/apply", headers=student_headers)
    app_id = r.json().get("id")
    results.append({"endpoint": "POST /student/jobs/{id}/apply", "status": r.status_code, "response": r.json()})

    # 9. Admin View Applicants
    print("Testing Admin View Applicants...")
    r = client.get(f"{BASE_URL}/admin/jobs/{job_id}/applicants", headers=admin_headers)
    results.append({"endpoint": "GET /admin/jobs/{id}/applicants", "status": r.status_code, "response": f"Found {len(r.json())} applicants"})

    # 10. Admin Update Status
    print("Testing Admin Update Status...")
    r = client.patch(f"{BASE_URL}/admin/applications/{app_id}/status", json={"status": "Shortlisted"}, headers=admin_headers)
    results.append({"endpoint": "PATCH /admin/applications/{id}/status", "status": r.status_code, "response": r.json()})

    # 11. Student Track Application
    print("Testing Student Track Application...")
    r = client.get(f"{BASE_URL}/student/applications", headers=student_headers)
    results.append({"endpoint": "GET /student/applications", "status": r.status_code, "response": r.json()})

    # Write to endpoints.md
    with open("endpoints.md", "w") as f:
        f.write("# API Testing Results\n\n")
        f.write("| Endpoint | Method | Status | Summary |\n")
        f.write("| --- | --- | --- | --- |\n")
        for res in results:
            parts = res["endpoint"].split(" ")
            method = parts[0]
            path = parts[1]
            f.write(f"| {path} | {method} | {res['status']} | {res['response']} |\n")

    print("Testing complete. Results saved to endpoints.md")
