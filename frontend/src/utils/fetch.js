async function get(url) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'GET',
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

async function post(url, data) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'POST',
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

async function put(url, data) {
  const res = await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'PUT',
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

export { get, post, put, patch }