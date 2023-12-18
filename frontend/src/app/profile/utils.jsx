import { get } from '../../utils/serverFetch';

export async function getUser(id) {
  const res = await get(`users/${id}`);
  if(res.ok) return res;
  else console.error(`${res.code} ${res.status}`);
}