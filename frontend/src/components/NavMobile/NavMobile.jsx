'use client'

import { NavbarBrand, NavbarContent, NavbarMenu, NavbarMenuItem } from '@nextui-org/navbar';
import { Link } from '@nextui-org/link';
import RouteLink from 'next/link';

import { menuItems } from './NavMobileConsts';
import { Button } from '@nextui-org/react';
import { useUserId } from '../../hooks/useUserId';

export default function NavMobile () {

  const { userId } = useUserId();

  return (
    <>
      <NavbarContent className='sm:hidden w-full flex-center flex-col' justify='center'>
          <NavbarBrand>
              <RouteLink href='/' className='font-bold text-inherit'>
                  TagMedX
              </RouteLink>
          </NavbarBrand>
      </NavbarContent>

      <NavbarMenu>
        {userId ?
          <>
            {menuItems.map((e, i) => (
              <NavbarMenuItem key={`${e.url}-${i}`}>
                <Link
                  className='w-full'
                  color={e.color}
                  href={e.url}
                  size='lg'
                  as={RouteLink}
                >
                  {e.name}
                </Link>
              </NavbarMenuItem>
            ))}
            <NavbarMenuItem>
              <Button
                className='w-full'
                color='danger'
                // size='lg'
                variant='ghost'
                onClick={() => console.log('logout')}
              >
                Logout
              </Button>
            </NavbarMenuItem>
          </>
        : menuItems.map((e, i) => (
          <NavbarMenuItem key={`${e.url}-${i}`}>
            <Link
              className='w-full'
              color={e.color}
              href={e.url}
              size='lg'
              as={RouteLink}
            >
              {e.name}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </>
  )
}