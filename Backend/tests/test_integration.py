import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings

@pytest.mark.asyncio
async def test_full_workflow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Register Admin
        admin_data = {
            "email": "admin_test@example.com",
            "password": "password123",
            "name": "Admin Test",
            "role": "admin"
        }
        response = await ac.post(f"{settings.API_V1_STR}/register", json=admin_data)
        assert response.status_code in [200, 400] # 400 if already exists

        # 2. Login Admin
        login_data = {
            "username": "admin_test@example.com",
            "password": "password123"
        }
        response = await ac.post(f"{settings.API_V1_STR}/login", data=login_data)
        assert response.status_code == 200
        admin_token = response.json()["access_token"]
        headers_admin = {"Authorization": f"Bearer {admin_token}"}

        # 3. Create Job
        job_data = {
            "company_name": "Test Company",
            "role": "Test SDE",
            "description": "Test Description",
            "min_cgpa": 7.0,
            "max_backlogs": 0,
            "deadline": "2026-12-31",
            "allowed_departments": ["CSE", "IT"],
            "allowed_years": [2025]
        }
        response = await ac.post(f"{settings.API_V1_STR}/admin/jobs", json=job_data, headers=headers_admin)
        assert response.status_code == 200
        job_id = response.json()["id"]

        # 4. Register Student
        student_data = {
            "email": "student_test@example.com",
            "password": "password123",
            "name": "Student Test",
            "role": "student",
            "cgpa": 8.5,
            "department": "CSE",
            "year": 2025
        }
        response = await ac.post(f"{settings.API_V1_STR}/register", json=student_data)
        assert response.status_code in [200, 400]

        # 5. Login Student
        login_data_student = {
            "username": "student_test@example.com",
            "password": "password123"
        }
        response = await ac.post(f"{settings.API_V1_STR}/login", data=login_data_student)
        assert response.status_code == 200
        student_token = response.json()["access_token"]
        headers_student = {"Authorization": f"Bearer {student_token}"}

        # 5b. Upload Resume
        files = {"file": ("resume.pdf", b"dummy content", "application/pdf")}
        response = await ac.post(f"{settings.API_V1_STR}/student/upload-resume", files=files, headers=headers_student)
        assert response.status_code == 200

        # 6. Apply for Job
        response = await ac.post(f"{settings.API_V1_STR}/student/jobs/{job_id}/apply", headers=headers_student)
        assert response.status_code == 200

        # 7. Update Status (as Admin)
        # First get the application ID
        response = await ac.get(f"{settings.API_V1_STR}/admin/jobs/{job_id}/applicants", headers=headers_admin)
        assert response.status_code == 200
        applicants = response.json()
        application_id = [a["id"] for a in applicants if a["student"]["email"] == "student_test@example.com"][0]

        status_data = {"status": "Shortlisted"}
        response = await ac.patch(f"{settings.API_V1_STR}/admin/applications/{application_id}/status", json=status_data, headers=headers_admin)
        assert response.status_code == 200
        assert response.json()["status"] == "Shortlisted"

        print("Integration test passed successfully!")
