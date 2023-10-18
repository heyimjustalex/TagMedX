import { NavbarBrand, NavbarItem, NavbarContent } from "@nextui-org/navbar";
import { Button } from "@nextui-org/button";
import { Link } from "@nextui-org/link";

import { menuItems } from "./NavDesktopConsts";

const NavDesktop = () => {
    return (
        <>
            <NavbarContent className="hidden sm:flex gap-4" justify="center">
                <NavbarBrand>
                    <Link href="/" className="font-bold text-inherit">
                        TagMedX
                    </Link>
                </NavbarBrand>
                {menuItems.map((e, i) => (
                    <NavbarItem key={`${e.url}-${i}`}>
                        <Link href="#" color={e.color}>
                            {e.name}
                        </Link>
                    </NavbarItem>
                ))}
            </NavbarContent>

            <NavbarContent className="hidden sm:flex" justify="end">
                <NavbarItem>
                    <Link href="/signup">Sign Up</Link>
                </NavbarItem>
                <NavbarItem>
                    <Button as={Link} color="primary" href="/login" variant="solid">
                        Login
                    </Button>
                </NavbarItem>
            </NavbarContent>
        </>
    )
}

export default NavDesktop