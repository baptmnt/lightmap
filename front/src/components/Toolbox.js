import { Paper, IconButton, Box, Button } from '@mui/material';

export default function Toolbox({ undo, redo, mirror, historyStep, historyLength }) {
  // Logic to determine if buttons should be disabled
  const canUndo = historyStep > 0;
  const canRedo = historyStep < historyLength - 1;

  return (
    <Paper 
      elevation={6} 
      sx={{ 
        position: 'absolute', bottom: 30, left: '50%', transform: 'translateX(-50%)', 
        p: 1, display: 'flex', alignItems: 'center', gap: 1, bgcolor: '#333' 
      }}
    >
      <IconButton onClick={undo} disabled={!canUndo} title="Undo">
        <span style={{ filter: !canUndo ? 'grayscale(1)' : 'none' }}>↩️</span>
      </IconButton>
      
      <IconButton onClick={redo} disabled={!canRedo} title="Redo">
        <span style={{ filter: !canRedo ? 'grayscale(1)' : 'none' }}>↪️</span>
      </IconButton>

      <Box sx={{ width: 1, height: 24, bgcolor: 'rgba(255,255,255,0.1)', mx: 1 }} />
      
      <Button size="small" variant="contained" color="inherit" sx={{ color: '#000' }}>
        Grille
      </Button>
      
      <Button 
        size="small" 
        onClick={mirror} 
        variant='contained' 
        color='inherit' 
        sx={{ color: '#000' }}
      >
        Mirror Selected
      </Button>
    </Paper>
  );
}