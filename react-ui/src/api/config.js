import axios from 'axios';

// Set the base URL for Axios
axios.defaults.baseURL = 'http://localhost:5000';

// Add an interceptor to include the JWT token in the headers if it exists
axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Export the configured Axios instance
export default axios;
