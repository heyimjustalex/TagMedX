'use client'

import { NavbarBrand, NavbarContent, NavbarMenu, NavbarMenuItem } from '@nextui-org/navbar';
import { useRouter } from 'next/navigation';
import { Link } from '@nextui-org/link';
import RouteLink from 'next/link';
import { useEffect, useState } from 'react';

import { menuItems } from '../NavConsts';
import { menuItemsUnlogged } from './NavMobileConsts';
import { handleLogout } from '../NavUtils';
import { useUserId } from '../../../hooks/useUserId';
import { useNotification } from '../../../hooks/useNotification';

export default function NavMobile ({ setIsMenuOpen }) {

  const router = useRouter();
  const notification = useNotification();
  const { userId, setUserId } = useUserId();
  const [isClient, setIsClient] = useState(false);
 
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
                  size='lg'
                  href={e.url}
                  as={RouteLink}
                  color={e.color}
                  className='w-full'
                  onPress={() => setIsMenuOpen(false)}
                >
                  {e.name}
                </Link>
              </NavbarMenuItem>
            ))}
            <NavbarMenuItem>
              <Link
                size='lg'
                color='danger'
                className='w-full cursor-pointer'
                onPress={() => { handleLogout(setUserId, router, notification); setIsMenuOpen(false)}}
              >
                Logout
              </Link>
            </NavbarMenuItem>
          </>
        : menuItemsUnlogged.map((e, i) => (
          <NavbarMenuItem key={`${e.url}-${i}`}>
            <Link
              size='lg'
              href={e.url}
              as={RouteLink}
              color={e.color}
              className='w-full'
              onPress={() => setIsMenuOpen(false)}
            >
              {e.name}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </>
  )
}