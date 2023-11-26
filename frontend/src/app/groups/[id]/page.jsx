import { redirect } from 'next/navigation';

import { get } from '../../../utils/serverFetch';
import { capitalize } from '../../../utils/text';
import Group from '../../../components/Group/Group';

async function getData(id) {
  const res = await get(`groups/${id}`);
  if(!res.ok) console.error(`Get group: ${res.code} ${res.status}`);
  return res;
}

async function getUsers(id) {
  const res = await get(`groups/${id}/users`);
  if(!res.ok) console.error(`Get group users: ${res.code} ${res.status}`);
  return res;
}

async function getSets(id) {
  const res = await get(`sets/group/${id}`);
  if(!res.ok) console.error(`Get group sets: ${res.code} ${res.status}`);
  return res;
}

export async function generateMetadata({ params, searchParams }) {
  const res = await get(`groups/${params.id}/name`);
  if(res.ok) return { title: `TagMedX - ${res.body} - ${capitalize(searchParams.tab)}` };
  else return { title: `TagMedX - Group no. ${params.id}` };
}

export default async function GroupPage({ params }) {

  const [data, users, sets] = await Promise.all([getData(params.id), getUsers(params.id), getSets(params.id)]);

  return (
    <>
      { 
        [data.code, users.code, sets.code].includes(401) ? redirect('/login?expired=1') :
        <section className='content-page flex flex-col'>
          <Group group={{ ...data.body, users: users.body.members, sets: sets.body }} />
        </section>
      }
    </>
  )
}