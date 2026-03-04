import { Paper, Typography, TextField } from '@mui/material';

export default function RightSidebar({ projectors, setProjectors, selectedId, saveAction }) {
    // Find the currently selected projector object
    const selectedProjector = projectors.find(p => p.id === selectedId);

    return (
      <Paper sx={{ width: 300, p: 3, borderRadius: 0, bgcolor: '#1e1e1e', color: 'inherit' }}>
        <Typography variant="h6" gutterBottom>Propriétés</Typography>
        
        {selectedId && selectedProjector ? (
          <TextField 
            fullWidth 
            label="Adresse DMX (Patch)" 
            variant="filled"
            sx={{ mt: 3, input: { color: 'white' }, label: { color: 'gray' }, bgcolor: '#2b2b2b' }}
            value={selectedProjector.patch || ''}
            onChange={(e) => {
              // Update local state for real-time typing feel
              const updated = projectors.map(p => 
                p.id === selectedId ? { ...p, patch: e.target.value } : p
              );
              setProjectors(updated);
            }}
            // Only push to history when the user finished typing
            onBlur={() => saveAction(projectors)}
          />
        ) : (
          <Typography sx={{ mt: 2, color: 'gray', fontStyle: 'italic' }}>
            Sélectionnez un élément sur le plan
          </Typography>
        )}
      </Paper>
    );
}