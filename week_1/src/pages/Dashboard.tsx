import { Box, Grid, Paper, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import axios from 'axios';

interface DashboardStats {
    totalWords: number;
    learningAccuracy: number;
    studyStreak: number;
    lastSession: {
        date: string;
        activity: string;
        score: number;
    };
}

const Dashboard = () => {
    const [stats, setStats] = useState<DashboardStats | null>(null);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/dashboard/stats');
                setStats(response.data);
            } catch (error) {
                console.error('Failed to fetch dashboard stats:', error);
            }
        };

        fetchStats();
    }, []);

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Dashboard
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} md={6} lg={3}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Total Words</Typography>
                        <Typography variant="h4">{stats?.totalWords || 0}</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={6} lg={3}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Learning Accuracy</Typography>
                        <Typography variant="h4">{stats?.learningAccuracy || 0}%</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={6} lg={3}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Study Streak</Typography>
                        <Typography variant="h4">{stats?.studyStreak || 0} days</Typography>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default Dashboard; 