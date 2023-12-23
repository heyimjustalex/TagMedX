import { redirect } from 'next/navigation';
import { getLabels, getPackage, getRole, getSet } from './utils';
import { getUser } from '../../../../../../../profile/utils';
import Editor from '../../../../../../../../components/Editor/Editor';
import { checkSession } from '../../../../../../../../utils/serverSession';

export default async function EditorPage({ params, searchParams }) {

  const [user, role, data, labels, set] = await Promise.all([
    getUser(checkSession()),
    getRole(params.id),
    getPackage(params.packageId, searchParams.tentative),
    getLabels(params.setId),
    getSet(params.setId)
  ]);

  return (
    <>
      { 
        [user.code, role.code, data.code, labels.code, set.code].includes(401) ? redirect('/login?expired=1') :
        <section className='editor-page'>
          <Editor user={{ ...user.body, role: role.body }} data={data.body} labels={labels.body} set={set.body} />
        </section>
      }
    </>
  )
}