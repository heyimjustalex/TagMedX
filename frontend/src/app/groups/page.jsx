export default function Groups() {
  return (
    <section className='page'>
      {typeof window !== 'undefined' ? window?.location?.pathname : 'Server component'}
    </section>
  )
}