import { cookies } from 'next/headers';

async function get(url) {
  const cookieStore = cookies();
  const cookie = cookieStore.get('token');

  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Cookie': `${cookie?.name}=${cookie?.value}`,
      'Content-Type': 'application/json'
    }
  })

  const body = res.ok ? await res.json() : Promise.resolve(null);

  return {
    ok: res.ok,
    body: body,
    code: res.status,
    status: res.statusText
  }
}

async function post(url, data, cookie) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Cookie': `${cookie?.name}=${cookie?.value}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })

  const body = res.ok ? await res.json() : Promise.resolve(null);

  return {
    ok: res.ok,
    body: body,
    code: res.status,
    status: res.statusText
  }
}

async function put(url, data, cookie) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Cookie': `${cookie?.name}=${cookie?.value}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })

  const body = res.ok ? await res.json() : Promise.resolve(null);

  return {
    ok: res.ok,
    body: body,
    code: res.status,
    status: res.statusText
  }
}

async function patch(url, data, cookie) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'PATCH',
    credentials: 'include',
    headers: {
      'Cookie': `${cookie?.name}=${cookie?.value}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })

  const body = res.ok ? await res.json() : Promise.resolve(null);

  return {
    ok: res.ok,
    body: body,
    code: res.status,
    status: res.statusText
  }
}

export { get, post, put, patch }