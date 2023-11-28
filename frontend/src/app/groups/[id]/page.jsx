import { redirect } from 'next/navigation';

import { get } from '../../../utils/serverFetch';
import { capitalize } from '../../../utils/text';
import Group from '../../../components/Group/Group';

async function getData(id) {
  if(!isNaN(id)) {
    const res = await get(`groups/${id}`);
    if(!res.ok) console.error(`Get group: ${res.code} ${res.status}`);
    return res;
  } else return Promise.resolve({ code: 204, body: [] });
}

async function getUsers(id) {
  if(!isNaN(id)) {
    const res = await get(`groups/${id}/users`);
    if(!res.ok) console.error(`Get group users: ${res.code} ${res.status}`);
    return res;
  } else return Promise.resolve({ code: 204, body: { members: [] } });
}

async function getSets(id) {
  if(!isNaN(id)) {
    const res = await get(`sets/group/${id}`);
    if(!res.ok) console.error(`Get group sets: ${res.code} ${res.status}`);
    return res;
  } else return Promise.resolve({ code: 204, body: [] });
}

async function getPackages(id, setId) {
  if(!isNaN(id) && setId) {
    const res = await get(`packages/set/${setId}`);
    if(!res.ok) console.error(`Get group sets: ${res.code} ${res.status}`);
    return res;
  } else return Promise.resolve({ code: 204, body: { packages: [] } });
}

async function getLabels(id, setId) {
  if(!isNaN(id) && setId) {
    const res = await get(`labels/set/${setId}`);
    if(!res.ok) console.error(`Get group labels: ${res.code} ${res.status}`);
    return res;
  } else return Promise.resolve({ code: 204, body: [] });
}

export async function generateMetadata({ params, searchParams }) {
  if(!isNaN(params.id)) {
    const res = await get(`groups/${params.id}/name`);
    if(res.ok) return { title: `TagMedX - ${res.body}${searchParams.tab ? ' - ' + capitalize(searchParams.tab) : ''}` };
  }
  return { title: `TagMedX - Group no. ${params.id}` };
}

export default async function GroupPage({ params, searchParams }) {

  const [data, users, sets, packages, labels] = await Promise.all([
    getData(params.id),
    getUsers(params.id),
    getSets(params.id),
    getPackages(params.id, searchParams.set),
    getLabels(params.id, searchParams.set)
  ]);

  return (
    <>
      { 
        [data.code, users.code, sets.code].includes(401) ? redirect('/login?expired=1') :
        <section className='content-page flex flex-col'>
          <Group group={{
            ...data.body,
            users: users.body.members || [],
            sets: sets.body || [],
            packages: packages.body.packages || [],
            labels: labels.body || []
          }} />
        </section>
      }
    </>
  )
}