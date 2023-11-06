import { get } from '../../../utils/serverFetch';

async function getData(id) {
  const res = await get(`groups/${id}`);
  if(res.ok) return res.body;
  else console.error(`${res.code} ${res.status}`);
}

export default async function Groups({ params }) {

  const data = await getData(params.id);

  return (
    <section className='content-page flex flex-col'>
      <div className='flex'>
        <h1 className='text-5xl font-bold'>{data?.name}</h1>
      </div>
      <div className='flex text-sm py-4 px-1'>{data?.description}</div>
    </section>
  )
}