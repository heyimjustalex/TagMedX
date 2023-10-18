"use client"
import React from "react";
import {Card, CardHeader, CardBody, CardFooter, Divider, Link, Button, Input} from "@nextui-org/react";

const SignupForm = () => {
    return (
        <Card className="w-full max-w-xl min-w-0 h-fit">
            <CardHeader className="flex gap-5">
                <div className="flex flex-col">
                    <p className="text-xl">Sign Up</p>
                    <p className="text-small text-default-500">nextui.org</p>
                </div>
            </CardHeader>
            <Divider/>
            <CardBody className="flex gap-3">
                <Input type="text" label="Name" isRequired />
                <Input type="email" label="Surname" isRequired />
                <Input type="email" label="Email" isRequired />
                <Input type="password" label="Password" isRequired />
            </CardBody>
            <Divider/>
            <CardFooter className="justify-around">
                <Button className="flex" variant="light" color="primary">Login</Button>
                <Button className="flex" variant="solid" color="primary">Sign Up</Button>
            </CardFooter>
        </Card>
    )
}

export default SignupForm