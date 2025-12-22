import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  confirmEmail: (token) => api.get(`/auth/confirm/${token}`),
  forgotPassword: (data) => api.post('/auth/forgot-password', data),
  resetPassword: (token, data) => api.post(`/auth/reset-password/${token}`, data),
};

export const userAPI = {
  getProfile: () => api.get('/users/profile'),
  uploadProfileImage: (formData) => {
    return api.post('/users/profile/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export const documentAPI = {
  upload: (formData) => {
    return api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  list: () => api.get('/documents/'),
};

export const qcmAPI = {
  generate: (data) => api.post('/qcm/generate', data),
  list: () => api.get('/qcm/'),
  getById: (qcmId) => api.get(`/qcm/${qcmId}`),
  delete: (qcmId) => api.delete(`/qcm/${qcmId}`),
  updateQuestion: (questionId, data) => api.put(`/qcm/question/${questionId}`, data),
  downloadPDF: (qcmId) => api.get(`/qcm/${qcmId}/download`, { responseType: 'blob' }),
};

export const examAPI = {
  create: (data) => api.post('/exams/create', data),
  join: (data) => api.post('/exams/join', data),
  submit: (data) => api.post('/exams/submit', data),
  listActive: () => api.get('/exams/active'),
  listProfessorExams: () => api.get('/exams/professor/list'),
  getResults: (sessionId) => api.get(`/exams/${sessionId}/results`),
  getLiveTracking: (sessionId) => api.get(`/exams/${sessionId}/live`),
  deleteSession: (sessionId) => api.delete(`/exams/${sessionId}`),
  listAll: () => api.get('/exams/all'),
};

export const schoolAPI = {
  listBranches: () => api.get('/school/branches'),
  getBranch: (branchId) => api.get(`/school/branches/${branchId}`),
  createBranch: (data) => api.post('/school/branch', data),
};

export const statsAPI = {
  getDashboardStats: () => api.get('/stats/dashboard'),
  getBranchStats: (branchId) => api.get(`/stats/branch/${branchId}`),
  getHardestQuestions: () => api.get('/stats/charts/hardest-questions'),
  getCompletionRate: () => api.get('/stats/charts/completion-rate'),
  getBranchPerformance: () => api.get('/stats/charts/branch-performance'),
};

export default api;
