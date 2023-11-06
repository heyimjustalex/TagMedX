'use client'

import { NavbarBrand, NavbarContent, NavbarMenu, NavbarMenuItem } from '@nextui-org/navbar';
import { useRouter } from 'next/navigation';
import { Link } from '@nextui-org/link';
import RouteLink from 'next/link';
import { useEffect, useState } from 'react';

import { Button } from '@nextui-org/react';
import { menuItems } from '../NavConsts';
import { menuItemsUnlogged } from './NavMobileConsts';
import { handleLogout } from '../NavUtils';
import { useUserId } from '../../../hooks/useUserId';
import { useNotification } from '../../../hooks/useNotification';

export default function NavMobile () {

  const router = useRouter();
  const notification = useNotification();
  const { userId, setUserId } = useUserId();
  const [isClient, setIsClient] = useState(false)
 
  useEffect(() => {
    setIsClient(true)
  }, [])

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
        {isClient && userId ?
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
                variant='ghost'
                onClick={() => handleLogout(setUserId, router, notification)}
              >
                Logout
              </Button>
            </NavbarMenuItem>
          </>
        : menuItemsUnlogged.map((e, i) => (
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