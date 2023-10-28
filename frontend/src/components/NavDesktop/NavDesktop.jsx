import { NavbarBrand, NavbarContent, NavbarItem } from '@nextui-org/navbar';
import { Button } from '@nextui-org/button';
import { Link } from '@nextui-org/link';
import RouteLink from 'next/link';

import { menuItems } from './NavDesktopConsts';

export default function NavDesktop () {
  return (
    <>
      <NavbarContent className='hidden sm:flex gap-4' justify='center'>
        <NavbarBrand>
          <RouteLink href='/' className='font-bold text-inherit'>
            TagMedX
          </RouteLink>
        </NavbarBrand>
        {menuItems.map((e, i) => (
          <NavbarItem key={`${e.url}-${i}`}>
            <Link as={RouteLink} href={e.url} color={e.color}>
              {e.name}
            </Link>
          </NavbarItem>
        ))}
      </NavbarContent>

      <NavbarContent className='hidden sm:flex' justify='end'>
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
      </NavbarContent>
    </>
  )
}