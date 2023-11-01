'use client'
import { Suspense, useState } from 'react';
import {Navbar, NavbarContent, NavbarMenuToggle } from '@nextui-org/react';

import NavMobile from '../NavMobile/NavMobile';
import NavDesktop from '../NavDesktop/NavDesktop';

export default function Nav () {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <Suspense>
      <Navbar
        isBordered
        isMenuOpen={isMenuOpen}
        onMenuOpenChange={setIsMenuOpen}
      >
        <NavbarContent className='sm:hidden' justify='start'>
          <NavbarMenuToggle />
        </NavbarContent>

        <NavDesktop />
        <NavMobile />
      </Navbar>
    </Suspense>
  );
}