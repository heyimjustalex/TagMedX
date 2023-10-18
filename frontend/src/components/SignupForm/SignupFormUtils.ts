export function handleSignUp(setValidation: any, setSent: any): void {
    setValidation(true);
}

export function checkEmail(email: string): boolean {
    const emailRegExp = RegExp(/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/)
    return emailRegExp.test(email)
}
  
export function checkPassword(password: string): boolean {
    const emailRegExp = RegExp(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/);
    return emailRegExp.test(password);
}