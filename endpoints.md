# Campus Placement Management System - API Report

## Overview
All business rules including eligibility, RBAC, and status transitions have been validated.

## API Summary
| Feature | Endpoint | Status | Result |
| :--- | :--- | :--- | :--- |
| Admin Reg | `POST /register` | 200 | Success |
| Student Reg | `POST /register` | 200 | Success |
| RBAC Check | `POST /admin/jobs` | 403 | Blocked Student |
| Job Creation | `POST /admin/jobs` | 200 | Created |
| Apply (No Resume) | `POST /student/jobs/{id}/apply` | 400 | Blocked |
| Apply (Success) | `POST /student/jobs/{id}/apply` | 200 | Applied |
| Shortlist | `PATCH /applications/{id}/status` | 200 | Success |
| Apply (Low CGPA) | `POST /student/jobs/{id}/apply` | 400 | Blocked |
| Apply (Wrong Dept) | `POST /student/jobs/{id}/apply` | 400 | Blocked |
| Status Lock | `PATCH /applications/{id}/status` | 400 | Transition Blocked |

## Test Cases
1. Registration & Login (Success)
2. RBAC Enforcement (Success)
3. Resume Requirement (Success)
4. Eligibility Check (Success)
5. Status Workflow (Success)
6. Edge Case Validations (Success)
