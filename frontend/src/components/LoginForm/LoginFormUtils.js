import { NextColor } from '../../consts/NextColor'

export async function handleLogin(setSent, data, setError, setUserId, router, notification) {
  setSent(true)
  const res = await fetch(process.env.NEXT_PUBLIC_API + 'login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  })

  if(res.ok) {
    const body = await res.json();
    router.push('/')
    setUserId(body.user_id);
  } else {
    switch(res.status) {
      case 401: setError({ email: false, user: false, password: true }); break;
      case 404: setError({ email: false, user: true, password: false }); break;
      case 406: setError({ email: true, user: true, password: false }); break;
      case 500: notification.make(NextColor.DANGER, 'Couldn\'t login', 'Something went wrong.' ); break;
      default: console.error(`${res.status} ${res.statusText}`); break;
    }
  }
}