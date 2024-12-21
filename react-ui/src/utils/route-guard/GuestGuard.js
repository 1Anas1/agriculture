import React from 'react';
import { Redirect, Route } from 'react-router-dom';
import { useAuth } from '../../provider/AuthProvider';

export const GuestGuard = ({ children }) => {
    const { token } = useAuth();

    if (token) {
        return <Redirect to="/dashboard/default" />;
    }

    return children;
};
