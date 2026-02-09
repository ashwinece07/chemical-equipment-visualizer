import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';

const api = axios.create({ 
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Request interceptor to add JWT token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If error is 401 and we haven't tried to refresh yet
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                if (refreshToken) {
                    const response = await axios.post(`${API_URL}token/refresh/`, {
                        refresh: refreshToken
                    });

                    const { access } = response.data;
                    localStorage.setItem('access_token', access);

                    // Retry original request with new token
                    originalRequest.headers['Authorization'] = `Bearer ${access}`;
                    return api(originalRequest);
                }
            } catch (refreshError) {
                // Refresh failed, logout user
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// ============ AUTH ENDPOINTS ============
export const loginUser = async (username, password) => {
    const response = await api.post('login/', { username, password });
    if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        if (response.data.user) {
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
    }
    return response.data;
};

export const registerUser = async (username, email, password) => {
    const response = await api.post('signup/', { username, email, password });
    if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        if (response.data.user) {
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
    }
    return response.data;
};

export const logoutUser = async () => {
    try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
            await api.post('logout/', { refresh_token: refreshToken });
        }
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    }
};

// ============ USER PROFILE ENDPOINTS ============
export const getUserProfile = async () => {
    const response = await api.get('profile/');
    return response.data;
};

export const updateUserProfile = async (profileData) => {
    const response = await api.put('profile/', profileData);
    return response.data;
};

export const changePassword = async (oldPassword, newPassword) => {
    const response = await api.post('profile/password/', {
        old_password: oldPassword,
        new_password: newPassword
    });
    return response.data;
};

// ============ FILE UPLOAD & ANALYSIS ============
export const uploadCSV = async (formData, onUploadProgress) => {
    const response = await api.post('upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: onUploadProgress
    });
    return response.data;
};

export const getAnalysis = async (fileId) => {
    const response = await api.get(`analysis/${fileId}/`);
    return response.data;
};

export const compareDatasets = async (fileId1, fileId2) => {
    const response = await api.post('compare/', {
        file_id_1: fileId1,
        file_id_2: fileId2
    });
    return response.data;
};

// ============ HISTORY ============
export const getHistory = async () => {
    const response = await api.get('history/');
    return response.data;
};

export const deleteDataset = async (fileId) => {
    await api.delete(`delete/${fileId}/`);
};

// ============ EXPORT ENDPOINTS ============
export const downloadPDF = async (fileId, filename, password) => {
    try {
        const token = localStorage.getItem('access_token');
        const response = await axios.post(
            `${API_URL}export/pdf/${fileId}/`,
            { password },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                responseType: 'blob'
            }
        );
        
        const blob = new Blob([response.data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${filename}_Professional_Report.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('PDF Download Error:', error);
        throw error;
    }
};

export const downloadExcel = async (fileId, filename, password) => {
    try {
        const token = localStorage.getItem('access_token');
        const response = await axios.post(
            `${API_URL}export/excel/${fileId}/`,
            { password },
            {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                responseType: 'blob'
            }
        );
        
        const blob = new Blob([response.data], { 
            type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
        });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${filename}_Professional_Analysis.xlsx`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Excel Download Error:', error);
        throw error;
    }
};

// ============ UTILITY ============
export const isAuthenticated = () => {
    return !!localStorage.getItem('access_token');
};

export const getCurrentUser = () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
};

export default api;
