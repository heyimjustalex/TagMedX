'use client'

import { Button } from '@nextui-org/button'
import { checkSession } from '../utils/localSession';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();
  return (
    <section className='page flex-col'>
      <h1 className='head-text text-center'>
        <span className='gradient-blue text-center'>TagMedX</span>
      </h1>
      <p className='desc text-center mt-6 max-w-md'>
        TagMedX is an open-source web app built with FastAPI,
        Next.js and MySQL, designed for medical image tagging.
      </p>
      <Button
        className='flex w-30 mt-4'
        color='primary'
        variant='ghost'
        onPress={checkSession() ? () => router.push('/groups') : () => router.push('/login')}
      >
        Let's tag!
      </Button>
    </section>
  )
}