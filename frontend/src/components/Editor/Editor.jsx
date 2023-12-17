'use client'

import { useCallback, useState } from 'react';

import { Tool } from './EditorConsts';
import EditorTools from './EditorTools';
import EditorDescriptor from './EditorDescriptor';
import EditorSelectionArea from './EditorSelectionArea';

export default function Editor({ labels }) {

  const [tags, setTags] = useState([]);
  const [pan, setPan] = useState(false);
  const [scale, setScale] = useState(1);
  const [bboxes, setBboxes] = useState([]);
  const [tool, setTool] = useState(Tool.SELECT);
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
        x: Math.floor((x - startPoint.x) / scale),
        y: Math.floor((y - startPoint.y) / scale),
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
        tool={tool}
        scale={scale}
        setTool={setTool}
        setScale={setScale}
        setTranslation={setTranslation}
      />
      <EditorDescriptor
        tags={tags}
        labels={labels}
        setTags={setTags}
        setBboxes={setBboxes}
        bbox={bboxes.find(e => e.active)}
      />
      <EditorSelectionArea
        tool={tool}
        scale={scale}
        bboxes={bboxes}
        setBboxes={setBboxes}
        translation={{ x: translation.x + newTranslation.x, y: translation.y + newTranslation.y }}
      />
    </div>
  )
}
