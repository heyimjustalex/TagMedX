'use client'

import { NavbarBrand, NavbarContent, NavbarItem } from '@nextui-org/navbar';
import { Button } from '@nextui-org/button';
import { Skeleton } from '@nextui-org/skeleton';
import { useRouter } from 'next/navigation';
import { Link } from '@nextui-org/link';
import RouteLink from 'next/link';
import { useEffect, useState } from 'react';

import { handleLogout } from '../Nav/NavUtils';
import { menuItems } from './NavDesktopConsts';
import { useUserId } from '../../hooks/useUserId';
import { useNotification } from '../../hooks/useNotification';

export default function NavDesktop () {

  const router = useRouter();
  const notification = useNotification();
  const { userId, setUserId } = useUserId();
  const [isClient, setIsClient] = useState(false);
 
  useEffect(() => {
    setIsClient(true)
  }, [])

  return (
    <>
      <NavbarContent className='hidden sm:flex gap-4' justify='center'>
        <NavbarBrand>
          <RouteLink href='/' className='font-bold text-inherit'>
            TagMedX
          </RouteLink>
        </NavbarBrand>
        {isClient && userId ? menuItems.map((e, i) => (
          <NavbarItem key={`${e.url}-${i}`}>
            <Link as={RouteLink} href={e.url} color={e.color}>
              {e.name}
            </Link>
          </NavbarItem>
        )) : null}
      </NavbarContent>

      <NavbarContent className='hidden sm:flex' justify='end'>
        {isClient && userId ? <>
          <NavbarItem>
            <Button
              className='w-full'
              color='danger'
              variant='ghost'
              onClick={() => handleLogout(setUserId, router, notification)}
            >
              Logout
            </Button>
          </NavbarItem>
        </> : isClient ? <>
          <NavbarItem>
            <Link as={RouteLink} href='/signup'>
              Sign Up
            </Link>
          </NavbarItem>
          <NavbarItem>
            <Button as={RouteLink} color='primary' href='/login' variant='solid'>
              Login
            </Button>
          </NavbarItem>
        </> : <NavbarItem>
          <Skeleton className="rounded-lg">
            <div className="h-10 w-20 rounded-lg bg-default-300" />
          </Skeleton>
        </NavbarItem>
        }
      </NavbarContent>
    </>
  )
}