import React, { useEffect, useState } from 'react';

// material-ui
import { Grid } from '@material-ui/core';
import Camera from './Camera';
// project imports

import { gridSpacing } from './../../store/constant';

//-----------------------|| DEFAULT DASHBOARD ||-----------------------//

const AnalysePlane = () => {
    const [isLoading, setLoading] = useState(true);
    useEffect(() => {
        setLoading(false);
    }, []);

    return (
        <Grid container spacing={gridSpacing}>
            <Grid item xs={12}>
                <Camera isLoading={isLoading} />
            </Grid>
        </Grid>
    );
};

export default AnalysePlane;
