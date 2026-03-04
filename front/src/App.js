import React, { useState, useRef } from 'react';
import { Box } from '@mui/material';
import LeftSidebar from './components/LeftSidebar';
import RightSidebar from './components/RightSidebar';
import Toolbox from './components/Toolbox';
import Canva from './components/Canva';

const App = () => {
  const [projectors, setProjectors] = useState([]);
  const [history, setHistory] = useState([[]]); 
  const [historyStep, setHistoryStep] = useState(0);
  const [selectedId, setSelectedId] = useState(null);
  
  const stageRef = useRef(null);
  const dragItem = useRef();

  const saveAction = (newItems) => {
    const newHistory = history.slice(0, historyStep + 1);
    setHistory([...newHistory, newItems]);
    setHistoryStep(newHistory.length);
    setProjectors(newItems);
  };

  const undo = () => {
    if (historyStep === 0) return;
    setHistoryStep(historyStep - 1);
    setProjectors(history[historyStep - 1]);
  };

  const redo = () => {
    if (historyStep === history.length - 1) return;
    setHistoryStep(historyStep + 1);
    setProjectors(history[historyStep + 1]);
  };

  const deleteSelected = () => {
  if (!selectedId) return;
  const updated = projectors.filter(p => p.id !== selectedId);
  saveAction(updated);
  setSelectedId(null);
};

 const mirror = () => {
  if (!selectedId) return;
  const selectedProjector = projectors.find((projo) => projo.id === selectedId);
  if (!selectedProjector) return;

  // 1. Calculate the width of the canvas area
  const canvasWidth = window.innerWidth - 480; 
  // 2. The vertical axis is at canvasWidth / 2
  const axis = canvasWidth / 2;

  const newProjo = {
    ...selectedProjector, // Copy type and other props
    id: `projo-${Date.now()}`,
    // 3. Mirror formula: NewX = 2 * Axis - OldX - ObjectWidth
    // We subtract 40 because your Rect width is 40
    x: (2 * axis) - selectedProjector.x - 40, 
    y: selectedProjector.y,
    patch: '1.001',
  };

  saveAction([...projectors, newProjo]);
  setSelectedId(newProjo.id);
};

  return (
    <Box sx={{ display: 'flex', height: '100vh', bgcolor: '#121212', color: '#fff', overflow: 'hidden' }}>
      <LeftSidebar dragItem={dragItem} />
      
      <Canva 
        projectors={projectors} 
        setProjectors={setProjectors}
        selectedId={selectedId}
        setSelectedId={setSelectedId}
        stageRef={stageRef}
        dragItem={dragItem}
        saveAction={saveAction}
      />

      <RightSidebar 
        projectors={projectors} 
        setProjectors={setProjectors} 
        selectedId={selectedId} 
        saveAction={saveAction}
      />

      <Toolbox 
        undo={undo} 
        redo={redo} 
        mirror={mirror} 
        historyStep={historyStep} 
        historyLength={history.length} 
      />
    </Box>
  );
};

export default App;