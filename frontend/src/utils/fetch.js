async function get(url) {
  await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  }).then(res => {
    return res;
  })
}

async function post(url, data) {
  await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => {
    return res;
  })
}

async function put(url, data) {
  await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => {
    return res;
  })
}

async function patch(url, data) {
  await fetch(process.env.NEXT_PUBLIC_API + url, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => {
    return res;
  })
}

export { get, post, put, patch }