import { getUser } from './utils';
import Profile from '../../components/Profile/Profile';
import { checkSession } from '../../utils/serverSession';

export default async function ProfilePage() {

  const user = await getUser(checkSession());

  return (
    <section className='page'>
      <Profile data={user.body} />
    </section>
  )
}
