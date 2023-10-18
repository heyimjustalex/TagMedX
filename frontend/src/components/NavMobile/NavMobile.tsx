import { NavbarBrand, NavbarMenuItem, NavbarMenu, NavbarContent } from "@nextui-org/navbar";
import { Link } from "@nextui-org/link";
import RouteLink from "next/link";

import { menuItems } from "./NavMobileConsts";

const NavMobile = () => {
    return (
        <>
            <NavbarContent className="sm:hidden w-full flex-center flex-col" justify="center">
                <NavbarBrand>
                    <RouteLink href="/" className="font-bold text-inherit">
                        TagMedX
                    </RouteLink>
                </NavbarBrand>
            </NavbarContent>

            <NavbarMenu>
                {menuItems.map((e, i) => (
                    <NavbarMenuItem key={`${e.url}-${i}`}>
                        <Link
                            className="w-full"
                            color={e.color}
                            href={e.url}
                            size="lg"
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

export default NavMobile