import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Typography, CircularProgress } from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';
import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';

// Custom styles
const useStyles = makeStyles((theme) => ({
    card: {
        padding: theme.spacing(3),
        margin: theme.spacing(3)
    },
    map: {
        height: '300px',
        width: '100%',
        marginTop: theme.spacing(2)
    },
    details: {
        marginBottom: theme.spacing(2)
    }
}));

const PlantDetails = ({ google }) => {
    const classes = useStyles();
    const { id } = useParams();

    const [plant, setPlant] = useState(null);
    const [loading, setLoading] = useState(true);
    const [userLocation, setUserLocation] = useState(null);

    useEffect(() => {
        // Fetch plant details
        const fetchPlant = async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/plants/${id}`);
                const data = await response.json();
                setPlant(data);
            } catch (error) {
                console.error('Error fetching plant details:', error);
            } finally {
                setLoading(false);
            }
        };

        // Get user location
        navigator.geolocation.getCurrentPosition(
            (position) => {
                setUserLocation({
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                });
            },
            (error) => console.error('Error getting user location:', error)
        );

        fetchPlant();
    }, [id]);

    if (loading) {
        return <CircularProgress />;
    }

    return (
        <Card className={classes.card}>
            <Typography variant="h5" className={classes.details}>
                Plant Details
            </Typography>
            {plant ? (
                <>
                    <Typography variant="body1">Name: {plant.name}</Typography>
                    <Typography variant="body1">Type: {plant.type}</Typography>
                    <Typography variant="body1">Treatment: {plant.treatment}</Typography>
                    <Typography variant="body1">Next Check Date: {plant.nextCheckDate}</Typography>

                    <div className={classes.map}>
                        <Map
                            google={google}
                            zoom={13}
                            initialCenter={{
                                lat: plant.location.lat,
                                lng: plant.location.lng
                            }}
                            style={{ height: '100%', width: '100%' }}
                        >
                            <Marker
                                position={{
                                    lat: plant.location.lat,
                                    lng: plant.location.lng
                                }}
                                title={plant.name}
                            />
                            {userLocation && (
                                <Marker
                                    position={userLocation}
                                    title="Your Location"
                                    icon={{
                                        url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                                    }}
                                />
                            )}
                        </Map>
                    </div>
                </>
            ) : (
                <Typography variant="body1">No details available for this plant.</Typography>
            )}
        </Card>
    );
};

export default GoogleApiWrapper({
    apiKey: 'YOUR_GOOGLE_MAPS_API_KEY' // Replace with your Google Maps API Key
})(PlantDetails);
