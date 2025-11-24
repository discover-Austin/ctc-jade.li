import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import HomePage from './pages/HomePage';
import VehicleSearchPage from './pages/VehicleSearchPage';
import VehicleDetailPage from './pages/VehicleDetailPage';
import RepairProcedurePage from './pages/RepairProcedurePage';
import DiagnosticPage from './pages/DiagnosticPage';
import MaintenancePage from './pages/MaintenancePage';
import Header from './components/Header';
import Footer from './components/Footer';

// Create Material-UI theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#fafafa',
    },
  },
  typography: {
    fontFamily: [
      'Roboto',
      'Helvetica',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Header />
            <main style={{ flex: 1, padding: '2rem 0' }}>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/search" element={<VehicleSearchPage />} />
                <Route path="/vehicle/:vehicleId" element={<VehicleDetailPage />} />
                <Route path="/repair/:procedureId" element={<RepairProcedurePage />} />
                <Route path="/diagnostic/:vehicleId" element={<DiagnosticPage />} />
                <Route path="/maintenance/:vehicleId" element={<MaintenancePage />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App;
