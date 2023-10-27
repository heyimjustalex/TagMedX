"use client"
import React, { useState } from "react";
import { Card, CardHeader, CardBody, CardFooter, Divider, Button, Input } from "@nextui-org/react";
import RouteLink from "next/link";

import { defaultLoginData } from "./LoginFormConsts";
import { handleLogin } from "./LoginFormUtils";

export default function LoginForm() {

    const [data, setData] = useState(defaultLoginData);
    const [sent, setSent] = useState(false);

    return (
        <Card className="w-full max-w-xl min-w-0 h-fit">
            <CardHeader className="flex gap-5">
                <div className="flex flex-col">
                    <p className="text-xl font-medium">Login</p>
                </div>
            </CardHeader>
            <Divider/>
            <CardBody className="flex gap-3">
                <Input
                    type="email"
                    size="sm"
                    label="Email"
                    value={data.email}
                    onChange={e => setData(prev => { return { ...prev, email: e.target.value }})}
                />
                <Input
                    type="password"
                    size="sm"
                    label="Password"
                    value={data.password}
                    onChange={e => setData(prev => { return { ...prev, password: e.target.value }})}
                />
            </CardBody>
            <Divider/>
            <CardFooter className="justify-around">
                <Button
                    className="flex"
                    variant="light"
                    color="primary"
                    as={RouteLink}
                    href="/signup"
                >
                    Sign Up
                </Button>
                <Button
                    className="flex"
                    variant="solid"
                    color="primary"
                    onClick={() => handleLogin(setSent, data)}
                    isLoading={sent}
                >
                    Login
                </Button>
            </CardFooter>
        </Card>
    )
}