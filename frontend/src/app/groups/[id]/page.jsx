import { redirect } from 'next/navigation';

import Group from '../../../components/Group/Group';
import { getData, getLabels, getPackages, getSets, getUsers, getStats } from './utils';

export default async function GroupPage({ params }) {

  const [data, users, sets, packages, labels, stats] = await Promise.all([
    getData(params.id),
    getUsers(params.id),
    getSets(params.id),
    getPackages(params.id),
    getLabels(params.id),
    getStats(params.id)
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
            labels: labels.body,
            stats: stats.body
          }} />
        </section>
      }
    </>
  )
}