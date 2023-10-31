import { NextColor } from '../../consts/NextColor'

export async function handleLogin(setSent, data, setError, router, notification) {
  setSent(true)
  await fetch(process.env.NEXT_PUBLIC_API + 'login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  }).then(res => {
    if(res.ok) {
      router.push('/')
    } else {
      if(res.status === 401) setError({ email: false, user: false, password: true })
      if(res.status === 404) setError({ email: false, user: true, password: false })
      if(res.status === 406) setError({ email: true, user: true, password: false })
      if(res.status === 500) notification.make(NextColor.DANGER, 'Couldn\'t login', 'Something went wrong.' );
      throw Error(`${res.status} ${res.statusText}`)
    }
  })
  .catch(err => {
    console.error(err);
  })
  setSent(false);
}
