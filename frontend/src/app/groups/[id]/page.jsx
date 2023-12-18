import { redirect } from 'next/navigation';

import Group from '../../../components/Group/Group';
import { getData, getLabels, getPackages, getSets, getUsers } from './utils';

export default async function GroupPage({ params }) {

  const [data, users, sets, packages, labels] = await Promise.all([
    getData(params.id),
    getUsers(params.id),
    getSets(params.id),
    getPackages(params.id),
    getLabels(params.id)
  ]);

  return (
    <>
      { 
        [data.code, users.code, sets.code, packages.code, labels.code].includes(401) ? redirect('/login?expired=1') :
        <section className='content-page flex flex-col'>
          <Group group={{
            ...data.body,
            users: users.body,
            sets: sets.body,
            packages: packages.body,
            labels: labels.body
          }} />
        </section>
      }
    </>
  )
}