import { get } from '../../../utils/serverFetch';
import Group from '../../../components/Group/Group';

async function getData(id) {
  const res = await get(`groups/${id}`);
  if(res.ok) return res.body;
  else console.error(`${res.code} ${res.status}`);
}

async function getUsers(id) {
  const res = await get(`groups/${id}/users`);
  if(res.ok) return res.body.members;
  else console.error(`${res.code} ${res.status}`);
}

export default async function GroupPage({ params }) {

  const [data, users] = await Promise.all([getData(params.id), getUsers(params.id)]);

  return (
    <section className='content-page flex flex-col'>
      <Group data={{ ...data, users: users }} />
    </section>
  )
}