// assets
import { IconDashboard, IconDeviceAnalytics } from '@tabler/icons';

// constant
const icons = {
    IconDashboard: IconDashboard,
    IconDeviceAnalytics
};

//-----------------------|| DASHBOARD MENU ITEMS ||-----------------------//

export const dashboard = {
    id: 'dashboard',
    title: 'Dashboard',
    type: 'group',
    children: [
        {
            id: 'default',
            title: 'Dashboard',
            type: 'item',
            url: '/dashboard/default',
            icon: icons['IconDashboard'],
            breadcrumbs: false
        },
        {
            id: 'AnalysePlane',
            title: 'AnalysePlane',
            type: 'item',
            url: '/AnalysePlane',
            icon: icons['IconDashboard'],
            breadcrumbs: false
        },
        {
            id: 'Plants',
            title: 'Plants',
            type: 'item',
            url: '/Plants',
            icon: icons['IconDashboard'],
            breadcrumbs: false
        }
    ]
};
