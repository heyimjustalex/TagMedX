import { get } from '../../../../../../../../utils/serverFetch';

export async function getLabels(setId) {
  if(!isNaN(setId)) {
    const res = await get(`labels/set/${setId}`);
    if(!res.ok) console.error(`Get set labels: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: [] });
}