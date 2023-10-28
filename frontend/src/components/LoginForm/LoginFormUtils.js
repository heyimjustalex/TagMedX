import { NextColor } from '../../consts/NextColor';

export async function handleLogin(setSent, data, router, notification) {
  setSent(true)
  await fetch(process.env.NEXT_PUBLIC_API + '/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => {
    if(!res.ok) throw Error;
    router.push('/')
    notification.make(NextColor.Success, 'Login', `${''}test test etst`);
  })
  .catch(err => {
    console.error('Error:', err);
    notification.make(NextColor.Danger, 'Login', `${''}test test etst`);
  })
  setSent(false);
}
