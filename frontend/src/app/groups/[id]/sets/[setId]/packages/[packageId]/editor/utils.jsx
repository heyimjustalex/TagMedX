import { get } from '../../../../../../../../utils/serverFetch';

export async function getLabels(setId) {
  if(!isNaN(setId)) {
    const res = await get(`labels/set/${setId}`);
    if(!res.ok) console.error(`Get set labels: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: [] });
}

export async function getPackage(packageId) {
  if(!isNaN(packageId)) {
  const res = await get(`packages/${packageId}/extend`);
    if(!res.ok) console.error(`Get set labels: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: [] });
}