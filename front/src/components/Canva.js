import React, { useState } from 'react';
import { Box } from '@mui/material';
import { Stage, Layer, Rect } from 'react-konva';
import useImage from 'use-image';

export default function Canva({ projectors, selectedId, setSelectedId, stageRef, dragItem, saveAction }) {
    const [roro] = useImage('/roro.svg');
    const [stageConfig, setStageConfig] = useState({ scale: 1, x: 0, y: 0 });

    const handleWheel = (e) => {
        e.evt.preventDefault();
        const scaleBy = 1.1;
        const stageObj = stageRef.current;
        const oldScale = stageObj.scaleX();
        const pointer = stageObj.getPointerPosition();

        const mousePointTo = {
          x: (pointer.x - stageObj.x()) / oldScale,
          y: (pointer.y - stageObj.y()) / oldScale,
        };

        const newScale = e.evt.deltaY < 0 ? oldScale * scaleBy : oldScale / scaleBy;
        setStageConfig({
          scale: newScale,
          x: pointer.x - mousePointTo.x * newScale,
          y: pointer.y - mousePointTo.y * newScale,
        });
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const stageObj = stageRef.current;
        stageObj.setPointersPositions(e);
        const pointer = stageObj.getPointerPosition();
        
        const x = (pointer.x - stageObj.x()) / stageObj.scaleX();
        const y = (pointer.y - stageObj.y()) / stageObj.scaleY();

        const newProjo = {
          id: `projo-${Date.now()}`,
          x, y,
          type: dragItem.current,
          patch: '1.001',
        };
        saveAction([...projectors, newProjo]);
        setSelectedId(newProjo.id);
    };

    return (
      <Box sx={{ flexGrow: 1, position: 'relative' }} onDragOver={(e) => e.preventDefault()} onDrop={handleDrop}>
        <Stage 
          width={window.innerWidth - 480} 
          height={window.innerHeight}
          ref={stageRef}
          scaleX={stageConfig.scale}
          scaleY={stageConfig.scale}
          x={stageConfig.x}
          y={stageConfig.y}
          onWheel={handleWheel}
          draggable
          onClick={(e) => e.target === e.target.getStage() && setSelectedId(null)}
        >
          <Layer>
            <Rect x={0} y={0} width={window.innerWidth} height={window.innerHeight} fillPatternImage={roro} listening={false} />
            {projectors.map((p) => (
              <Rect
                key={p.id}
                x={p.x} y={p.y}
                width={40} height={40}
                fill="#3f51b5"
                draggable
                stroke={selectedId === p.id ? '#ff9800' : 'white'}
                strokeWidth={2}
                cornerRadius={4}
                onClick={() => setSelectedId(p.id)}
                onDragEnd={(e) => {
                  const updated = projectors.map(pr => 
                    pr.id === p.id ? { ...pr, x: e.target.x(), y: e.target.y() } : pr
                  );
                  saveAction(updated);
                }}
              />
            ))}
          </Layer>
        </Stage>
      </Box>
    );
}