import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Chip,
  Divider
} from '@mui/material';
import axios from 'axios';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index }) => {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

const VehicleDetailPage: React.FC = () => {
  const { vehicleId } = useParams<{ vehicleId: string }>();
  const [vehicle, setVehicle] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    const fetchVehicle = async () => {
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_API_URL}/vehicles/${vehicleId}`
        );
        setVehicle(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch vehicle');
      } finally {
        setLoading(false);
      }
    };

    fetchVehicle();
  }, [vehicleId]);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!vehicle) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="warning">Vehicle not found</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          {vehicle.year} {vehicle.make} {vehicle.model}
        </Typography>
        {vehicle.trim && (
          <Typography variant="h6" color="text.secondary" gutterBottom>
            {vehicle.trim}
          </Typography>
        )}
        <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {vehicle.body_style && <Chip label={vehicle.body_style} />}
          {vehicle.drive_type && <Chip label={vehicle.drive_type} color="primary" />}
          {vehicle.transmission_type && <Chip label={vehicle.transmission_type} />}
          {vehicle.engine_config && <Chip label={vehicle.engine_config} color="secondary" />}
        </Box>
      </Paper>

      {/* Tabs */}
      <Paper elevation={3}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Specifications" />
          <Tab label="Engines" />
          <Tab label="Transmissions" />
          <Tab label="Repair Procedures" />
          <Tab label="Diagnostic Codes" />
          <Tab label="Maintenance" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Basic Information
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box sx={{ mb: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Model Year
                </Typography>
                <Typography variant="body1">{vehicle.year}</Typography>
              </Box>
              <Box sx={{ mb: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Manufacturer
                </Typography>
                <Typography variant="body1">{vehicle.make}</Typography>
              </Box>
              <Box sx={{ mb: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Model
                </Typography>
                <Typography variant="body1">{vehicle.model}</Typography>
              </Box>
              {vehicle.platform_code && (
                <Box sx={{ mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Platform Code
                  </Typography>
                  <Typography variant="body1">{vehicle.platform_code}</Typography>
                </Box>
              )}
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Production Information
              </Typography>
              <Divider sx={{ mb: 2 }} />
              {vehicle.production_start && (
                <Box sx={{ mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Production Start
                  </Typography>
                  <Typography variant="body1">
                    {new Date(vehicle.production_start).toLocaleDateString()}
                  </Typography>
                </Box>
              )}
              {vehicle.production_end && (
                <Box sx={{ mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Production End
                  </Typography>
                  <Typography variant="body1">
                    {new Date(vehicle.production_end).toLocaleDateString()}
                  </Typography>
                </Box>
              )}
              {vehicle.market_region && (
                <Box sx={{ mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Market Region
                  </Typography>
                  <Typography variant="body1">{vehicle.market_region}</Typography>
                </Box>
              )}
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          {vehicle.engines && vehicle.engines.length > 0 ? (
            vehicle.engines.map((engine: any, index: number) => (
              <Paper key={index} elevation={1} sx={{ p: 2, mb: 2 }}>
                <Typography variant="h6" gutterBottom>
                  {engine.engine_code}
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6} sm={4}>
                    <Typography variant="body2" color="text.secondary">
                      Displacement
                    </Typography>
                    <Typography>
                      {engine.displacement_liters}L ({engine.displacement_cc}cc)
                    </Typography>
                  </Grid>
                  <Grid item xs={6} sm={4}>
                    <Typography variant="body2" color="text.secondary">
                      Configuration
                    </Typography>
                    <Typography>{engine.configuration}</Typography>
                  </Grid>
                  <Grid item xs={6} sm={4}>
                    <Typography variant="body2" color="text.secondary">
                      Power
                    </Typography>
                    <Typography>
                      {engine.horsepower} HP @ {engine.horsepower_rpm} RPM
                    </Typography>
                  </Grid>
                  <Grid item xs={6} sm={4}>
                    <Typography variant="body2" color="text.secondary">
                      Torque
                    </Typography>
                    <Typography>
                      {engine.torque_lb_ft} lb-ft @ {engine.torque_rpm} RPM
                    </Typography>
                  </Grid>
                  <Grid item xs={6} sm={4}>
                    <Typography variant="body2" color="text.secondary">
                      Aspiration
                    </Typography>
                    <Typography>{engine.aspiration}</Typography>
                  </Grid>
                  <Grid item xs={6} sm={4}>
                    <Typography variant="body2" color="text.secondary">
                      Fuel System
                    </Typography>
                    <Typography>{engine.fuel_system}</Typography>
                  </Grid>
                </Grid>
              </Paper>
            ))
          ) : (
            <Alert severity="info">No engine data available</Alert>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          {vehicle.transmissions && vehicle.transmissions.length > 0 ? (
            vehicle.transmissions.map((trans: any, index: number) => (
              <Paper key={index} elevation={1} sx={{ p: 2, mb: 2 }}>
                <Typography variant="h6" gutterBottom>
                  {trans.transmission_code || `Transmission ${index + 1}`}
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Type
                    </Typography>
                    <Typography>{trans.type}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Speeds
                    </Typography>
                    <Typography>{trans.speeds}-Speed</Typography>
                  </Grid>
                  {trans.fluid_type && (
                    <Grid item xs={12}>
                      <Typography variant="body2" color="text.secondary">
                        Fluid Type
                      </Typography>
                      <Typography>{trans.fluid_type}</Typography>
                    </Grid>
                  )}
                </Grid>
              </Paper>
            ))
          ) : (
            <Alert severity="info">No transmission data available</Alert>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          <Alert severity="info">
            Repair procedures will be displayed here
          </Alert>
        </TabPanel>

        <TabPanel value={tabValue} index={4}>
          <Alert severity="info">
            Diagnostic codes will be displayed here
          </Alert>
        </TabPanel>

        <TabPanel value={tabValue} index={5}>
          <Alert severity="info">
            Maintenance schedule will be displayed here
          </Alert>
        </TabPanel>
      </Paper>
    </Container>
  );
};

export default VehicleDetailPage;
