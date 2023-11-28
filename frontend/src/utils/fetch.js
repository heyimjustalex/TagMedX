async function get(url) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'GET',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' }
  })

  const body = await res.json();

  return {
    ok: res.ok,
    body: body,
    code: res.status,
    status: res.statusText
  }
}

async function post(url, data, multipart = false) {

  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'POST',
    credentials: 'include',
    headers: multipart ? { 'Accept': 'application/json' } : { 'Content-Type': 'application/json' },
    body: multipart ? data : JSON.stringify(data)
  })

  const body = await res.json();

  return {
    ok: res.ok,
    body: body,
    code: res.status,
    status: res.statusText
  }
}

async function put(url, data) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })

  const body = await res.json();

  return {
    ok: res.ok,
    body: body,
    code: res.status,
    status: res.statusText
  }
}

async function patch(url, data) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'PATCH',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })

  const body = await res.json();

  return {
    ok: res.ok,
    body: body,
    code: res.status,
    status: res.statusText
  }
}

async function del(url) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'DELETE',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' }
  })

  const body = await res.json();

  return {
    ok: res.ok,
    body: body,
    code: res.status,
    status: res.statusText
  }
}

export { get, post, put, patch, del }