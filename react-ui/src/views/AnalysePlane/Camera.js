import React, { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import axios from './../../api/config';

// material-ui
import { Grid, Button, Typography, Card, CardMedia, CircularProgress } from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';

// Custom styles
const useStyles = makeStyles((theme) => ({
    media: {
        borderRadius: theme.shape.borderRadius,
        maxWidth: '100%',
        maxHeight: '300px',
        border: `2px solid ${theme.palette.primary.main}`
    },
    buttonContainer: {
        marginTop: theme.spacing(2)
    },
    message: {
        marginTop: theme.spacing(2),
        textAlign: 'center',
        fontWeight: 'bold',
        color: theme.palette.primary.main
    }
}));

const Camera = ({ isLoading }) => {
    const classes = useStyles();

    const [photo, setPhoto] = useState(null);
    const [isSending, setIsSending] = useState(false);
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

    // Stop the camera
    const stopCamera = () => {
        if (videoRef.current?.srcObject) {
            const tracks = videoRef.current.srcObject.getTracks();
            tracks.forEach((track) => track.stop());
        }
    };

    // Automatically start the camera when the component mounts
    useEffect(() => {
        startCamera();
        return () => stopCamera(); // Cleanup on unmount
    }, []);

    // Take a photo
    const takePhoto = () => {
        if (videoRef.current && canvasRef.current) {
            const context = canvasRef.current.getContext('2d');
            canvasRef.current.width = 300; // Resize width
            canvasRef.current.height = 300; // Resize height
            context.drawImage(videoRef.current, 0, 0, 300, 300);

            // Get photo as a data URL
            const imageDataUrl = canvasRef.current.toDataURL('image/jpeg', 0.7); // Reduce quality to 70%
            setPhoto(imageDataUrl);

            // Stop the camera after capturing the photo
            stopCamera();
        }
    };

    // Send photo as base64
    const sendPhoto = async () => {
        if (!photo) return;
        setIsSending(true);
        try {
            // Prepare data
            const payload = {
                image_base64: photo
            };

            // Send data using axios
            const response = await axios.post('/plants/detect-disease', payload, {
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.status === 200) {
                alert('Photo sent successfully!');
            } else {
                alert('Failed to send photo.');
            }
        } catch (error) {
            console.error('Error sending photo:', error);
            alert('Error occurred while sending the photo.');
        } finally {
            setIsSending(false);
        }
    };

    // Reset to retake the photo
    const retakePhoto = () => {
        setPhoto(null);
        startCamera();
    };

    return (
        <React.Fragment>
            {isLoading ? (
                <CircularProgress />
            ) : (
                <Card>
                    <Grid container spacing={3} justifyContent="center" alignItems="center">
                        <Grid item xs={12}>
                            <Typography variant="h5" align="center">
                                Capture and Send Photo
                            </Typography>
                        </Grid>
                        <Grid item xs={12}>
                            {photo ? (
                                <CardMedia component="img" image={photo} alt="Captured" className={classes.media} />
                            ) : (
                                <video ref={videoRef} autoPlay className={classes.media} />
                            )}
                            <canvas ref={canvasRef} style={{ display: 'none' }} />
                        </Grid>
                        <Grid item xs={12} container justifyContent="center" spacing={2} className={classes.buttonContainer}>
                            {!photo && (
                                <Grid item>
                                    <Button
                                        variant="contained"
                                        color="secondary"
                                        onClick={takePhoto}
                                        disabled={videoRef.current?.srcObject}
                                    >
                                        Take Photo
                                    </Button>
                                </Grid>
                            )}
                            {photo && (
                                <>
                                    <Grid item>
                                        <Button variant="contained" color="primary" onClick={sendPhoto} disabled={isSending}>
                                            {isSending ? 'Sending...' : 'Send Photo'}
                                        </Button>
                                    </Grid>
                                    <Grid item>
                                        <Button variant="contained" color="secondary" onClick={retakePhoto}>
                                            Retake Photo
                                        </Button>
                                    </Grid>
                                </>
                            )}
                        </Grid>
                    </Grid>
                </Card>
            )}
        </React.Fragment>
    );
};

Camera.propTypes = {
    isLoading: PropTypes.bool
};

export default Camera;
