import { get } from '../../../utils/serverFetch';
import Group from '../../../components/Group/Group';
import { capitalize } from '../../../utils/text';

async function getData(id) {
  const res = await get(`groups/${id}`);
  if(res.ok) return res.body;
  else {
    console.error(`${res.code} ${res.status}`);
    return {};
  }
}

async function getUsers(id) {
  const res = await get(`groups/${id}/users`);
  if(res.ok) return res.body.members;
  else {
    console.error(`${res.code} ${res.status}`);
    return [];
  }
}

async function getSets(id) {
  const res = await get(`sets/group/${id}`);
  if(res.ok) return res.body;
  else {
    console.error(`${res.code} ${res.status}`);
    return [];
  }
}

export async function generateMetadata({ params, searchParams }) {
  const res = await get(`groups/${params.id}/name`);
  if(res.ok) return { title: `TagMedX - ${res.body} - ${capitalize(searchParams.tab)}` };
  else return { title: `TagMedX - Group no. ${params.id}` };
}

export default async function GroupPage({ params }) {

  const [data, users, sets] = await Promise.all([getData(params.id), getUsers(params.id), getSets(params.id)]);

  return (
    <section className='content-page flex flex-col'>
      <Group data={{ ...data, users: users, sets: sets }} />
    </section>
  )
}