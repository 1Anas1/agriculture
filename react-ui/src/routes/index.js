import React from 'react';
import { Redirect, Switch } from 'react-router-dom';

// routes
import MainRoutes from './MainRoutes';
import LoginRoutes from './LoginRoutes';
import AuthenticationRoutes from './AuthenticationRoutes';

// project imports
import config from './../config';
import { AuthProvider } from './../provider/AuthProvider';

//-----------------------|| ROUTING RENDER ||-----------------------//

const Routes = () => {
    return (
        <AuthProvider>
            <Switch>
                <Redirect exact from="/" to={config.defaultPath} />
                <React.Fragment>
                    {/* Routes for authentication pages */}
                    <AuthenticationRoutes />

                    {/* Route for login */}
                    <LoginRoutes />

                    {/* Routes for main layouts */}
                    <MainRoutes />
                </React.Fragment>
            </Switch>
        </AuthProvider>
    );
};

export default Routes;
