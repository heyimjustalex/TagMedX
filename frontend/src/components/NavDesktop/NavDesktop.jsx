'use client'

import { NavbarBrand, NavbarContent, NavbarItem } from '@nextui-org/navbar';
import { Button } from '@nextui-org/button';
import { Link } from '@nextui-org/link';
import RouteLink from 'next/link';

import { menuItems } from './NavDesktopConsts';
import { useUserId } from '../../hooks/useUserId';

export default function NavDesktop () {

  const { userId } = useUserId();
  console.log(userId)

  return (
    <>
      <NavbarContent className='hidden sm:flex gap-4' justify='center'>
        <NavbarBrand>
          <RouteLink href='/' className='font-bold text-inherit'>
            TagMedX
          </RouteLink>
        </NavbarBrand>
        {userId ? menuItems.map((e, i) => (
          <NavbarItem key={`${e.url}-${i}`}>
            <Link as={RouteLink} href={e.url} color={e.color}>
              {e.name}
            </Link>
          </NavbarItem>
        )) : null}
      </NavbarContent>

      <NavbarContent className='hidden sm:flex' justify='end'>
        {userId ? <>
          <NavbarItem>
            <Button
                className='w-full'
                color='danger'
                variant='ghost'
                onClick={() => console.log('logout')}
              >
                Logout
              </Button>
          </NavbarItem>
        </> : <>
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
        </>}
      </NavbarContent>
    </>
  )
}