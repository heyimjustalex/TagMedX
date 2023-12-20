import { NextColor } from '../../consts/NextColor';

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
    b1.forEach((bbox, i) => {
      if(
        bbox.x != b2[i].x ||
        bbox.y != b2[i].y ||
        bbox.width != b2[i].width ||
        bbox.height != b2[i].height ||
        bbox.id_label != b2[i].id_label ||
        bbox.comment != b2[i].comment
      ) return false;
    });
  } else return false;
  return true;
}