'use client'
import { useCallback, useEffect, useState } from 'react';

import { Tool } from './EditorConsts';
import EditorTools from './EditorTools';
import EditorDescriptor from './EditorDescriptor';
import EditorNavigation from './EditorNavigation';
import EditorSelectionArea from './EditorSelectionArea';

export default function Editor({ user, pack, labels }) {

  const [pan, setPan] = useState(false);
  const [scale, setScale] = useState(1);
  const [bboxes, setBboxes] = useState([]);
  const [tool, setTool] = useState(Tool.SELECT);
  const [startPoint, setStartPoint] = useState({ x: 0, y: 0 });
  const [translation, setTranslation] = useState({ x: 0, y: 0 });
  const [newTranslation, setNewTranslation] = useState({ x: 0, y: 0 });
  const [status, setStatus] = useState({ ready: false, error: false });
  const [examination, setExamination] = useState({ id_user: '', user: '', tentative: false });
  const [pointer, setPointer] = useState(pack?.samples?.findIndex(e => e?.examinations?.length < 1) || 0);

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

  useEffect(() => {
    if(pack?.samples[pointer]?.examinations?.length) {
      setExamination({
        id_user: pack?.samples[pointer]?.examinations[0]?.id_user,
        user: pack?.samples[pointer]?.examinations[0]?.user,
        tentative: pack?.samples[pointer]?.examinations[0]?.tentative || false
      });
      if(pack?.samples[pointer]?.examinations[0]?.bboxes) {
        setBboxes(pack?.samples[pointer]?.examinations[0].bboxes);
      }
    } else {
      setExamination({ id_user: user?.user_id, user: `${user?.title} ${user?.name} ${user?.surname}`, tentative: false });
      setBboxes([]);
    }
  }, [pointer, user]);

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
        labels={labels}
        setBboxes={setBboxes}
        examination={examination}
        setExamination={setExamination}
        bbox={bboxes.find(e => e.active)}
      />
      <EditorNavigation 
        pointer={pointer}
        setStatus={setStatus}
        setPointer={setPointer}
        length={pack?.samples?.length}
      />
      <EditorSelectionArea
        tool={tool}
        scale={scale}
        bboxes={bboxes}
        status={status}
        setBboxes={setBboxes}
        setStatus={setStatus}
        sampleId={pack?.samples[pointer]?.id}
        setTranslation={setTranslation}
        translation={{ x: translation.x + newTranslation.x, y: translation.y + newTranslation.y }}
      />
    </div>
  )
}
