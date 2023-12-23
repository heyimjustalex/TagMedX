import { get } from '../../../../../../../../utils/serverFetch';

export async function getLabels(setId) {
  if(!isNaN(setId)) {
    const res = await get(`labels/set/${setId}`);
    if(!res.ok) console.error(`Get set labels: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: [] });
}

export async function getPackage(packageId, tentative) {
  if(!isNaN(packageId)) {
  const res = await get(`packages/${packageId}/extend?tentative=${tentative ? 'true' : 'false'}`);
    if(!res.ok) console.error(`Get package: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: {} });
}

export async function getSet(setId) {
  if(!isNaN(setId)) {
  const res = await get(`sets/${setId}`);
    if(!res.ok) console.error(`Get set: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: {} });
}

export async function getRole(groupId) {
  if(!isNaN(groupId)) {
  const res = await get(`groups/${groupId}/role`);
    if(!res.ok) console.error(`Get role: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: '' });
}