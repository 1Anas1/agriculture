import React, { useEffect, useState } from 'react';

// material-ui
import { Grid } from '@material-ui/core';
// project imports

import { gridSpacing } from './../../store/constant';
import PlantsList from './PlantsList'
//-----------------------|| DEFAULT DASHBOARD ||-----------------------//

const Plants = () => {
    const [isLoading, setLoading] = useState(true);
    useEffect(() => {
        setLoading(false);
    }, []);

    return (
        <Grid container spacing={gridSpacing}>
            <Grid item xs={12}>
                <PlantsList />
            </Grid>
        </Grid>
    );
};

export default Plants;
