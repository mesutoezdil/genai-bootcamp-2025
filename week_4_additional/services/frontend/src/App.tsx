import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { theme } from './theme';
import { Layout } from './components/Layout';
import { PrivateRoute } from './components/PrivateRoute';
import { Dashboard } from './pages/Dashboard';
import { Study } from './pages/Study';
import { Words } from './pages/Words';
import { Login } from './pages/Login';
import { AuthProvider } from './contexts/AuthContext';
import { WordProvider } from './contexts/WordContext';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <WordProvider>
          <Router>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route element={<Layout />}>
                <Route
                  path="/dashboard"
                  element={
                    <PrivateRoute>
                      <Dashboard />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/study"
                  element={
                    <PrivateRoute>
                      <Study />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/words"
                  element={
                    <PrivateRoute>
                      <Words />
                    </PrivateRoute>
                  }
                />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
              </Route>
            </Routes>
          </Router>
        </WordProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
