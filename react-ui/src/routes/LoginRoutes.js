import React, { lazy } from 'react';
import { Route, Switch, useLocation } from 'react-router-dom';
import Loadable from '../ui-component/Loadable';
import { GuestGuard } from '../utils/route-guard/GuestGuard';
// project imports
import MinimalLayout from './../layout/MinimalLayout';

// login option 3 routing
const AuthLogin3 = Loadable(lazy(() => import('../views/pages/authentication/authentication3/Login3')));
const AuthRegister3 = Loadable(lazy(() => import('../views/pages/authentication/authentication3/Register3')));

const AuthenticationRoutes = () => {
    const location = useLocation();

    return (
        <Route path={['/pages/login/login3', '/pages/register/register3']}>
            <MinimalLayout>
                <Switch location={location} key={location.pathname}>
                    <GuestGuard>
                        <Route path="/pages/login/login3" component={AuthLogin3} />
                        <Route path="/pages/register/register3" component={AuthRegister3} />
                    </GuestGuard>
                </Switch>
            </MinimalLayout>
        </Route>
    );
};

export default AuthenticationRoutes;
