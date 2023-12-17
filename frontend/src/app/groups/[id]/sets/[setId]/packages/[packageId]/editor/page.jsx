import { getLabels, getPackage } from './utils';
import Editor from '../../../../../../../../components/Editor/Editor';
import { redirect } from 'next/navigation';

export default async function EditorPage({ params }) {

  const [pack, labels] = await Promise.all([
    getPackage(params.packageId),
    getLabels(params.setId)
  ]);

  return (
    <>
      { 
        [pack.code, labels.code].includes(401) ? redirect('/login?expired=1') :
        <section className='editor-page'>
          <Editor pack={pack.body} labels={labels.body} />
        </section>
      }
    </>
  )
}