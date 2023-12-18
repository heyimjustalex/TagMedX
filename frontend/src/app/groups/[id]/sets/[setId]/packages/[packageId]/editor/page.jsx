import { redirect } from 'next/navigation';
import { getLabels, getPackage } from './utils';
import { getUser } from '../../../../../../../profile/utils';
import Editor from '../../../../../../../../components/Editor/Editor';
import { checkSession } from '../../../../../../../../utils/serverSession';

export default async function EditorPage({ params }) {

  const [user, pack, labels] = await Promise.all([
    getUser(checkSession()),
    getPackage(params.packageId),
    getLabels(params.setId)
  ]);

  return (
    <>
      { 
        [user.code, pack.code, labels.code].includes(401) ? redirect('/login?expired=1') :
        <section className='editor-page'>
          <Editor user={user.body} pack={pack.body} labels={labels.body} />
        </section>
      }
    </>
  )
}