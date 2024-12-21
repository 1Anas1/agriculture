import React, { useState, useRef } from 'react';
import PropTypes from 'prop-types';

// material-ui
import { Grid, Button, Typography } from '@material-ui/core';

// project imports
import MainCard from './../../ui-component/cards/MainCard';
import { gridSpacing } from './../../store/constant';

//-----------------------|| CAMERA COMPONENT - TAKE PHOTO ||-----------------------//

const Camera = ({ isLoading }) => {
    const [photo, setPhoto] = useState(null);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    // Start the camera
    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
        } catch (error) {
            console.error('Error accessing camera:', error);
        }
    };

    // Take a photo
    const takePhoto = () => {
        if (videoRef.current && canvasRef.current) {
            const context = canvasRef.current.getContext('2d');
            canvasRef.current.width = videoRef.current.videoWidth;
            canvasRef.current.height = videoRef.current.videoHeight;
            context.drawImage(videoRef.current, 0, 0, videoRef.current.videoWidth, videoRef.current.videoHeight);

            // Get photo as a data URL
            const imageDataUrl = canvasRef.current.toDataURL('image/png');
            setPhoto(imageDataUrl);
        }
    };

    return (
        <React.Fragment>
            {isLoading ? (
                <Typography variant="subtitle2">Loading...</Typography>
            ) : (
                <MainCard>
                    <Grid container spacing={gridSpacing}>
                        <Grid item xs={12}>
                            <Typography variant="h5" align="center">
                                Camera Capture
                            </Typography>
                        </Grid>
                        <Grid item xs={12}>
                            {/* Video Stream */}
                            <video ref={videoRef} autoPlay style={{ width: '100%', maxHeight: '400px' }} />
                        </Grid>
                        <Grid item xs={12}>
                            {/* Canvas for Capturing Photo */}
                            <canvas ref={canvasRef} style={{ display: 'none' }} />
                        </Grid>
                        <Grid item xs={12} container justifyContent="center" spacing={2}>
                            <Grid item>
                                <Button variant="contained" color="primary" onClick={startCamera}>
                                    Start Camera
                                </Button>
                            </Grid>
                            <Grid item>
                                <Button variant="contained" color="secondary" onClick={takePhoto}>
                                    Take Photo
                                </Button>
                            </Grid>
                        </Grid>
                        {photo && (
                            <Grid item xs={12}>
                                <Typography variant="h6" align="center">
                                    Captured Photo:
                                </Typography>
                                <img src={photo} alt="Captured" style={{ width: '100%', maxHeight: '400px' }} />
                            </Grid>
                        )}
                    </Grid>
                </MainCard>
            )}
        </React.Fragment>
    );
};

Camera.propTypes = {
    isLoading: PropTypes.bool
};

export default Camera;
