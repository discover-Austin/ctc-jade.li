import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Chip,
  Box
} from '@mui/material';
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar';
import { useNavigate } from 'react-router-dom';

interface VehicleCardProps {
  vehicle: {
    vehicle_id: string;
    year: number;
    make: string;
    model: string;
    trim?: string;
    body_style?: string;
    drive_type?: string;
    engine_config?: string;
  };
}

const VehicleCard: React.FC<VehicleCardProps> = ({ vehicle }) => {
  const navigate = useNavigate();

  const handleViewDetails = () => {
    navigate(`/vehicles/${vehicle.vehicle_id}`);
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <DirectionsCarIcon color="primary" sx={{ mr: 1 }} />
          <Typography variant="h6" component="h2">
            {vehicle.year} {vehicle.make} {vehicle.model}
          </Typography>
        </Box>

        {vehicle.trim && (
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Trim: {vehicle.trim}
          </Typography>
        )}

        <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {vehicle.body_style && (
            <Chip label={vehicle.body_style} size="small" variant="outlined" />
          )}
          {vehicle.drive_type && (
            <Chip label={vehicle.drive_type} size="small" variant="outlined" color="primary" />
          )}
          {vehicle.engine_config && (
            <Chip label={vehicle.engine_config} size="small" variant="outlined" color="secondary" />
          )}
        </Box>
      </CardContent>

      <CardActions>
        <Button size="small" onClick={handleViewDetails}>
          View Details
        </Button>
        <Button size="small" color="secondary">
          Repair Procedures
        </Button>
      </CardActions>
    </Card>
  );
};

export default VehicleCard;
