import { useCallback, useEffect, useRef, useState } from 'react';
import Image from 'next/image';

import './Editor.css';
import { getSample } from './EditorUtils';
import { Tool } from './EditorConsts';
import { useNotification } from '../../hooks/useNotification';
import { Spinner } from '@nextui-org/react';
import { NextColor } from '../../consts/NextColor';

export default function EditorSelectionArea({ scale, tool, bboxes, setBboxes, sampleId, translation, status, setStatus, detection, setTranslation, adminOverride }) {
  const containerRef = useRef(null);
  const notification = useNotification();
  const [isSelecting, setIsSelecting] = useState(false);
  const [image, setImage] = useState({ src: '', width: 0, height: 0 });
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
      if(adminOverride) notification.make(NextColor.WARNING, 'Override denied', 'You cannot override admin\'s examination.')
      else if(detection) setBboxes(prev => [...prev.map(bbox => ({ ...bbox, active: false })), { ...selection, active: true }]);
      else setBboxes([{ ...selection, active: true }]);
    } else {
      setBboxes(prev => prev.map(bbox => ({ ...bbox, active: false })));
    }
    
  }, [setIsSelecting, selection, setBboxes, adminOverride]);

  const handleBboxMouseDown = useCallback((e, i) => {
    e.stopPropagation();
    setBboxes(prev => prev.map((bbox, j) => i === j ? { ...bbox, active: true } : { ...bbox, active: false } ))
  }, [setBboxes]);

  const handleBboxMouseUp = useCallback(e => {
    if (!isSelecting) e.stopPropagation();
  }, [isSelecting]);

  useEffect(() => {
    getSample(setImage, setStatus, sampleId, notification);
  }, [sampleId]);

  useEffect(() => setTranslation({ x: 0, y: 0 }), [image.src])

  return (
    <>
      { status.error ? <div
        className='text-zinc-500 w-60'
        style={{
          position: 'relative',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)'
        }}
      >
        Could not load sample image!
      </div> : !status.ready && !image.src ? <div
        className='w-min'
        style={{
          position: 'relative',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)'
        }}
      >
        <Spinner size='lg' />
      </div> : <div
        ref={containerRef}
        style={{
          cursor: tool === Tool.PAN ? 'inherit' : 'crosshair',
          scale: scale,
          transform: `translate(calc(-50% + ${translation.x}px), calc(-50% + ${translation.y}px))`
        }}
        className='editor-selection-area'
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
                cursor: tool === Tool.PAN ? 'inherit' : 'pointer'
              }}
              className={
                bbox.active
                  ? `bg-${bbox?.label?.color || 'zinc'}-100/10 border-3 border-${bbox?.label?.color || 'zinc'}-500`
                  : `bg-${bbox?.label?.color || 'zinc'}-200/10 border-2 border-${bbox?.label?.color || 'zinc'}-400`
              }
              onMouseDown={tool === Tool.SELECT ? (e) => handleBboxMouseDown(e, i) : () => {}}
              onMouseUp={tool === Tool.SELECT ? handleBboxMouseUp : () => {}}
            />)
        : null }
        { image.src ? <Image src={image.src} width={image.width} height={image.height} alt={`Sample ID: ${sampleId}`} draggable={false} /> : null}
      </div>
      }
    </>
  );
}
