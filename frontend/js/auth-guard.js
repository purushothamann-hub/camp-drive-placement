(function() {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    const path = window.location.pathname;
    
    // Pages that don't need auth
    const isLoginPage = path.endsWith('index.html') || path === '/' || path.endsWith('/') || path.endsWith('/frontend/');
    
    if (!token || !userStr) {
        if (!isLoginPage) {
            // Redirect to login if not already there
            const loginPath = path.includes('/admin/') ? '../index.html' : 'index.html';
            window.location.href = loginPath;
        }
        return;
    }

    const user = JSON.parse(userStr);
    const isAdminPage = path.includes('/admin/');
    const isSharedPage = path.includes('job-details.html');
    const isStudentPage = !isAdminPage && !isLoginPage && !isSharedPage;

    // Redirect if authenticated user tries to access login page
    if (isLoginPage) {
        if (user.role === 'admin') {
            window.location.href = path.endsWith('/') ? 'admin/dashboard.html' : 'admin/dashboard.html';
        } else {
            window.location.href = path.endsWith('/') ? 'dashboard.html' : 'dashboard.html';
        }
        return;
    }

    // Role-based access control
    if (user.role === 'student' && isAdminPage) {
        window.location.href = '../dashboard.html';
    } else if (user.role === 'admin' && isStudentPage) {
        window.location.href = 'admin/dashboard.html';
    }
})();
