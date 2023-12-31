'use client'
import { useCallback, useEffect, useMemo, useState } from 'react';

import { Tool } from './EditorConsts';
import EditorTools from './EditorTools';
import EditorDescriptor from './EditorDescriptor';
import EditorNavigation from './EditorNavigation';
import EditorSelectionArea from './EditorSelectionArea';
import { bboxCompare, examinationCompare, getPointerDefaultValue } from './EditorUtils';

export default function Editor({ user, data, labels, set }) {

  const [pan, setPan] = useState(false);
  const [scale, setScale] = useState(1);
  const [pack, setPack] = useState(data);
  const [bboxes, setBboxes] = useState([]);
  const [tool, setTool] = useState(Tool.SELECT);
  const [startPoint, setStartPoint] = useState({ x: 0, y: 0 });
  const [translation, setTranslation] = useState({ x: 0, y: 0 });
  const [newTranslation, setNewTranslation] = useState({ x: 0, y: 0 });
  const [status, setStatus] = useState({ ready: false, error: false });
  const [examination, setExamination] = useState({ id_user: '', user: '', role: '?', tentative: false });
  const [pointer, setPointer] = useState(() => getPointerDefaultValue(pack?.samples));

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

  const setDefaultValues = useCallback(() => {
    if(pack?.samples[pointer]?.examination) {
      setExamination({
        id: pack?.samples[pointer]?.examination?.id,
        id_sample: pack?.samples[pointer]?.examination?.id_sample,
        id_user: pack?.samples[pointer]?.examination?.id_user,
        user: pack?.samples[pointer]?.examination?.user,
        role: pack?.samples[pointer]?.examination?.role,
        tentative: pack?.samples[pointer]?.examination?.tentative || false
      });
      if(pack?.samples[pointer]?.examination?.bboxes) {
        setBboxes(pack?.samples[pointer]?.examination.bboxes);
      }
    } else {
      setExamination({
        id: null,
        id_sample: null,
        id_user: user?.user_id,
        user: `${user?.title} ${user?.name} ${user?.surname}`,
        role: user?.role,
        tentative: false
      });
      setBboxes([]);
    }
  }, [pack, pointer, user])

  useEffect(setDefaultValues, [pack, pointer, user]);

  const changed = useMemo(() =>
    !(examinationCompare(pack?.samples[pointer]?.examination, examination)
    && bboxCompare(pack?.samples[pointer]?.examination?.bboxes, bboxes))
  , [examination, bboxes])

  const adminOverride = useMemo(() =>
    user.role === 'User' &&
    pack?.samples[pointer]?.examination?.role === 'Admin'
  , [pack, pointer, user])

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
        user={user}
        tool={tool}
        scale={scale}
        bboxes={bboxes}
        pointer={pointer}
        setPack={setPack}
        changed={changed}
        setTool={setTool}
        setScale={setScale}
        examination={examination}
        setTranslation={setTranslation}
        sampleId={pack?.samples[pointer]?.id}
        setDefaultValues={setDefaultValues}
      />
      <EditorDescriptor
        labels={labels}
        setBboxes={setBboxes}
        examination={examination}
        adminOverride={adminOverride}
        setExamination={setExamination}
        bbox={bboxes.find(e => e.active)}
      />
      <EditorNavigation
        pointer={pointer}
        changed={changed}
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
        adminOverride={adminOverride}
        setTranslation={setTranslation}
        detection={set.type === 'Detection'}
        sampleId={pack?.samples[pointer]?.id}
        translation={{ x: translation.x + newTranslation.x, y: translation.y + newTranslation.y }}
      />
    </div>
  )
}
