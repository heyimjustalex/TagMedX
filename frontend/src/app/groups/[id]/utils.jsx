import { get } from '../../../utils/serverFetch';
import { capitalize } from '../../../utils/text';

export async function getData(id) {
  if(!isNaN(id)) {
    const res = await get(`groups/${id}`);
    if(!res.ok) console.error(`Get group: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: [] });
}

export async function getUsers(id) {
  if(!isNaN(id)) {
    const res = await get(`groups/${id}/users`);
    if(!res.ok) console.error(`Get group users: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: { members: [] } });
}

export async function getSets(id) {
  if(!isNaN(id)) {
    const res = await get(`sets/group/${id}`);
    if(!res.ok) console.error(`Get group sets: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: [] });
}

export async function getPackages(id) {
  if(!isNaN(id)) {
    const res = await get(`packages/group/${id}`);
    if(!res.ok) console.error(`Get group sets: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: { packages: [] } });
}

export async function getLabels(id) {
  if(!isNaN(id)) {
    const res = await get(`labels/group/${id}`);
    if(!res.ok) console.error(`Get group labels: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: [] });
}

export async function getStats(id) {
  if(!isNaN(id)) {
    const res = await get(`group/${id}/stats`);
    if(!res.ok) console.error(`Get group stats: ${res.code} ${res.status}`);
    else return res;
  }
  return Promise.resolve({ code: 204, body: {} });
}

export async function generateMetadata({ params, searchParams }) {
  if(!isNaN(params.id)) {
    const res = await get(`groups/${params.id}/name`);
    if(res.ok) return { title: `TagMedX - ${res.body}${searchParams.tab ? ' - ' + capitalize(searchParams.tab) : ''}` };
  }
  return { title: `TagMedX - Group no. ${params.id}` };
}