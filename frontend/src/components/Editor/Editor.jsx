'use client'

import { useCallback, useState } from 'react';

import EditorSelectionArea from './EditorSelectionArea';
import EditorTools from './EditorTools';
import { Tool } from './EditorConsts';

export default function Editor() {

  const [scale, setScale] = useState(1);
  const [tool, setTool] = useState(Tool.SELECT);
  const [pan, setPan] = useState(false);
  const [startPoint, setStartPoint] = useState({ x: 0, y: 0 });
  const [translation, setTranslation] = useState({ x: 0, y: 0 });
  const [newTranslation, setNewTranslation] = useState({ x: 0, y: 0 });

  const handleMouseDown = useCallback((e) => {
    setPan(true);
    const { x, y } = e.nativeEvent;
    setStartPoint({ x, y });
  }, [setPan, setStartPoint]);

  const handleMouseMove = useCallback((e) => {
    if (pan) {
      const { x, y } = e.nativeEvent;
      setNewTranslation({
        x: x - startPoint.x,
        y: y - startPoint.y,
      });
    }
  }, [pan, startPoint, setNewTranslation]);

  const handleMouseUp = useCallback(() => {
    setPan(false);
    if (Math.abs(newTranslation.x) > 0 || Math.abs(newTranslation.y) > 0) {
      setNewTranslation({ x: 0, y: 0 });
      setTranslation(prev => ({
        x: prev.x + newTranslation.x,
        y: prev.y + newTranslation.y,
      }));
    }
  }, [setPan, newTranslation, setTranslation]);

  return (
    <div
      className='editor'
      onMouseDown={tool === Tool.PAN ? handleMouseDown : () => {}}
      onMouseMove={tool === Tool.PAN ? handleMouseMove : () => {}}
      onMouseUp={tool === Tool.PAN ? handleMouseUp : () => {}}
      style={{
        cursor: tool === Tool.PAN ? pan ? 'grabbing' : 'grab' : 'default',
        overflow: 'hidden'
      }}
    >
      <EditorTools
        scale={scale}
        setScale={setScale}
        tool={tool}
        setTool={setTool}
      />
      <EditorSelectionArea
        scale={scale}
        tool={tool}
        translation={{ x: translation.x + newTranslation.x, y: translation.y + newTranslation.y }}
      />
    </div>
  )
}
