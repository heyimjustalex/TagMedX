import { NextColor } from '../../consts/NextColor';

export async function handleSignUp(setValidation, setSent, data, router, notification) {
  setValidation(true);
  if(data.name !== '' && data.surname !== '' && checkEmail(data.email) && checkPassword(data.password)) {
    setSent(true);
    await fetch(process.env.NEXT_PUBLIC_API + '/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => {
      if(res.ok) {
        router.push('/');
        notification.make(NextColor.Success, 'Register', 'You have been successfully registered.');
      } else {
        throw Error(`${res.status} ${res.statusText}`)
      }
    })
    .catch(err => {
      console.error(err);
      notification.make(NextColor.Danger, 'Register', 'Something went wrong.');
    })
    setSent(false);
  }
}

export function checkEmail(email) {
  const emailRegExp = RegExp(/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/)
  return emailRegExp.test(email)
}
  
export function checkPassword(password) {
  const emailRegExp = RegExp(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/);
  return emailRegExp.test(password);
}
