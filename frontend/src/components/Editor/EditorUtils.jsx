import { NextColor } from '../../consts/NextColor';
import { del, put } from '../../utils/fetch';

export async function getSample(setImage, setStatus, sampleId, notification) {

  setStatus({ ready: false, error: false });
  setImage({ src: '', width: 0, height: 0 })
  
  fetch(process.env.NEXT_PUBLIC_API + `samples/${sampleId}`, {
    method: 'GET',
    credentials: 'include',
    headers: { 'Content-Type': '*/*' }
  })
  .then(res => {
    if(!res.ok) throw new Error(`${res.status} ${res.statusText}`)
    return res
  })
  .then(res => res.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const img = new Image();
    img.src = url;
    img.onload = () => {
      setImage({ src: url, width: img.width, height: img.height });
    };
    setStatus({ ready: true, error: false });
  })
  .catch((err) => {
    console.error(err)
    setStatus({ ready: false, error: true });
    notification.make(NextColor.DANGER, 'Error', 'Could not load sample image.');
  })
}

export function examinationCompare(e1, e2) {
  if(e1) {
    return e1?.id_user === e2?.id_user && e1?.tentative === e2?.tentative;
  } else return true;
  
}

export function bboxCompare(b1, b2) {
  if(!b1 && b2.length === 0) return true;
  else if(b1?.length === b2.length) {
    if(b1.some((bbox, i) =>
      bbox.x != b2[i].x ||
      bbox.y != b2[i].y ||
      bbox.width != b2[i].width ||
      bbox.height != b2[i].height ||
      bbox.id_label != b2[i].id_label ||
      bbox.comment != b2[i].comment
    )) return false;
  } else return false;
  return true;
}

export async function saveExamination(pointer, examination, bboxes, sampleId, user, setPack, notification) {
  const res = await put('examinations', {
    id: examination.id || null,
    id_sample: sampleId,
    tentative: examination.tentative,
    BBox: bboxes.map(e => ({
      x: e.x,
      y: e.y,
      width: e.width,
      height: e.height,
      comment: e.comment || null,
      id_label: e?.label?.id || null
    })),
  });

  if(res.ok) {
    setPack(prev => ({
      ...prev,
      samples: [...prev.samples.map((e, i) => ({
        id: e.id,
        id_package: e.id_package,
        examination: pointer === i ?
          {
            bboxes: bboxes,
            id: examination.id || null, // here use response id
            id_sample: res.body.id_sample,
            id_user: user.id,
            role: user.role,
            tentative: res.body.tentative,
            user: `${user.title} ${user.name} ${user.surname}`
          }
        : e.examination
      }))]
    }));
    notification.make(NextColor.SUCCESS, 'Examination saved', 'You have successfully saved examination.');
  }
  else {
    notification.make(NextColor.DANGER, 'Examination error', 'Could not save examination.');
  }
}

export async function deleteExamination(pointer, examination, setPack, notification) {
  const res = await del(`examinations/${examination.id}`);

  if(res.ok) {
    setPack(prev => ({
      ...prev,
      samples: [...prev.samples.map((e, i) => ({
        id: e.id,
        id_package: e.id_package,
        examination: pointer === i ? null : e.examination
      }))]
    }));
    notification.make(NextColor.SUCCESS, 'Examination removed', 'You have successfully removed examination.');
  }
  else {
    notification.make(NextColor.DANGER, 'Examination error', 'Could not remove examination.');
  }
}

export function getPointerDefaultValue(samples) {
  if(samples) {
    const index = samples?.findIndex(e => !e?.examination);
    return index !== -1 ? index : 0;
  } else return 0;
}