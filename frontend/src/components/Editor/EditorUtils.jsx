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