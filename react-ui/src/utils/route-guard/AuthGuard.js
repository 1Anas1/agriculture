import React from 'react';
import { Redirect } from 'react-router-dom';
import { useAuth } from '../../provider/AuthProvider';

export const AuthGuard = ({ children }) => {
    const { token } = useAuth();

    if (!token) {
        return <Redirect to="/pages/login/login3" />;
    }

    return children;
};
