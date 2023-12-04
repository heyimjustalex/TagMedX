import { getLabels } from './utils';
import Editor from '../../../../../../../../components/Editor/Editor';
import { redirect } from 'next/navigation';

export default async function EditorPage({ params }) {

  const labels = await getLabels(params.setId);

  return (
    <>
      { 
        [labels.code].includes(401) ? redirect('/login?expired=1') :
        <section className='editor-page'>
          <Editor labels={labels.body} />
        </section>
      }
    </>
  )
}