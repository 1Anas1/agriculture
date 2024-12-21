import React, { createContext, useState, useContext } from 'react';
import axios from '../api/config'; // Use the pre-configured Axios instance

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('token') || null);
    const [user, setUser] = useState(null); // Store user details if needed
    const [loading, setLoading] = useState(false);

    // Login function
    const login = async (email, password) => {
        try {
            setLoading(true);
            const response = await axios.post('/auth/login', { email, password });
            const { token } = response.data;

            localStorage.setItem('token', token);
            setToken(token);
            // Optional: Fetch and set user details here if needed
            return { success: true };
        } catch (error) {
            console.error('Login error:', error.response || error.message);
            return { success: false, message: error.response?.data?.error || 'An error occurred' };
        } finally {
            setLoading(false);
        }
    };

    // Register function
    const register = async (name, email, password) => {
        try {
            setLoading(true);
            const response = await axios.post('/auth/register', { name, email, password });
            return { success: true, message: response.data.message };
        } catch (error) {
            console.error('Register error:', error.response || error.message);
            return { success: false, message: error.response?.data?.error || 'An error occurred' };
        } finally {
            setLoading(false);
        }
    };

    // Logout function
    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
    };

    return <AuthContext.Provider value={{ token, user, login, register, logout, loading }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
