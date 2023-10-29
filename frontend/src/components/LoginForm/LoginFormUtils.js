import { NextColor } from '../../consts/NextColor';

export async function handleLogin(setSent, data, router, notification) {
  setSent(true)
  await fetch(process.env.NEXT_PUBLIC_API + '/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => {
    if(res.ok) {
      router.push('/')
    } else {
      throw Error(`${res.status} ${res.statusText}`)
    }
  })
  .catch(err => {
    console.error(err);
    notification.make(NextColor.Danger, 'Login', 'Something went wrong.');
  })
  setSent(false);
}
