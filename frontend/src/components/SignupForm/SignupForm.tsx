"use client"
import React, { useMemo, useState } from "react";
import { Card, CardHeader, CardBody, CardFooter, Divider, Button, Input, Link } from "@nextui-org/react";

import { defaultSignupData, ISignupErrorData } from "./SignupFormConsts";
import { checkEmail, checkPassword, handleSignUp } from "./SignupFormUtils";

const SignupForm = () => {

    const [data, setData] = useState(defaultSignupData);
    const [validation, setValidation] = useState(false);
    const [sent, setSent] = useState(false);

    const error = useMemo(() => {
        return {
            name: data.name === '',
            surname: data.surname === '',
            email: !checkEmail(data.email),
            password: !checkPassword(data.password)
        } as ISignupErrorData;
    }, [data]);

    return (
        <Card className="w-full max-w-xl min-w-0 h-fit">
            <CardHeader className="flex gap-5">
                <div className="flex flex-col">
                    <p className="text-xl font-medium">Sign Up</p>
                </div>
            </CardHeader>
            <Divider/>
            <CardBody className="flex gap-3">
                <Input
                    type="text"
                    size="sm"
                    label="Name"
                    isRequired
                    isInvalid={validation && error.name}
                    value={data.name}
                    errorMessage={validation && error.name ? "Name cannot be empty." : null}
                    onChange={e => setData(prev => { return { ...prev, name: e.target.value }})}
                />
                <Input
                    type="text"
                    size="sm"
                    label="Surname"
                    isRequired
                    isInvalid={validation && error.surname}
                    value={data.surname}
                    errorMessage={validation && error.surname ? "Surname cannot be empty." : null}
                    onChange={e => setData(prev => { return { ...prev, surname: e.target.value }})}
                />
                <Input
                    type="email"
                    size="sm"
                    label="Email"
                    isRequired
                    isInvalid={validation && error.email}
                    value={data.email}
                    errorMessage={validation && error.email ? "Invalid email address." : null}
                    onChange={e => setData(prev => { return { ...prev, email: e.target.value }})}
                />
                <Input
                    type="password"
                    size="sm"
                    label="Password"
                    isRequired
                    isInvalid={validation && error.password}
                    value={data.password}
                    errorMessage={validation && error.password
                        ? "The password should have 8 or more characters including lowercase and uppercase letters, a number and a special character."
                        : null
                    }
                    onChange={e => setData(prev => { return { ...prev, password: e.target.value }})}
                />
            </CardBody>
            <Divider/>
            <CardFooter className="justify-around">
                <Button
                    className="flex"
                    variant="light"
                    color="primary"
                    as={Link}
                    href="/login"
                >
                    Login
                </Button>
                <Button
                    className="flex"
                    variant="solid"
                    color="primary"
                    onClick={() => handleSignUp(setValidation, setSent, data)}
                    isLoading={sent}
                >
                    Sign Up
                </Button>
            </CardFooter>
        </Card>
    )
}

export default SignupForm