import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useTable } from 'react-table';
import { Card, CircularProgress, Typography, Table, TableBody, TableCell, TableHead, TableRow, TableContainer } from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';

// Custom styles
const useStyles = makeStyles((theme) => ({
    card: {
        padding: theme.spacing(3),
        margin: theme.spacing(3)
    },
    title: {
        marginBottom: theme.spacing(2)
    },
    tableContainer: {
        marginTop: theme.spacing(2),
        maxHeight: 400,
        overflowY: 'auto'
    },
    loading: {
        display: 'flex',
        justifyContent: 'center',
        marginTop: theme.spacing(3)
    }
}));

const PlantsList = () => {
    const classes = useStyles();
    const history = useHistory();

    const [plants, setPlants] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch plants data from API
        const fetchPlants = async () => {
            try {
                const response = await fetch('http://localhost:5000/plants/user-plants', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}` // Pass JWT token for authentication
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    setPlants(data);
                } else {
                    console.error('Failed to fetch plants:', response.statusText);
                }
            } catch (error) {
                console.error('Error fetching plants:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchPlants();
    }, []);

    const columns = React.useMemo(
        () => [
            { Header: 'ID', accessor: '_id' },
            { Header: 'Name', accessor: 'name' },
            { Header: 'Type', accessor: 'type' },
            { Header: 'Location', accessor: 'location' },
            { Header: 'Treatment', accessor: 'treatment' }
        ],
        []
    );

    const data = React.useMemo(() => plants, [plants]);

    const tableInstance = useTable({ columns, data });

    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance;

    const handleRowClick = (row) => {
        history.push(`/PlantDetails/${row.original._id}`);
    };

    return (
        <Card className={classes.card}>
            <Typography variant="h5" className={classes.title}>
                Plants List
            </Typography>
            {loading ? (
                <div className={classes.loading}>
                    <CircularProgress />
                </div>
            ) : (
                <TableContainer className={classes.tableContainer}>
                    <Table {...getTableProps()} size="small">
                        <TableHead>
                            {headerGroups.map((headerGroup) => (
                                <TableRow {...headerGroup.getHeaderGroupProps()}>
                                    {headerGroup.headers.map((column) => (
                                        <TableCell {...column.getHeaderProps()}>{column.render('Header')}</TableCell>
                                    ))}
                                </TableRow>
                            ))}
                        </TableHead>
                        <TableBody {...getTableBodyProps()}>
                            {rows.map((row) => {
                                prepareRow(row);
                                return (
                                    <TableRow {...row.getRowProps()} onClick={() => handleRowClick(row)} style={{ cursor: 'pointer' }}>
                                        {row.cells.map((cell) => (
                                            <TableCell {...cell.getCellProps()}>{cell.render('Cell')}</TableCell>
                                        ))}
                                    </TableRow>
                                );
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}
        </Card>
    );
};

export default PlantsList;
