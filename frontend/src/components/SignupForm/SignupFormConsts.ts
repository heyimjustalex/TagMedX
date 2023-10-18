export interface ISignupData {
    name: string,
    surname: string,
    email: string,
    password: string
}

export const defaultSignupData: ISignupData = {
    name: '',
    surname: '',
    email: '',
    password: ''
}

export interface ISignupErrorData {
    name: boolean,
    surname: boolean,
    email: boolean,
    password: boolean
}