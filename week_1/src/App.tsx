import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { theme } from './theme';
import Dashboard from './pages/Dashboard';
import StudyActivities from './pages/StudyActivities';
import Words from './pages/Words';
import Groups from './pages/Groups';
import Layout from './components/Layout';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Router>
                <Layout>
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/study" element={<StudyActivities />} />
                        <Route path="/words" element={<Words />} />
                        <Route path="/groups" element={<Groups />} />
                    </Routes>
                </Layout>
            </Router>
        </ThemeProvider>
    );
}

export default App; 