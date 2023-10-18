"use client"
import React, { useState } from "react";
import {Navbar, NavbarMenuToggle, NavbarContent } from "@nextui-org/react";

import NavMobile from "../NavMobile/NavMobile";
import NavDesktop from "../NavDesktop/NavDesktop";

const Nav = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <Navbar
            isBordered
            isMenuOpen={isMenuOpen}
            onMenuOpenChange={setIsMenuOpen}
        >
            <NavbarContent className="sm:hidden" justify="start">
                <NavbarMenuToggle />
            </NavbarContent>

            <NavDesktop />
            <NavMobile />
        </Navbar>
    );
}

export default Nav;