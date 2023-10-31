'use client'
import { Button, Card, CardBody, CardFooter, CardHeader, Divider, Input } from '@nextui-org/react';
import RouteLink from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

import { defaultLoginData } from './LoginFormConsts';
import { handleLogin } from './LoginFormUtils';
import { useNotification } from '../../hooks/useNotification';

export default function LoginForm() {

  const router = useRouter();
  const notification = useNotification();
  const [data, setData] = useState(defaultLoginData);
  const [error, setError] = useState({ email: false, user: false, password: false });
  const [sent, setSent] = useState(false);

  return (
    <Card className='w-full max-w-xl min-w-0 h-fit'>
      <CardHeader className='flex gap-5'>
        <div className='flex flex-col'>
          <p className='text-xl font-medium'>Login</p>
        </div>
      </CardHeader>
      <Divider/>
      <CardBody className='flex gap-3'>
        <Input
          type='email'
          size='sm'
          label='Email'
          value={data.email}
          isInvalid={error.email || error.user}
          errorMessage={error.email ? 'Invalid email.' : error.user ? 'This user does not exist.' : ''}
          onChange={e => {
            setData(prev => { return { ...prev, email: e.target.value }})
            if(error.email || error.user) setError({ email: false, user: false, password: false })
          }}
        />
        <Input
          type='password'
          size='sm'
          label='Password'
          value={data.password}
          isInvalid={error.password}
          errorMessage={error.password ? 'Invalid password.' : null}
          onChange={e => {
            setData(prev => { return { ...prev, password: e.target.value }})
            if(error.password) setError({ email: false, password: false })
          }}
        />
      </CardBody>
      <Divider/>
      <CardFooter className='justify-around'>
        <Button
          className='flex'
          variant='light'
          color='primary'
          as={RouteLink}
          href='/signup'
        >
          Sign Up
        </Button>
        <Button
          className='flex'
          variant='solid'
          color='primary'
          onClick={() => handleLogin(setSent, data, setError, router, notification)}
          isLoading={sent}
        >
          Login
        </Button>
      </CardFooter>
    </Card>
  )
}