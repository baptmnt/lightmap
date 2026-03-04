import { Paper, Typography, Stack, Button } from '@mui/material';

export default function LeftSidebar({ dragItem }) {
    return (
      <Paper sx={{ width: 180, p: 2, borderRadius: 0, bgcolor: '#1e1e1e', color: 'inherit' }}>
        <Typography variant="button" display="block" sx={{ mb: 2, opacity: 0.7 }}>Projecteurs</Typography>
        <Stack spacing={1}>
          {['Spot', 'Wash', 'Beam'].map((type) => (
            <Button 
              key={type} 
              variant="outlined" 
              color="inherit"
              draggable 
              onDragStart={() => (dragItem.current = type)}
              sx={{ cursor: 'grab', borderColor: 'rgba(255,255,255,0.2)' }}
            >
              {type}
            </Button>
          ))}
        </Stack>
      </Paper>
    );
}