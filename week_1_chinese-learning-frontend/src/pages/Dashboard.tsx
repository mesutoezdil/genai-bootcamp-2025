import React from 'react';
import { Box, Card, CardContent, Typography, Grid } from '@mui/material';
import { api } from '../../services/api';

export default function Dashboard() {
  const [stats, setStats] = React.useState({
    totalWords: 0,
    wordsLearned: 0,
    streak: 0,
  });

  React.useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/dashboard/stats');
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
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Words
              </Typography>
              <Typography variant="h5">
                {stats.totalWords}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Words Learned
              </Typography>
              <Typography variant="h5">
                {stats.wordsLearned}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Learning Streak
              </Typography>
              <Typography variant="h5">
                {stats.streak} days
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
