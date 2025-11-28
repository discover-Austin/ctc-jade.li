import React, { useState } from 'react';
import {
  Box,
  TextField,
  MenuItem,
  Button,
  Grid,
  Paper
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

interface SearchFiltersProps {
  onSearch: (filters: SearchFilters) => void;
}

export interface SearchFilters {
  year?: number;
  make?: string;
  model?: string;
  engine?: string;
  vin?: string;
}

const SearchFilters: React.FC<SearchFiltersProps> = ({ onSearch }) => {
  const [filters, setFilters] = useState<SearchFilters>({});

  const handleFilterChange = (field: keyof SearchFilters, value: string | number) => {
    setFilters(prev => ({
      ...prev,
      [field]: value || undefined
    }));
  };

  const handleSearch = () => {
    onSearch(filters);
  };

  const handleClear = () => {
    setFilters({});
    onSearch({});
  };

  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: currentYear - 2013 }, (_, i) => 2014 + i).reverse();

  const popularMakes = [
    'Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan',
    'BMW', 'Mercedes-Benz', 'Volkswagen', 'Hyundai', 'Mazda',
    'Subaru', 'Kia', 'Jeep', 'Ram', 'GMC'
  ];

  return (
    <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6} md={2.4}>
          <TextField
            select
            fullWidth
            label="Year"
            value={filters.year || ''}
            onChange={(e) => handleFilterChange('year', parseInt(e.target.value))}
            size="small"
          >
            <MenuItem value="">All Years</MenuItem>
            {years.map(year => (
              <MenuItem key={year} value={year}>{year}</MenuItem>
            ))}
          </TextField>
        </Grid>

        <Grid item xs={12} sm={6} md={2.4}>
          <TextField
            select
            fullWidth
            label="Make"
            value={filters.make || ''}
            onChange={(e) => handleFilterChange('make', e.target.value)}
            size="small"
          >
            <MenuItem value="">All Makes</MenuItem>
            {popularMakes.map(make => (
              <MenuItem key={make} value={make}>{make}</MenuItem>
            ))}
          </TextField>
        </Grid>

        <Grid item xs={12} sm={6} md={2.4}>
          <TextField
            fullWidth
            label="Model"
            value={filters.model || ''}
            onChange={(e) => handleFilterChange('model', e.target.value)}
            size="small"
            placeholder="e.g., Camry"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={2.4}>
          <TextField
            fullWidth
            label="Engine"
            value={filters.engine || ''}
            onChange={(e) => handleFilterChange('engine', e.target.value)}
            size="small"
            placeholder="e.g., 2.5L"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={2.4}>
          <TextField
            fullWidth
            label="VIN"
            value={filters.vin || ''}
            onChange={(e) => handleFilterChange('vin', e.target.value)}
            size="small"
            placeholder="17-character VIN"
            inputProps={{ maxLength: 17 }}
          />
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              startIcon={<SearchIcon />}
              onClick={handleSearch}
            >
              Search
            </Button>
            <Button
              variant="outlined"
              onClick={handleClear}
            >
              Clear Filters
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default SearchFilters;
