import { useCallback, useRef, useState } from 'react';
import { Tool } from './EditorConsts';

export default function EditorSelectionArea({ scale, tool, bboxes, setBboxes, translation }) {
  const containerRef = useRef(null);
  const [isSelecting, setIsSelecting] = useState(false);
  const [selection, setSelection] = useState({ x: 0, y: 0, width: 0, height: 0 });
  const [startPoint, setStartPoint] = useState({ x: 0, y: 0, layerX: 0, layerY: 0 });

  const handleMouseDown = useCallback((e) => {
    setIsSelecting(true);
    const { x, y, layerX, layerY } = e.nativeEvent;
    setStartPoint({ x, y, layerX, layerY });
    setSelection({ x: layerX, y: layerY, width: 0, height: 0 });
  }, [setIsSelecting, setStartPoint, setSelection]);

  const handleMouseMove = useCallback((e) => {
    if (isSelecting) {
      const { x, y } = e.nativeEvent;

      const endPoint = { 
        layerX: startPoint.layerX + x - startPoint.x,
        layerY: startPoint.layerY + y - startPoint.y
      };

      setSelection({ 
        x: Math.min(endPoint.layerX, startPoint.layerX),
        y: Math.min(endPoint.layerY, startPoint.layerY),
        width: Math.floor(Math.abs(endPoint.layerX - startPoint.layerX) / scale),
        height: Math.floor(Math.abs(endPoint.layerY - startPoint.layerY) / scale)
      });
    }
  }, [isSelecting, startPoint, setSelection]);

  const handleMouseUp = useCallback(() => {
    setIsSelecting(false);
    if(selection.width > 1 && selection.height > 1) {
      setBboxes(prev => [...prev.map(bbox => ({ ...bbox, active: false })), { ...selection, active: true }]);
    } else {
      setBboxes(prev => prev.map(bbox => ({ ...bbox, active: false })));
    }
  }, [setIsSelecting, selection, setBboxes]);

  const handleBboxMouseDown = useCallback((e, i) => {
    e.stopPropagation();
    setBboxes(prev => prev.map((bbox, j) => i === j ? { ...bbox, active: true } : { ...bbox, active: false } ))
  }, [setBboxes]);

  const handleBboxMouseUp = useCallback(e => {
    if (!isSelecting) e.stopPropagation();
  }, [isSelecting]);

  return (
    <div
      ref={containerRef}
      style={{
        position: 'relative',
        width: '500px',
        height: '500px',
        border: '1px solid #000',
        cursor: tool === Tool.PAN ? 'inherit' : 'crosshair',
        scale: scale,
        left: '50%',
        top: '50%',
        transformOrigin: '0 0 0px',
        transform: `translate(calc(-50% + ${translation.x}px), calc(-50% + ${translation.y}px))`
      }}
      onMouseDown={tool === Tool.SELECT ? handleMouseDown : () => {}}
      onMouseMove={tool === Tool.SELECT ? handleMouseMove : () => {}}
      onMouseUp={tool === Tool.SELECT ? handleMouseUp : () => {}}
    >
      { isSelecting ? (
        <div
          style={{
            position: 'absolute',
            top: selection.y,
            left: selection.x,
            width: selection.width,
            height: selection.height,
            border: '1px dashed #000',
            backgroundColor: 'rgba(0, 0, 0, 0.2)',
          }}
        />
      ) : null }
      { bboxes.length > 0 ?
          bboxes.map((bbox, i) => <div
            key={`bbox-${i}`}
            style={{
              position: 'absolute',
              top: bbox.y,
              left: bbox.x,
              width: bbox.width,
              height: bbox.height,
              border: bbox.active ? '1px solid #0f0' : '1px solid #f00',
              // backgroundColor: bbox.active ? 'rgba(0, 255, 0, 0.2)' : 'rgba(255, 0, 0, 0.2)',
              cursor: tool === Tool.PAN ? 'inherit' : 'pointer'
            }}
            className={
              bbox.active
                ? 'bg-green-300/20'
                : 'bg-red-300/20'
            }
            onMouseDown={tool === Tool.SELECT ? (e) => handleBboxMouseDown(e, i) : () => {}}
            onMouseUp={tool === Tool.SELECT ? handleBboxMouseUp : () => {}}
          />)
      : null }
    </div>
  );
}
