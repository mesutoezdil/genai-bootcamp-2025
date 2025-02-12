import React, { useEffect, useState } from 'react';

function App() {
    const [stats, setStats] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('/api/dashboard/quick-stats')
            .then(response => response.json())
            .then(data => setStats(data))
            .catch(err => setError(err.message));
    }, []);

    if (error) return <div>Error: {error}</div>;
    if (!stats) return <div>Loading...</div>;

    return (
        <div className="App">
            <h1>Chinese Learning Portal</h1>
            <div>
                <h2>Quick Stats</h2>
                <p>Success Rate: {stats.success_rate}%</p>
                <p>Total Study Sessions: {stats.total_study_sessions}</p>
                <p>Total Active Groups: {stats.total_active_groups}</p>
                <p>Study Streak: {stats.study_streak_days} days</p>
            </div>
        </div>
    );
}

export default App; 