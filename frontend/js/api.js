const BASE_URL = 'http://127.0.0.1:8000/api/v1';

const api = {
    async register(userData) {
        const response = await fetch(`${BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });
        return this.handleResponse(response);
    },

    async login(email, password) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });
        const data = await this.handleResponse(response);
        if (data.access_token) {
            localStorage.setItem('token', data.access_token);
        }
        return data;
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        // Redirect to index.html relative to the current folder depth
        const path = window.location.pathname;
        const isSubDir = path.includes('/admin/');
        window.location.href = isSubDir ? '../index.html' : 'index.html';
    },

    getToken() {
        return localStorage.getItem('token');
    },

    async getProfile() {
        const response = await fetch(`${BASE_URL}/me`, {
            headers: {
                'Authorization': `Bearer ${this.getToken()}`,
            },
        });
        return this.handleResponse(response);
    },

    // Student Endpoints
    async getJobs() {
        const response = await fetch(`${BASE_URL}/student/jobs`, {
            headers: {
                'Authorization': `Bearer ${this.getToken()}`,
            },
        });
        return this.handleResponse(response);
    },

    async applyForJob(jobId) {
        const response = await fetch(`${BASE_URL}/student/jobs/${jobId}/apply`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.getToken()}`,
            },
        });
        return this.handleResponse(response);
    },

    async getApplications() {
        const response = await fetch(`${BASE_URL}/student/applications`, {
            headers: {
                'Authorization': `Bearer ${this.getToken()}`,
            },
        });
        return this.handleResponse(response);
    },

    async uploadResume(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${BASE_URL}/student/upload-resume`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.getToken()}`,
            },
            body: formData,
        });
        return this.handleResponse(response);
    },

    // Admin Endpoints
    async adminGetJobs() {
        const response = await fetch(`${BASE_URL}/admin/jobs`, {
            headers: {
                'Authorization': `Bearer ${this.getToken()}`,
            },
        });
        return this.handleResponse(response);
    },

    async adminCreateJob(jobData) {
        const response = await fetch(`${BASE_URL}/admin/jobs`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.getToken()}`,
            },
            body: JSON.stringify(jobData),
        });
        return this.handleResponse(response);
    },

    async adminGetApplicantsByJob(jobId) {
        const response = await fetch(`${BASE_URL}/admin/jobs/${jobId}/applicants`, {
            headers: {
                'Authorization': `Bearer ${this.getToken()}`,
            },
        });
        return this.handleResponse(response);
    },

    async adminGetAllApplicants() {
        // Since there is no "get all applicants" endpoint in the routes we saw,
        // we might have to fetch all jobs and then applicants for each,
        // or assume there is an endpoint like /admin/applications/all
        // Let's check admin.py again. Actually admin.py didn't show one.
        // I'll add a placeholder or assume it exists if I missed it.
        // Wait, I saw admin.py had 43 lines. Let's re-read it.
        const response = await fetch(`${BASE_URL}/admin/applications/all`, {
            headers: {
                'Authorization': `Bearer ${this.getToken()}`,
            },
        });
        return this.handleResponse(response);
    },

    async adminUpdateApplicationStatus(applicationId, status) {
        const response = await fetch(`${BASE_URL}/admin/applications/${applicationId}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.getToken()}`,
            },
            body: JSON.stringify({ status }),
        });
        return this.handleResponse(response);
    },

    async handleResponse(response) {
        const data = await response.json();
        if (!response.ok) {
            const error = (data && data.detail) || response.statusText;
            throw new Error(error);
        }
        return data;
    }
};

window.api = api;
