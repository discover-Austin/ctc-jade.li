import React, { useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Autocomplete,
  Chip,
  CircularProgress,
  Alert,
  Box,
} from '@mui/material';
import { Search, DirectionsCar } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

interface Vehicle {
  vehicle_id: string;
  year: number;
  make: string;
  model: string;
  trim?: string;
  engine_config?: string;
  transmission_type?: string;
  body_style?: string;
  drive_type?: string;
}

const POPULAR_MAKES = [
  'Ford', 'Chevrolet', 'Toyota', 'Honda', 'BMW', 'Mercedes-Benz',
  'Nissan', 'Volkswagen', 'Audi', 'Lexus', 'Hyundai', 'Kia',
  'Mazda', 'Subaru', 'Jeep', 'Ram', 'GMC', 'Dodge'
];

const VehicleSearchPage: React.FC = () => {
  const navigate = useNavigate();
  const [year, setYear] = useState<number | null>(null);
  const [make, setMake] = useState<string>('');
  const [model, setModel] = useState<string>('');
  const [vin, setVin] = useState<string>('');
  const [searchTriggered, setSearchTriggered] = useState(false);

  // Build search query
  const buildSearchQuery = () => {
    const params = new URLSearchParams();
    if (year) params.append('year', year.toString());
    if (make) params.append('make', make);
    if (model) params.append('model', model);
    if (vin) params.append('vin', vin);
    return params.toString();
  };

  // Search vehicles query
  const { data: vehicles, isLoading, error } = useQuery({
    queryKey: ['vehicles', year, make, model, vin],
    queryFn: async () => {
      if (!searchTriggered) return [];
      const query = buildSearchQuery();
      if (!query) return [];

      const response = await axios.get(`${API_BASE_URL}/vehicles/search?${query}`);
      return response.data as Vehicle[];
    },
    enabled: searchTriggered,
  });

  const handleSearch = () => {
    if (!year && !make && !model && !vin) {
      return;
    }
    setSearchTriggered(true);
  };

  const handleVehicleClick = (vehicleId: string) => {
    navigate(`/vehicle/${vehicleId}`);
  };

  const years = Array.from({ length: new Date().getFullYear() - 2013 }, (_, i) => 2014 + i).reverse();

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" gutterBottom align="center" sx={{ fontWeight: 'bold' }}>
          Vehicle Repair Database
        </Typography>
        <Typography variant="h6" align="center" color="text.secondary" gutterBottom>
          Search for repair procedures, diagnostic codes, and technical information
        </Typography>
      </Box>

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Search Vehicles
          </Typography>

          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={3}>
              <Autocomplete
                options={years}
                value={year}
                onChange={(_, value) => setYear(value)}
                renderInput={(params) => (
                  <TextField {...params} label="Year" placeholder="2014-2024" />
                )}
              />
            </Grid>

            <Grid item xs={12} md={3}>
              <Autocomplete
                freeSolo
                options={POPULAR_MAKES}
                value={make}
                onChange={(_, value) => setMake(value || '')}
                onInputChange={(_, value) => setMake(value)}
                renderInput={(params) => <TextField {...params} label="Make" />}
              />
            </Grid>

            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Model"
                value={model}
                onChange={(e) => setModel(e.target.value)}
                placeholder="e.g., Camry, F-150"
              />
            </Grid>

            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="VIN (Optional)"
                value={vin}
                onChange={(e) => setVin(e.target.value.toUpperCase())}
                inputProps={{ maxLength: 17 }}
                placeholder="17 characters"
              />
            </Grid>

            <Grid item xs={12}>
              <Button
                fullWidth
                variant="contained"
                size="large"
                startIcon={isLoading ? <CircularProgress size={20} /> : <Search />}
                onClick={handleSearch}
                disabled={isLoading || (!year && !make && !model && !vin)}
              >
                {isLoading ? 'Searching...' : 'Search Vehicles'}
              </Button>
            </Grid>
          </Grid>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              Error searching vehicles. Please try again.
            </Alert>
          )}
        </CardContent>
      </Card>

      {vehicles && vehicles.length > 0 && (
        <Box>
          <Typography variant="h5" gutterBottom>
            Search Results ({vehicles.length})
          </Typography>

          <Grid container spacing={2}>
            {vehicles.map((vehicle) => (
              <Grid item xs={12} md={6} lg={4} key={vehicle.vehicle_id}>
                <Card
                  sx={{
                    cursor: 'pointer',
                    transition: 'all 0.3s',
                    '&:hover': {
                      boxShadow: 6,
                      transform: 'translateY(-4px)',
                    },
                  }}
                  onClick={() => handleVehicleClick(vehicle.vehicle_id)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <DirectionsCar sx={{ mr: 1, color: 'primary.main' }} />
                      <Typography variant="h6" component="div">
                        {vehicle.year} {vehicle.make} {vehicle.model}
                      </Typography>
                    </Box>

                    {vehicle.trim && (
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        Trim: {vehicle.trim}
                      </Typography>
                    )}

                    <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {vehicle.engine_config && (
                        <Chip
                          label={vehicle.engine_config}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                      )}
                      {vehicle.transmission_type && (
                        <Chip
                          label={vehicle.transmission_type}
                          size="small"
                          color="secondary"
                          variant="outlined"
                        />
                      )}
                      {vehicle.drive_type && (
                        <Chip
                          label={vehicle.drive_type}
                          size="small"
                          variant="outlined"
                        />
                      )}
                      {vehicle.body_style && (
                        <Chip
                          label={vehicle.body_style}
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {searchTriggered && vehicles && vehicles.length === 0 && !isLoading && (
        <Alert severity="info">
          No vehicles found matching your search criteria. Try adjusting your filters.
        </Alert>
      )}

      {!searchTriggered && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary">
            Enter search criteria above to find vehicles
          </Typography>
        </Box>
      )}
    </Container>
  );
};

export default VehicleSearchPage;
